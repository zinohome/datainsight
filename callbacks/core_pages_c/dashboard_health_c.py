import heapq
import random
import time
from datetime import datetime, timedelta
from dash import Input, Output, callback, State, no_update, callback_context, dcc
from orm.db import db, _sentinel
from utils.log import log
# 导入寿命相关的ORM模型
from orm.chart_health_equipment import ChartHealthEquipment
from orm.d_chart_health_clean import DChartHealthClean
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

    if search:
        try:
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
            parsed_carriage = params.get('carriage_no', [''])[0]
            parsed_component = params.get('component_type', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train,
        'carriage_no': parsed_carriage,
        'component_type': parsed_component
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
     State('h_health_comp', 'value')],
    prevent_initial_call=False
)
def health_table_callback(url_params, nClicks, pagination, train_no, carriage_no, component_type):
    log.debug(f"[health_table_callback] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    query_train_no = ''
    query_carriage_no = ''
    query_component_type = ''

    if trigger_id == 'h_url-params-store' and url_params:
        # 当URL参数变化时，使用URL参数进行查询
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_component_type = url_params.get('component_type', '')
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    elif trigger_id == 'h_query_button' and nClicks > 0:
        # 当点击查询按钮时，使用表单参数进行查询
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_component_type = component_type or ''
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    else:
        # 对于分页触发或初始加载，使用上次的查询参数
        if hasattr(health_table_callback, 'last_params'):
            query_train_no, query_carriage_no, query_component_type = health_table_callback.last_params
        else:
            # 初始加载时，尝试从URL获取参数
            if url_params:
                query_train_no = url_params.get('train_no', '')
                query_carriage_no = url_params.get('carriage_no', '')
                query_component_type = url_params.get('component_type', '')

    # 保存当前参数
    health_table_callback.last_params = (
        query_train_no, query_carriage_no, query_component_type
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
            '额定寿命[小时/次]': item['额定寿命'],
            '已耗[秒/次]': item['已耗'],
            '操作':{
                        'content': f'清零',
                        'type': 'dashed',
                        'danger': True,
                        'custom': 'balabalabalabala',
                    },
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
     Output('h_health_comp', 'value')],
    [Input('h_url-params-store', 'modified_timestamp')],
    [State('h_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    time.sleep(0.5)  # 关键延迟：等待前端元素加载
    
    log.debug(f"[sync_url_params_to_form] 函数被触发，收到参数: {url_params}")
    if not isinstance(url_params, dict):
        log.warning(f"[sync_url_params_to_form] 参数不是字典类型: {type(url_params)}")
        return None, None, None
    train_no = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    component_type = url_params.get('component_type')
    log.debug(f"[sync_url_params_to_form] 同步到表单: 车号={train_no}, 车厢号={carriage_no}, 部件={component_type}")
    return train_no, carriage_no, component_type

@callback(
    [Output('h_clean_table', 'data'),
     Output('h_clean_table', 'pagination')],
    [Input('h_url-params-store', 'data'),
     Input('h_query_button', 'nClicks'),
     Input('h_clean_table', 'pagination'),
     Input('h_health-table', 'nClicksButton')],
    [State('h_train_no', 'value'),
     State('h_carriage_no', 'value'),
     State('h_health_comp', 'value'),
     State('h_health-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=False
)

def clean_table_callback(url_params, nClicks, pagination, nClicksButton, train_no, carriage_no, component_type, recentlyButtonClickedRow_health_table):
    ctx = callback_context
    # 打印完整的触发信息，帮助调试
    log.debug(f"[clean_table_callback] 触发详情: {ctx.triggered if ctx.triggered else '初始加载'}")
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    trigger_prop = ctx.triggered[0]["prop_id"].split(".")[1] if ctx.triggered and len(ctx.triggered[0]["prop_id"].split(".")) > 1 else None
    log.debug(f"[clean_table_callback] 触发ID: {trigger_id}, 触发属性: {trigger_prop}")
    # 增加按钮点击检测的详细日志
    if trigger_id == 'h_health-table' and trigger_prop == 'nClicksButton':
        log.debug(f"[clean_table_callback] 检测到h_health-table的nClicksButton事件, nClicksButton={nClicksButton}")
    query_train_no = ''
    query_carriage_no = ''
    query_component_type = ''
    reset_pagination = False

    # 处理清零按钮点击 - 检查是否是nClicksButton触发
    if trigger_id == 'h_health-table' and trigger_prop == 'nClicksButton' and nClicksButton is not None and nClicksButton > 0:
        log.debug(f"[clean_table_callback] 检测到清零按钮点击，nClicksButton={nClicksButton}")
        # 使用h_health-table的点击行数据
        health_table_row = recentlyButtonClickedRow_health_table
        if health_table_row:
            try:
                # 获取点击行的数据
                row_data = health_table_row
                log.debug(f"[clean_table_callback] h_health-table点击行数据: {row_data}")

                # 创建新的清零记录
                with db.atomic():
                    # 生成新的clean_time（当前时间）
                    new_clean_time = datetime.now()

                    # 插入新记录到DChartHealthClean表
                    DChartHealthClean.create(
                        clean_time=new_clean_time,
                        车号=row_data['车号'],
                        车厢号=row_data['车厢号'],
                        部件=row_data['部件'],
                        已耗=row_data['已耗']
                    )
                    log.info(f"[clean_table_callback] 成功添加清零记录: 车号={row_data['车号']}, 车厢号={row_data['车厢号']}, 部件={row_data['部件']}")

                # 重置分页到第一页以显示最新数据
                reset_pagination = True
            except Exception as e:
                log.error(f"[clean_table_callback] 处理按钮点击错误: {e}")
        else:
            log.warning("[clean_table_callback] 未获取到点击行数据")

    # 处理其他触发源
    if trigger_id == 'h_url-params-store' and url_params:
        # 当URL参数变化时，使用URL参数进行查询
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_component_type = url_params.get('component_type', '')
        reset_pagination = True
    elif trigger_id == 'h_query_button' and nClicks > 0:
        # 当点击查询按钮时，使用表单参数进行查询
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_component_type = component_type or ''
        reset_pagination = True
    else:
        # 对于分页触发或初始加载，使用上次的查询参数
        if hasattr(clean_table_callback, 'last_params'):
            query_train_no, query_carriage_no, query_component_type = clean_table_callback.last_params
        else:
            # 初始加载时，尝试从URL获取参数
            if url_params:
                query_train_no = url_params.get('train_no', '')
                query_carriage_no = url_params.get('carriage_no', '')
                query_component_type = url_params.get('component_type', '')

    # 保存当前参数
    clean_table_callback.last_params = (
        query_train_no, query_carriage_no, query_component_type
    )

    # 重置分页（如果需要）
    if reset_pagination:
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100]}

    # 构建查询
    query = DChartHealthClean.select()
    if query_train_no:
        query = query.where(DChartHealthClean.车号 == query_train_no)
    if query_carriage_no:
        query = query.where(DChartHealthClean.车厢号 == query_carriage_no)
    if query_component_type:
        if isinstance(query_component_type, list):
            query = query.where(DChartHealthClean.部件.in_(query_component_type))
        else:
            query = query.where(DChartHealthClean.部件 == query_component_type)

    # 分页处理
    pagination = pagination or {'current': 1, 'pageSize': 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}

    # 计算总记录数
    total = query.count()

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.order_by(DChartHealthClean.clean_time.desc()).offset(
                (pagination['current'] - 1) * pagination['pageSize']
            ).limit(pagination['pageSize']).dicts())

        # 格式化数据（包含操作按钮）
        formatted_data = [{
            '清除时间': item['clean_time'].strftime('%Y-%m-%d %H:%M:%S'),
            '车号': item['车号'],
            '车厢号': item['车厢号'],
            '部件': item['部件'],
            '已耗[秒/次]': item['已耗'],
            '操作':{
                'content': f'清零',
                'type': 'dashed',
                'danger': True,
                'custom': f"{item['车号']}_{item['车厢号']}_{item['部件']}",
            },
        } for item in data]
        log.debug(f"[clean_table_callback] 查询完成，返回 {len(formatted_data)}/{total} 条记录")
        return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize'],'showSizeChanger': pagination['showSizeChanger'],'pageSizeOptions': pagination['pageSizeOptions']}
    except Exception as e:
        log.error(f"[clean_table_callback] 查询错误: {e}")
        return [], pagination
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
    Output('h_download-excel', 'data'),
    Input('h_export_button', 'nClicks'),
    [State('h_train_no', 'value'),
     State('h_carriage_no', 'value'),
     State('h_health_comp', 'value')],
    prevent_initial_call=True
)
def export_health_data_to_excel(nClicks, train_no, carriage_no, component_type):
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
            '额定寿命[小时/次]': item['额定寿命'],
            '已耗[秒/次]': item['已耗']
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
