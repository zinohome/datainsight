# 在文件顶部添加 datetime 导入
import time
import re
from datetime import datetime  # 添加这一行
from dash import Input, Output, callback, State, no_update, callback_context, dash
from configs import LayoutConfig
from orm.db import db
from utils.log import log
from orm.chart_view_fault_timed import Chart_view_fault_timed
from urllib.parse import urlparse, parse_qs

# 全局变量用于跟踪URL参数初始化状态
# 在文件顶部初始化全局变量
url_initialized = False
initial_params = None
# 添加一个新的全局变量用于标记是否已经执行过一次性初始化
one_time_initialized = False
last_query_time = 0
DEBOUNCE_TIME = 1.0  # 1秒防抖

@callback(
    Output('initial-url-params', 'data', allow_duplicate=True),
    Input('root-url', 'href'),
    prevent_initial_call=True
)
def initialize_url_params(href):
    global url_initialized, initial_params
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered and ctx.triggered[0]["prop_id"] != "." else None
    log.info(f"[initialize_url_params] 触发源: {trigger_id}, url_initialized={url_initialized}, href={href}")
    
    # 增强判断：已初始化且触发源不是特定需要的，直接返回no_update
    if url_initialized and trigger_id == 'root-url':
        log.info("[initialize_url_params] 已初始化且触发源为root-url，不执行任何操作")
        return dash.no_update
    
    # 未初始化则解析URL参数
    if not url_initialized:
        log.info(f"[initialize_url_params] 开始解析URL参数")
        parsed_train = ''
        parsed_carriage = ''
        parsed_fault = ''

        if href:
            try:
                parsed_url = urlparse(href)
                params = parse_qs(parsed_url.query)
                parsed_train = params.get('train_no', [''])[0]
                parsed_carriage = params.get('carriage_no', [''])[0]
                parsed_fault = params.get('fault_type', [''])[0]
            except Exception as e:
                log.error(f"[initialize_url_params] 解析URL参数错误: {e}")

        initial_params = {
            'train_no': parsed_train,
            'carriage_no': parsed_carriage,
            'fault_type': parsed_fault
        }
        url_initialized = True
        log.info(f"[initialize_url_params] URL参数初始化完成: {initial_params}")
        return initial_params
    
    # 其他情况返回no_update
    return dash.no_update

@callback(
    [Output('train_no', 'value'),
     Output('carriage_no', 'value'),
     Output('fault_type', 'value')],
    [Input('initial-url-params', 'data')],
    [State('train_no', 'value'),
     State('carriage_no', 'value'),
     State('fault_type', 'value')],
    prevent_initial_call=True
)
def sync_initial_params_to_form(initial_params, current_train, current_carriage, current_fault):
    """将初始URL参数同步到表单"""
    if initial_params:
        # 检查参数是否有变化
        if (initial_params['train_no'] != current_train or
            initial_params['carriage_no'] != current_carriage or
            initial_params['fault_type'] != current_fault):
            log.info(f"[sync_initial_params_to_form] 同步初始参数到表单: {initial_params}")
            return (
                initial_params['train_no'],
                initial_params['carriage_no'],
                initial_params['fault_type']
            )
    return no_update, no_update, no_update

@callback(
    Output('query-trigger', 'data', allow_duplicate=True),
    Input('initial-url-params', 'data'),
    [State('start_time_range', 'value')],
    prevent_initial_call=True
)
def trigger_initial_query(initial_params, start_time_range):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered and ctx.triggered[0]["prop_id"] != "." else None
    if not initial_params:  # 防止无效空输入清空表格
        log.info("[trigger_initial_query] 输入参数为空，直接no_update防止覆盖")
        return dash.no_update
    if initial_params:
        result = {
            'train_no': initial_params.get('train_no', ''),
            'carriage_no': initial_params.get('carriage_no', ''),
            'fault_type': initial_params.get('fault_type', ''),
            'start_time_range': start_time_range,
            'timestamp': time.time()
        }
    log.info(f"[trigger_initial_query][输出即将返回] {result}")
    return result if result else no_update

@callback(
    [Output('fault-warning-table', 'data'),
     Output('fault-warning-table', 'pagination')],
    [Input('query-trigger', 'data'),
     Input('fault-warning-table', 'pagination')],
    prevent_initial_call=True
)
def fault_warning_table_callback(query_trigger, pagination):
    log.info(f"[fault_warning_table_callback][触发] callback_context.triggered: {callback_context.triggered}")
    log.info(f"[fault_warning_table_callback][输入] query_trigger={query_trigger} ...")
    global last_query_time
    current_time = time.time()
    if (current_time - last_query_time) < DEBOUNCE_TIME:
        log.warning(f"[fault_warning_table_callback][防抖拦截] {current_time - last_query_time:.2f}s")
        return no_update
    last_query_time = current_time

    # 确定查询参数
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered and ctx.triggered[0]["prop_id"] != "." else None
    if trigger_id == 'query-trigger' and query_trigger:
        train_no = query_trigger.get('train_no', '')
        carriage_no = query_trigger.get('carriage_no', '')
        fault_type = query_trigger.get('fault_type', '')
        start_time_range = query_trigger.get('start_time_range')
    else:
        # 从上次查询参数获取
        if hasattr(fault_warning_table_callback, 'last_params'):
            train_no, carriage_no, fault_type, start_time_range = fault_warning_table_callback.last_params
        else:
            train_no, carriage_no, fault_type, start_time_range = '', '', '', None

    # 保存当前参数
    fault_warning_table_callback.last_params = (train_no, carriage_no, fault_type, start_time_range)

    # 构建查询
    query = Chart_view_fault_timed.select()
    if train_no:
        query = query.where(Chart_view_fault_timed.dvc_train_no == train_no)
    if carriage_no:
        query = query.where(Chart_view_fault_timed.dvc_carriage_no == carriage_no)
    if fault_type:
        query = query.where(Chart_view_fault_timed.fault_type == fault_type)

    # 修复缩进 - 将时间范围处理逻辑移出 if fault_type 块
    # 处理时间范围
    if start_time_range and isinstance(start_time_range, list) and len(start_time_range) == 2:
        start_time, end_time = start_time_range
        try:
            # 尝试将字符串转换为 datetime 对象
            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            if not isinstance(end_time, datetime):
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            query = query.where(Chart_view_fault_timed.start_time >= start_time, Chart_view_fault_timed.start_time <= end_time)
        except Exception as e:
            log.warning(f"[fault_warning_table_callback] 时间格式转换错误: {e}, 时间范围: {start_time_range}")
    elif start_time_range:
        log.warning(f"[fault_warning_table_callback] 无效的时间范围: {start_time_range}")

    # 分页处理
    pagination = pagination or {'current': 1, 'pageSize': 5}

    # 计算总记录数
    total = query.count()

    # 执行查询并获取数据
    with db.atomic():
        data = query.order_by(Chart_view_fault_timed.start_time.desc()).offset(
            (pagination['current'] - 1) * pagination['pageSize']
        ).limit(pagination['pageSize']).dicts()

    # 格式化数据
    formatted_data = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '故障名称': item['param_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] is not None else '',
        '结束时间': item['end_time'].strftime('%Y-%m-%d %H:%M:%S') if item['end_time'] is not None else '',
        '状态': item['status'],
        '故障等级': item['fault_level'],
        '类型': item['fault_type'],
        '维修建议': item['repair_suggestion']
    } for item in data]

    log.info(f"[fault_warning_table_callback] 查询完成，返回 {len(formatted_data)}/{total} 条记录")
    return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize']}


@callback(
    Output('initial-url-params', 'data', allow_duplicate=True),
    Input('app-initialized', 'data'),  # 假设存在一个应用初始化完成的信号
    prevent_initial_call=True
)
def one_time_url_initialization(app_initialized):
    global one_time_initialized
    if not one_time_initialized and app_initialized:
        # 执行一次性初始化逻辑
        # 这里可以放置需要在应用启动时执行一次的代码
        one_time_initialized = True
        log.info("[one_time_url_initialization] 应用已初始化，执行一次性URL参数设置")
        return initial_params if initial_params else dash.no_update
    return dash.no_update
