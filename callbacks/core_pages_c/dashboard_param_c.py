
import heapq
import random
import time

from datetime import datetime, timedelta
from dash import Input, Output, callback, State, callback_context, no_update

from configs import BaseConfig
from orm.chart_view_param_test import Chart_view_param
from orm.db import db, _sentinel
from utils.log import log
import pandas as pd
from io import BytesIO
from dash import dcc
import pytz


# 查询按钮点击时更新URL参数
@callback(
    Output('url', 'search', allow_duplicate=True),
    Input('p_query_button', 'nClicks'),
    [State('p_train_no', 'value'),
     State('p_carriage_no', 'value'),
     State('p_component', 'value'),
     State('p_start_time_range', 'value')],
    prevent_initial_call=True
)
def update_url_on_query(nClicks, train_no, carriage_no, component, start_time_range):
    """查询按钮点击时更新URL参数"""
    if nClicks is None or nClicks == 0:
        return no_update
    
    log.debug(f"[update_url_on_query] 查询按钮点击: train_no={train_no}, carriage_no={carriage_no}, component={component}, start_time_range={start_time_range}")
    
    # 构建URL参数
    params = []
    
    if train_no:
        params.append(f"train_no={train_no}")
    
    if carriage_no:
        # 处理列表类型的车厢号
        if isinstance(carriage_no, list):
            carriage_str = ','.join(map(str, carriage_no))
        else:
            carriage_str = str(carriage_no)
        params.append(f"carriage_no={carriage_str}")
    
    if component:
        # 处理列表类型的组件
        if isinstance(component, list):
            component_str = ','.join(component)
        else:
            component_str = str(component)
        params.append(f"component={component_str}")
    
    if start_time_range and len(start_time_range) == 2:
        params.append(f"start_time={start_time_range[0]}")
        params.append(f"end_time={start_time_range[1]}")
    
    search = '?' + '&'.join(params) if params else ''
    log.debug(f"[update_url_on_query] 更新URL参数: {search}")
    return search
# 解析URL参数回调
@callback(
    Output('p_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.debug(f"[update_url_params] 开始解析URL参数: {search}")
    parsed_train = ''
    parsed_carriage = ''
    parsed_component = ''
    parsed_start_time = ''
    parsed_end_time = ''

    if search:
        try:
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
            parsed_carriage = params.get('carriage_no', [''])[0]
            parsed_component = params.get('component', [''])[0]
            parsed_start_time = params.get('start_time', [''])[0]
            parsed_end_time = params.get('end_time', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train,
        'carriage_no': parsed_carriage,
        'component': parsed_component,
        'start_time': parsed_start_time,
        'end_time': parsed_end_time
    }

    # 检查并设置默认时间
    if result['start_time'] == '' or result['end_time'] == '':
        result['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result['start_time'] = (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    log.debug(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

# 数据查询回调
@callback(
    Output('param_operation-data-chart', 'data'),
    [Input('p_url-params-store', 'data'),
     Input('p_query_button', 'nClicks')],
    [State('p_train_no', 'value'),
     State('p_carriage_no', 'value'),
     State('p_component', 'value'),
     State('p_start_time_range', 'value')],
    prevent_initial_call=False
)
def update_dashboard_data(url_params, nClicks, train_no, carriage_no, component, start_time_range):
    log.debug(f"[update_dashboard_data] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    shanghai = pytz.timezone('Asia/Shanghai')

    # 确定查询参数
    query_train_no = ''
    query_carriage_no = []
    query_components = []
    query_start_time = None
    query_end_time = None

    # 处理URL参数
    if trigger_id == 'p_url-params-store' and url_params:
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '').split(',') if url_params.get('carriage_no') else []
        query_components = url_params.get('component', '').split(',') if url_params.get('component') else ['新风温度-系统']
        # 处理时间范围
        start_time = url_params.get('start_time')
        end_time = url_params.get('end_time')
        if start_time and end_time:
            try:
                # query_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                # query_end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                query_start_time = shanghai.localize(datetime.fromisoformat(start_time))
                query_end_time = shanghai.localize(datetime.fromisoformat(end_time))
            except Exception as e:
                log.warning(f"line 98 [update_dashboard_data] URL时间格式转换错误: {e}")
    # 处理查询按钮
    elif trigger_id == 'p_query_button' and nClicks > 0:
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or []
        query_components = component or ['新风温度-系统']
        if start_time_range and len(start_time_range) == 2:
            try:
                # query_start_time = datetime.strptime(start_time_range[0], '%Y-%m-%d %H:%M:%S')
                # query_end_time = datetime.strptime(start_time_range[1], '%Y-%m-%d %H:%M:%S')
                query_start_time = shanghai.localize(datetime.fromisoformat(start_time_range[0]))
                query_end_time = shanghai.localize(datetime.fromisoformat(start_time_range[1]))
                log.warning(f"{start_time_range}")
            except Exception as e:
                log.warning(f"line 111 [update_dashboard_data] 表单时间格式转换错误: {e}")
    # 定时刷新或初始加载
    else:
        # 使用上次查询参数
        if hasattr(update_dashboard_data, 'last_params'):
            query_train_no, query_carriage_no, query_components, query_start_time, query_end_time = update_dashboard_data.last_params

    # 保存当前查询参数
    update_dashboard_data.last_params = (
        query_train_no, query_carriage_no, query_components, query_start_time, query_end_time
    )

    # 构建查询
    # 验证train_no和carriage_no必须存在
    if not (query_train_no and query_carriage_no):
        log.warning("[update_dashboard_data] train_no和carriage_no为必填参数")
        return []
    query = Chart_view_param.select()
    if query_train_no:
        query = query.where(Chart_view_param.dvc_train_no == query_train_no)
    if query_carriage_no:
        query = query.where(Chart_view_param.dvc_carriage_no.in_(query_carriage_no))
    if query_components:
        query = query.where(Chart_view_param.param_name.in_(query_components))
    if query_start_time and query_end_time:
        query = query.where(Chart_view_param.msg_calc_dvc_time.between(query_start_time, query_end_time))

    # 执行查询
    try:
        with db.atomic():
            data = list(query.order_by(Chart_view_param.msg_calc_dvc_time).dicts())

        # 格式化数据为折线图所需格式
        formatted_data = [{
            'msg_calc_dvc_time': item['msg_calc_dvc_time'].astimezone(shanghai).isoformat(timespec='seconds'),  # 2025-07-21T17:07:43+08:00
            'param_value': item['param_value'],
            'param_name': f"{item['param_name']}-车厢{item['dvc_carriage_no']}"
        } for item in data]

        log.debug(f"[update_dashboard_data] 查询完成，返回 {len(formatted_data)} 条记录")
        return formatted_data
    except Exception as e:
        log.error(f"[update_dashboard_data] 查询错误: {e}")
        return []
    finally:
        # 强制将当前连接放回连接池（绕过自动管理逻辑）
        try:
            conn = db.connection()  # 获取当前线程连接
            key = db.conn_key(conn)  # 生成连接唯一标识
            with db._pool_lock:  # 线程安全操作
                if key in db._in_use:
                    pool_conn = db._in_use.pop(key)
                    # 将连接添加回空闲连接堆
                    heapq.heappush(db._connections, (pool_conn.timestamp, _sentinel(), conn))
                    log.debug(f"显式放回连接 {key} 到连接池")
        except Exception as e:
            log.warning(f"显式释放连接失败: {str(e)}")

def clamp_15min(start_iso, end_iso):
    """返回 (修正后的 end_iso, 是否需要提示)"""
    if not start_iso or not end_iso:
        return end_iso, False
    s = datetime.fromisoformat(start_iso)
    e = datetime.fromisoformat(end_iso)
    limit = s + timedelta(minutes=15)
    if e > limit:
        return limit.isoformat(timespec='seconds'), True
    return end_iso, False

@callback(
    Output('param-message', 'maxCount'),   # 控制是否允许弹出
    Input('global-message-trigger', 'children')
)
def do_message(trigger):
    return 1 if trigger else 0

# 同步URL参数到表单回调
@callback(
    [Output('p_train_no', 'value'),
     Output('p_carriage_no', 'value'),
     Output('p_component', 'value'),
     Output('p_start_time_range', 'value'),
     Output('global-message-trigger', 'children')],   # 只用来“踢一脚”
    Input('p_url-params-store', 'modified_timestamp'),
    State('p_url-params-store', 'data'),
    prevent_initial_call=True
)
def sync_url_params_to_form(ts, url_params):
    time.sleep(0.5)
    if not isinstance(url_params, dict):
        return None, None, None, [], []

    train_no    = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    component   = url_params.get('component', '').split(',') if url_params.get('component') else None
    start_time  = url_params.get('start_time')
    end_time    = url_params.get('end_time')

    trigger = []
    if start_time and end_time:
        end_time, need = clamp_15min(start_time, end_time)
        if need:
            trigger = ['show']      # 非空即可触发提示
    start_time_range = [start_time, end_time] if start_time and end_time else []
    return train_no, carriage_no, component, start_time_range, trigger

@callback(
    Output('p_start_time_range', 'value', allow_duplicate=True),
    Output('global-message-trigger', 'children', allow_duplicate=True),
    Input('p_start_time_range', 'value'),
    prevent_initial_call=True
)
def enforce_15min_manual(sel):
    if not sel or len(sel) != 2:
        return sel, []
    new_end, need = clamp_15min(sel[0], sel[1])
    if need:
        return [sel[0], new_end], ['show']
    return sel, []

@callback(
    Output('p_download-excel', 'data'),
    Input('p_export_button', 'nClicks'),
    prevent_initial_call=True
)
def export_param_data_to_excel(nClicks):
    shanghai = pytz.timezone('Asia/Shanghai')
    # 获取上次查询参数
    if not hasattr(update_dashboard_data, 'last_params'):
        log.warning("[export_param_data_to_excel] 没有查询数据可供导出")
        return None
    
    query_train_no, query_carriage_no, query_components, query_start_time, query_end_time = update_dashboard_data.last_params
    
    # 验证必要参数
    if not (query_train_no and query_carriage_no):
        log.warning("[export_param_data_to_excel] train_no和carriage_no为必填参数")
        return None
    
    # 构建查询
    query = Chart_view_param.select()
    if query_train_no:
        query = query.where(Chart_view_param.dvc_train_no == query_train_no)
    if query_carriage_no:
        query = query.where(Chart_view_param.dvc_carriage_no.in_(query_carriage_no))
    if query_components:
        query = query.where(Chart_view_param.param_name.in_(query_components))
    if query_start_time and query_end_time:
        query = query.where(Chart_view_param.msg_calc_dvc_time.between(query_start_time, query_end_time))
    
    # 执行查询
    try:
        with db.atomic():
            data = list(query.order_by(Chart_view_param.msg_calc_dvc_time).dicts())
        
        # 格式化数据
        formatted_data = [{
            '时间': item['msg_calc_dvc_time'].astimezone(shanghai).isoformat(timespec='seconds'),  # 2025-07-21T17:07:43+08:00
            '参数名称': item['param_name'],
            '数值': item['param_value'],
            '车号': item['dvc_train_no'],
            '车厢号': item['dvc_carriage_no']
        } for item in data]
        
        if not formatted_data:
            log.warning("[export_param_data_to_excel] 没有找到可导出的数据")
            return None
        
        # 创建Excel文件
        df = pd.DataFrame(formatted_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='参数数据')
        output.seek(0)
        
        # 生成文件名
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'参数数据导出_{current_time}.xlsx'
        
        log.info(f"[export_param_data_to_excel] 导出 {len(formatted_data)} 条数据到Excel文件: {filename}")
        return dcc.send_bytes(output.getvalue(), filename=filename)
    except Exception as e:
        log.error(f"[export_param_data_to_excel] 导出错误: {e}")
        return None
    finally:
        # 强制将当前连接放回连接池（绕过自动管理逻辑）
        try:
            conn = db.connection()  # 获取当前线程连接
            key = db.conn_key(conn)  # 生成连接唯一标识
            with db._pool_lock:  # 线程安全操作
                if key in db._in_use:
                    pool_conn = db._in_use.pop(key)
                    # 将连接添加回空闲连接堆
                    heapq.heappush(db._connections, (pool_conn.timestamp, _sentinel(), conn))
                    log.debug(f"显式放回连接 {key} 到连接池")
        except Exception as e:
            log.warning(f"显式释放连接失败: {str(e)}")