import time
from datetime import datetime
from dash import Input, Output, callback, State, callback_context
from orm.chart_view_param import Chart_view_param
from orm.db import db
from utils.log import log

# 解析URL参数回调
@callback(
    Output('p_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.info(f"[update_url_params] 开始解析URL参数: {search}")
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
    log.info(f"[update_url_params] URL参数解析完成，存储结果: {result}")
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
    log.info(f"[update_dashboard_data] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    # 确定查询参数
    query_train_no = ''
    query_carriage_no = ''
    query_components = []
    query_start_time = None
    query_end_time = None

    # 处理URL参数
    if trigger_id == 'p_url-params-store' and url_params:
        query_train_no = url_params.get('train_no', '')
        query_carriage_no = url_params.get('carriage_no', '')
        query_components = url_params.get('component', '').split(',') if url_params.get('component') else []
        # 处理时间范围
        start_time = url_params.get('start_time')
        end_time = url_params.get('end_time')
        if start_time and end_time:
            try:
                query_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                query_end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                log.warning(f"[update_dashboard_data] URL时间格式转换错误: {e}")
    # 处理查询按钮
    elif trigger_id == 'p_query_button' and nClicks > 0:
        query_train_no = train_no or ''
        query_carriage_no = carriage_no or ''
        query_components = component or []
        if start_time_range and len(start_time_range) == 2:
            try:
                query_start_time = datetime.strptime(start_time_range[0], '%Y-%m-%d %H:%M:%S')
                query_end_time = datetime.strptime(start_time_range[1], '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                log.warning(f"[update_dashboard_data] 表单时间格式转换错误: {e}")
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
    query = Chart_view_param.select()
    if query_train_no:
        query = query.where(Chart_view_param.dvc_train_no == query_train_no)
    if query_carriage_no:
        query = query.where(Chart_view_param.dvc_carriage_no == query_carriage_no)
    if query_components:
        query = query.where(Chart_view_param.param_name.in_(query_components))
    if query_start_time and query_end_time:
        query = query.where(Chart_view_param.time_minute.between(query_start_time, query_end_time))

    # 执行查询
    try:
        with db.atomic():
            data = query.order_by(Chart_view_param.time_minute).dicts()

        # 格式化数据为折线图所需格式
        formatted_data = [{
            'time_minute': item['time_minute'].strftime('%Y-%m-%d %H:%M:%S'),
            'avg_value': item['avg_value'],
            'param_name': item['param_name']
        } for item in data]

        log.info(f"[update_dashboard_data] 查询完成，返回 {len(formatted_data)} 条记录")
        return formatted_data
    except Exception as e:
        log.error(f"[update_dashboard_data] 查询错误: {e}")
        return []

# 同步URL参数到表单回调
@callback(
    [Output('p_train_no', 'value'),
     Output('p_carriage_no', 'value'),
     Output('p_component', 'value'),
     Output('p_start_time_range', 'value')],
    [Input('p_url-params-store', 'modified_timestamp')],
    [State('p_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    time.sleep(0.5)  # 等待前端元素加载
    log.info(f"[sync_url_params_to_form] 同步URL参数到表单: {url_params}")
    if not isinstance(url_params, dict):
        return None, None, None, []

    train_no = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    component = url_params.get('component', '').split(',') if url_params.get('component') else None
    start_time = url_params.get('start_time')
    end_time = url_params.get('end_time')
    start_time_range = [start_time, end_time] if start_time and end_time else []

    return train_no, carriage_no, component, start_time_range