# 添加 _sentinel 类定义
class _sentinel:
    def __lt__(self, other):
        return True

import heapq
import random
import time
from datetime import datetime
from dash import Input, Output, callback, State, no_update, callback_context, dcc
from orm.db import db
from utils.log import log
# 导入寿命相关的ORM模型
from orm.chart_health_equipment import ChartHealthEquipment
from urllib.parse import urlparse, parse_qs
import pandas as pd
from io import BytesIO

@callback(
    Output('h_url-params-store', 'data'),
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
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
            parsed_carriage = params.get('carriage_no', [''])[0]
            parsed_component = params.get('component_type', [''])[0]
            parsed_start_time = params.get('start_time', [''])[0]
            parsed_end_time = params.get('end_time', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train,
        'carriage_no': parsed_carriage,
        'component_type': parsed_component,
        'start_time': parsed_start_time,
        'end_time': parsed_end_time
    }
    log.debug(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

@callback(
    [Output('h_health-table', 'data'),
     Output('h_health-table', 'pagination')],
    [Input('h_url-params-store', 'data'),
     Input('h_query_button', 'nClicks'),
     Input('h_health-table', 'pagination')],
    [State('h_train_no', 'value'),
     State('h_carriage_no', 'value'),
     State('h_health_comp', 'value'),
     State('h_start_time_range', 'value')],
    prevent_initial_call=False
)
def health_table_callback(url_params, nClicks, pagination, train_no, carriage_no, component_type, start_time_range):
    log.debug(f"[health_table_callback] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    query_train_no = ''
    query_carriage_no = ''
    query_component_type = ''
    query_start_time_range = None

    if trigger_id == 'h_url-params-store' and url_params:
        # 当URL参数变化时，使用URL参数进行查询
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_component_type = url_params.get('component_type', '')
        # 尝试从URL参数构建时间范围
        start_time = url_params.get('start_time', '')
        end_time = url_params.get('end_time', '')
        if start_time and end_time:
            try:
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                query_start_time_range = [start_time_obj, end_time_obj]
            except Exception as e:
                log.warning(f"[health_table_callback] URL时间格式转换错误: {e}")
        else:
            query_start_time_range = start_time_range
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    elif trigger_id == 'h_query_button' and nClicks > 0:
        # 当点击查询按钮时，使用表单参数进行查询
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_component_type = component_type or ''
        query_start_time_range = start_time_range
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    else:
        # 对于分页触发或初始加载，使用上次的查询参数
        if hasattr(health_table_callback, 'last_params'):
            query_train_no, query_carriage_no, query_component_type, query_start_time_range = health_table_callback.last_params
        else:
            # 初始加载时，尝试从URL获取参数
            if url_params:
                query_train_no = url_params.get('train_no', '')
                query_carriage_no = url_params.get('carriage_no', '')
                query_component_type = url_params.get('component_type', '')
            query_start_time_range = start_time_range

    # 保存当前参数
    health_table_callback.last_params = (
        query_train_no, query_carriage_no, query_component_type, query_start_time_range
    )

    # 构建查询
    query = ChartHealthEquipment.select()
    if query_train_no:
        query = query.where(ChartHealthEquipment.车号 == query_train_no)
    if query_carriage_no:
        query = query.where(ChartHealthEquipment.车厢号 == query_carriage_no)
    if query_component_type:
        if isinstance(query_component_type, list):
            query = query.where(ChartHealthEquipment.部件.in_(query_component_type))
        else:
            query = query.where(ChartHealthEquipment.部件 == query_component_type)

    # 处理时间范围 - 寿命表没有时间字段，注释掉相关代码
    # if query_start_time_range and isinstance(query_start_time_range, list) and len(query_start_time_range) == 2:
    #     start_time, end_time = query_start_time_range
    #     try:
    #         # 尝试将字符串转换为 datetime 对象
    #         if not isinstance(start_time, datetime):
    #             start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    #         if not isinstance(end_time, datetime):
    #             end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    #         query = query.where(ChartHealthEquipment.更新时间 >= start_time, ChartHealthEquipment.更新时间 <= end_time)
    #     except Exception as e:
    #         log.warning(f"[health_table_callback] 时间格式转换错误: {e}, 时间范围: {query_start_time_range}")
    # elif query_start_time_range:
    #     log.warning(f"[health_table_callback] 无效的时间范围: {query_start_time_range}")

    # 分页处理
    pagination = pagination or {'current': 1, 'pageSize': 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}

    # 计算总记录数
    total = query.count()

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.order_by(ChartHealthEquipment.耗用率.desc()).offset(
                (pagination['current'] - 1) * pagination['pageSize']
            ).limit(pagination['pageSize']).dicts())

        # 格式化数据
        formatted_data = [{
            '车号': item['车号'],
            '车厢号': item['车厢号'],
            '部件': item['部件'],
            '耗用率': f"{item['耗用率']:.2%}",
            '额定寿命': item['额定寿命'],
            '已耗': item['已耗']
        } for item in data]
        log.debug(f"[health_table_callback] 查询完成，返回 {len(formatted_data)}/{total} 条记录")
        return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize'],'showSizeChanger': pagination['showSizeChanger'],'pageSizeOptions': pagination['pageSizeOptions']}
    except Exception as e:
        log.error(f"[health_table_callback] 查询错误: {e}")
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

@callback(
    [Output('h_train_no', 'value'),
     Output('h_carriage_no', 'value'),
     Output('h_health_comp', 'value'),
     Output('h_start_time_range', 'value')],
    [Input('h_url-params-store', 'modified_timestamp')],
    [State('h_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    time.sleep(0.5)  # 关键延迟：等待前端元素加载
    
    log.debug(f"[sync_url_params_to_form] 函数被触发，收到参数: {url_params}")
    if not isinstance(url_params, dict):
        log.warning(f"[sync_url_params_to_form] 参数不是字典类型: {type(url_params)}")
        return None, None, None, []
    train_no = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    component_type = url_params.get('component_type')
    start_time = url_params.get('start_time')
    end_time = url_params.get('end_time')
    # AntdDateRangePicker需要字符串list，否则置空
    start_time_range = [start_time, end_time] if start_time and end_time else []
    log.debug(f"[sync_url_params_to_form] 同步到表单: 车号={train_no}, 车厢号={carriage_no}, 部件={component_type}, 时间范围={start_time_range}")
    return train_no, carriage_no, component_type, start_time_range

@callback(
    Output('h_download-excel', 'data'),
    Input('h_export_button', 'nClicks'),
    [State('h_train_no', 'value'),
     State('h_carriage_no', 'value'),
     State('h_health_comp', 'value'),
     State('h_start_time_range', 'value')],
    prevent_initial_call=True
)
def export_health_data_to_excel(nClicks, train_no, carriage_no, component_type, start_time_range):
    # 构建查询
    query = ChartHealthEquipment.select()
    if train_no:
        query = query.where(ChartHealthEquipment.车号 == train_no)
    if carriage_no:
        query = query.where(ChartHealthEquipment.车厢号 == carriage_no)
    if component_type:
        if isinstance(component_type, list):
            query = query.where(ChartHealthEquipment.部件.in_(component_type))
        else:
            query = query.where(ChartHealthEquipment.部件 == component_type)

    # 处理时间范围 - 寿命表没有时间字段，注释掉相关代码
    # if start_time_range and isinstance(start_time_range, list) and len(start_time_range) == 2:
    #     start_time, end_time = start_time_range
    #     try:
    #         if not isinstance(start_time, datetime):
    #             start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    #         if not isinstance(end_time, datetime):
    #             end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    #         query = query.where(ChartHealthEquipment.更新时间 >= start_time, ChartHealthEquipment.更新时间 <= end_time)
    #     except Exception as e:
    #         log.error(f"[export_health_data_to_excel] 时间格式转换错误: {e}")
    #         return no_update

    # 获取所有数据
    try:
        with db.atomic():
            data = list(query.order_by(ChartHealthEquipment.耗用率.desc()).dicts())

        # 格式化数据
        formatted_data = [{
            '车号': item['车号'],
            '车厢号': item['车厢号'],
            '部件': item['部件'],
            '耗用率': f"{item['耗用率']:.2%}",
            '额定寿命': item['额定寿命'],
            '已耗': item['已耗']
        } for item in data]

        # 创建Excel文件
        df = pd.DataFrame(formatted_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='寿命数据')
        output.seek(0)

        # 生成文件名
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'寿命数据导出_{current_time}.xlsx'

        log.info(f"[export_health_data_to_excel] 导出 {len(formatted_data)} 条数据到Excel文件: {filename}")
        return dcc.send_bytes(output.getvalue(), filename=filename)
    except Exception as e:
        log.error(f"[export_health_data_to_excel] 导出错误: {e}")
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
