
import heapq
import random
import time
from datetime import datetime
from dash import Input, Output, callback, State, no_update, callback_context, dcc
from orm.db import db, _sentinel
from utils.log import log
from orm.chart_view_fault_timed import Chart_view_fault_timed
from orm.chart_table_fault_timed import Chart_table_fault_timed
from orm.d_chart_fault_clean import DChartFaultClean
from urllib.parse import urlparse, parse_qs
import pandas as pd
from io import BytesIO

dcc.Store(id='fault-table-refresh-trigger')

@callback(
    Output('f_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.debug(f"[update_url_params] 开始解析URL参数: {search}")
    parsed_train = ''
    parsed_carriage = ''
    parsed_fault = ''
    parsed_start_time = ''
    parsed_end_time = ''

    if search:
        try:
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
            parsed_carriage = params.get('carriage_no', [''])[0]
            parsed_fault = params.get('fault_type', [''])[0]
            parsed_start_time = params.get('start_time', [''])[0]
            parsed_end_time = params.get('end_time', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train,
        'carriage_no': parsed_carriage,
        'fault_type': parsed_fault,
        'start_time': parsed_start_time,
        'end_time': parsed_end_time
    }
    log.debug(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

@callback(
    [Output('f_fault-warning-table', 'data'),
     Output('f_fault-warning-table', 'pagination')],
    [Input('f_url-params-store', 'data'),
     Input('f_query_button', 'nClicks'),
     Input('f_fault-warning-table', 'pagination'),
     Input('fault-table-refresh-trigger', 'data')],  # 添加这一行
    [State('f_train_no', 'value'),
     State('f_carriage_no', 'value'),
     State('f_fault_type', 'value'),
     State('f_start_time_range', 'value')],
    prevent_initial_call=False
)
def fault_warning_table_callback(url_params, nClicks, pagination, refresh_trigger, train_no, carriage_no, fault_type, start_time_range):
    log.debug(f"[fault_warning_table_callback] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    query_train_no = ''
    query_carriage_no = ''
    query_fault_type = ''
    query_start_time_range = None

    if refresh_trigger is not None and isinstance(refresh_trigger, dict) and refresh_trigger.get('trigger'):
        log.debug(f"[fault_warning_table_callback] 由刷新标志触发，使用传递的查询参数")
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_fault_type = fault_type or ''
        query_start_time_range = start_time_range
    elif trigger_id == 'f_url-params-store' and url_params:
        # 当URL参数变化时，使用URL参数进行查询
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_fault_type = url_params.get('fault_type', '')
        # 尝试从URL参数构建时间范围
        start_time = url_params.get('start_time', '')
        end_time = url_params.get('end_time', '')
        if start_time and end_time:
            try:
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                query_start_time_range = [start_time_obj, end_time_obj]
            except Exception as e:
                log.warning(f"[fault_warning_table_callback] URL时间格式转换错误: {e}")
        else:
            query_start_time_range = start_time_range
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    elif trigger_id == 'f_query_button' and nClicks > 0:
        # 当点击查询按钮时，使用表单参数进行查询
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_fault_type = fault_type or ''
        query_start_time_range = start_time_range
        # 重置分页到第一页
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}
    else:
        # 对于分页触发或初始加载，使用上次的查询参数
        if hasattr(fault_warning_table_callback, 'last_params'):
            query_train_no, query_carriage_no, query_fault_type, query_start_time_range = fault_warning_table_callback.last_params
        else:
            # 初始加载时，尝试从URL获取参数
            if url_params:
                query_train_no = url_params.get('train_no', '')
                query_carriage_no = url_params.get('carriage_no', '')
                query_fault_type = url_params.get('fault_type', '')
            query_start_time_range = start_time_range

    # 保存当前参数
    fault_warning_table_callback.last_params = (
        query_train_no, query_carriage_no, query_fault_type, query_start_time_range
    )

    # 构建查询
    query = Chart_view_fault_timed.select()
    if query_train_no:
        query = query.where(Chart_view_fault_timed.dvc_train_no == query_train_no)
    if query_carriage_no:
        query = query.where(Chart_view_fault_timed.dvc_carriage_no == query_carriage_no)
    if query_fault_type:
        query = query.where(Chart_view_fault_timed.fault_type == query_fault_type)

    # 处理时间范围
    if query_start_time_range and isinstance(query_start_time_range, list) and len(query_start_time_range) == 2:
        start_time, end_time = query_start_time_range
        try:
            # 尝试将字符串转换为 datetime 对象
            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            if not isinstance(end_time, datetime):
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            query = query.where(Chart_view_fault_timed.start_time >= start_time, Chart_view_fault_timed.start_time <= end_time)
        except Exception as e:
            log.warning(f"[fault_warning_table_callback] 时间格式转换错误: {e}, 时间范围: {query_start_time_range}")
    elif query_start_time_range:
        log.warning(f"[fault_warning_table_callback] 无效的时间范围: {query_start_time_range}")

    # 分页处理
    pagination = pagination or {'current': 1, 'pageSize': 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}

    # 计算总记录数
    total = query.count()

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.order_by(
                Chart_view_fault_timed.status,
                Chart_view_fault_timed.start_time.desc()).offset(
                (pagination['current'] - 1) * pagination['pageSize']
            ).limit(pagination['pageSize']).dicts())

        # 格式化数据
        formatted_data = [{
            '车号': item['dvc_train_no'],
            '车厢号': item['dvc_carriage_no'],
            '故障名称': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] is not None else '',
            '结束时间': item['end_time'].strftime('%Y-%m-%d %H:%M:%S') if item['end_time'] is not None else '',
            '状态': item['status'],
            '故障等级': item['fault_level'],
            '类型': item['fault_type'],
            '维修建议': item['repair_suggestion'],
            '操作':{
                        'content': f'清除',
                        'type': 'dashed',
                        'danger': True,
                        'custom': 'balabalabalabala',
                    },
        } for item in data]
        log.debug(f"[fault_warning_table_callback] 查询完成，返回 {len(formatted_data)}/{total} 条记录")
        return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize'],'showSizeChanger': pagination['showSizeChanger'],'pageSizeOptions': pagination['pageSizeOptions']}
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

@callback(
    [Output('f_train_no', 'value'),
     Output('f_carriage_no', 'value'),
     Output('f_fault_type', 'value'),
     Output('f_start_time_range', 'value')],
    [Input('f_url-params-store', 'modified_timestamp')],
    [State('f_url-params-store', 'data')],
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
    fault_type = url_params.get('fault_type')
    start_time = url_params.get('start_time')
    end_time = url_params.get('end_time')
    # AntdDateRangePicker需要字符串list，否则置空
    start_time_range = [start_time, end_time] if start_time and end_time else []
    log.debug(f"[sync_url_params_to_form] 同步到表单: 车号={train_no}, 车厢号={carriage_no}, 类型={fault_type}, 时间范围={start_time_range}")
    return train_no, carriage_no, fault_type, start_time_range

@callback(
    [Output('f_clean_table', 'data'),
     Output('f_clean_table', 'pagination'),
     Output('fault-table-refresh-trigger', 'data')],  # 添加这一行],
    [Input('f_url-params-store', 'data'),
     Input('f_query_button', 'nClicks'),
     Input('f_clean_table', 'pagination'),
     Input('f_fault-warning-table', 'nClicksButton')],
    [State('f_train_no', 'value'),
     State('f_carriage_no', 'value'),
     State('f_fault_type', 'value'),
     State('f_fault-warning-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=False
)
def fault_clean_table_callback(url_params, nClicks, pagination, nClicksButton, train_no, carriage_no, fault_type, recentlyButtonClickedRow_fault_table):
    ctx = callback_context
    # 打印完整的触发信息，帮助调试
    log.debug(f"[fault_clean_table_callback] 触发详情: {ctx.triggered if ctx.triggered else '初始加载'}")
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    trigger_prop = ctx.triggered[0]["prop_id"].split(".")[1] if ctx.triggered and len(ctx.triggered[0]["prop_id"].split(".")) > 1 else None
    log.debug(f"[fault_clean_table_callback] 触发ID: {trigger_id}, 触发属性: {trigger_prop}")
    refresh_trigger = None
    # 增加按钮点击检测的详细日志
    if trigger_id == 'f_fault-warning-table' and trigger_prop == 'nClicksButton':
        log.debug(f"[fault_clean_table_callback] 检测到f_fault-warning-table的nClicksButton事件, nClicksButton={nClicksButton}")
    query_train_no = ''
    query_carriage_no = ''
    query_fault_type = ''
    reset_pagination = False

    # 处理清除按钮点击 - 检查是否是nClicksButton触发
    if trigger_id == 'f_fault-warning-table' and trigger_prop == 'nClicksButton' and nClicksButton is not None and nClicksButton > 0:
        log.debug(f"[fault_clean_table_callback] 检测到清除按钮点击，nClicksButton={nClicksButton}")
        # 使用f_fault-warning-table的点击行数据
        fault_table_row = recentlyButtonClickedRow_fault_table
        if fault_table_row:
            try:
                # 获取点击行的数据
                row_data = fault_table_row
                log.debug(f"[fault_clean_table_callback] f_fault-warning-table点击行数据: {row_data}")

                # 创建新的清除记录
                with db.atomic():
                    # 生成新的clean_time（当前时间）
                    new_clean_time = datetime.now()

                    # 插入新记录到DChartFaultClean表
                    DChartFaultClean.create(
                        clean_time=new_clean_time,
                        dvc_train_no=row_data['车号'],
                        dvc_carriage_no=row_data['车厢号'],
                        param_name=row_data['故障名称'],
                        start_time=datetime.strptime(row_data['开始时间'], '%Y-%m-%d %H:%M:%S'),
                        fault_level=row_data['故障等级'],
                        fault_type=row_data['类型']
                    )

                    # 更新Chart_view_fault_timed表中对应记录的status为"结束"并设置update_time
                    Chart_table_fault_timed.update(
                        status="结束",
                        end_time=new_clean_time,
                        update_time=new_clean_time
                    ).where(
                        (Chart_table_fault_timed.dvc_train_no == row_data['车号']) &
                        (Chart_table_fault_timed.dvc_carriage_no == row_data['车厢号']) &
                        (Chart_table_fault_timed.fault_name == row_data['故障名称']) &
                        (Chart_table_fault_timed.start_time == datetime.strptime(row_data['开始时间'], '%Y-%m-%d %H:%M:%S'))
                    ).execute()
                    log.info(f"[fault_clean_table_callback] 成功添加清除记录: 车号={row_data['车号']}, 车厢号={row_data['车厢号']}, 故障名称={row_data['故障名称']}")
                    #障警告表刷新
                    refresh_trigger = {
                        'trigger': True,
                    }

                # 重置分页到第一页以显示最新数据
                reset_pagination = True
            except Exception as e:
                log.error(f"[fault_clean_table_callback] 处理按钮点击错误: {e}")
                refresh_trigger = None
        else:
            log.warning("[fault_clean_table_callback] 未获取到点击行数据")
            refresh_trigger = None

    # 处理其他触发源
    if trigger_id == 'f_url-params-store' and url_params:
        # 当URL参数变化时，使用URL参数进行查询
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_fault_type = url_params.get('fault_type', '')
        reset_pagination = True
    elif trigger_id == 'f_query_button' and nClicks > 0:
        # 当点击查询按钮时，使用表单参数进行查询
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_fault_type = fault_type or ''
        reset_pagination = True
    else:
        # 对于分页触发或初始加载，使用上次的查询参数
        if hasattr(fault_clean_table_callback, 'last_params'):
            query_train_no, query_carriage_no, query_fault_type = fault_clean_table_callback.last_params
        else:
            # 初始加载时，尝试从URL获取参数
            if url_params:
                query_train_no = url_params.get('train_no', '')
                query_carriage_no = url_params.get('carriage_no', '')
                query_fault_type = url_params.get('fault_type', '')

    # 保存当前参数
    fault_clean_table_callback.last_params = (
        query_train_no, query_carriage_no, query_fault_type
    )

    # 重置分页（如果需要）
    if reset_pagination:
        pagination = {'current': 1, 'pageSize': pagination.get('pageSize', 10) if pagination else 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100]}

    # 构建查询
    query = DChartFaultClean.select()
    if query_train_no:
        query = query.where(DChartFaultClean.dvc_train_no == query_train_no)
    if query_carriage_no:
        query = query.where(DChartFaultClean.dvc_carriage_no == query_carriage_no)
    if query_fault_type:
        query = query.where(DChartFaultClean.fault_type == query_fault_type)

    # 分页处理
    pagination = pagination or {'current': 1, 'pageSize': 10,'showSizeChanger': True,'pageSizeOptions': [10, 20, 50, 100],'showQuickJumper': True}

    # 计算总记录数
    total = query.count()

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.order_by(DChartFaultClean.clean_time.desc()).offset(
                (pagination['current'] - 1) * pagination['pageSize']
            ).limit(pagination['pageSize']).dicts())

        # 格式化数据
        formatted_data = [{
            '清除时间': item['clean_time'].strftime('%Y-%m-%d %H:%M:%S'),
            '车号': item['dvc_train_no'],
            '车厢号': item['dvc_carriage_no'],
            '故障名称': item['param_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '故障等级': item['fault_level'],
            '故障类型': item['fault_type'],
        } for item in data]
        log.debug(f"[fault_clean_table_callback] 查询完成，返回 {len(formatted_data)}/{total} 条记录")
        return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize'],'showSizeChanger': pagination['showSizeChanger'],'pageSizeOptions': pagination['pageSizeOptions']}, refresh_trigger
    except Exception as e:
        log.error(f"[fault_clean_table_callback] 查询错误: {e}")
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
    Output('f_download-excel', 'data'),
    Input('f_export_button', 'nClicks'),
    [State('f_train_no', 'value'),
     State('f_carriage_no', 'value'),
     State('f_fault_type', 'value'),
     State('f_start_time_range', 'value')],
    prevent_initial_call=True
)
def export_fault_data_to_excel(nClicks, train_no, carriage_no, fault_type, start_time_range):
    # 构建查询
    query = Chart_view_fault_timed.select()
    if train_no:
        query = query.where(Chart_view_fault_timed.dvc_train_no == train_no)
    if carriage_no:
        query = query.where(Chart_view_fault_timed.dvc_carriage_no == carriage_no)
    if fault_type:
        query = query.where(Chart_view_fault_timed.fault_type == fault_type)

    # 处理时间范围
    if start_time_range and isinstance(start_time_range, list) and len(start_time_range) == 2:
        start_time, end_time = start_time_range
        try:
            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            if not isinstance(end_time, datetime):
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            query = query.where(Chart_view_fault_timed.start_time >= start_time, Chart_view_fault_timed.start_time <= end_time)
        except Exception as e:
            log.error(f"[export_fault_data_to_excel] 时间格式转换错误: {e}")
            return no_update

    # 获取所有数据
    try:
        with db.atomic():
            data = list(query.order_by(Chart_view_fault_timed.start_time.desc()).dicts())

        # 格式化数据
        formatted_data = [{
            '车号': item['dvc_train_no'],
            '车厢号': item['dvc_carriage_no'],
            '故障名称': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '结束时间': item['end_time'].strftime('%Y-%m-%d %H:%M:%S') if item['end_time'] else '',
            '状态': item['status'],
            '故障等级': item['fault_level'],
            '类型': item['fault_type'],
            '维修建议': item['repair_suggestion']
        } for item in data]

        # 创建Excel文件
        df = pd.DataFrame(formatted_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='故障数据')
        output.seek(0)

        # 生成文件名
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'故障数据导出_{current_time}.xlsx'

        log.info(f"[export_fault_data_to_excel] 导出 {len(formatted_data)} 条数据到Excel文件: {filename}")
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
