import time
from datetime import datetime
from dash import Input, Output, callback, State, no_update, callback_context, dcc
from orm.db import db
from utils.log import log
from orm.chart_view_fault_timed import Chart_view_fault_timed
from urllib.parse import urlparse, parse_qs
import pandas as pd
from io import BytesIO

@callback(
    Output('f_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.info(f"[update_url_params] 开始解析URL参数: {search}")
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
    log.info(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

@callback(
    [Output('f_fault-warning-table', 'data'),
     Output('f_fault-warning-table', 'pagination')],
    [Input('f_url-params-store', 'data'),
     Input('f_query_button', 'nClicks'),
     Input('f_fault-warning-table', 'pagination')],
    [State('f_train_no', 'value'),
     State('f_carriage_no', 'value'),
     State('f_fault_type', 'value'),
     State('f_start_time_range', 'value')],
    prevent_initial_call=False
)
def fault_warning_table_callback(url_params, nClicks, pagination, train_no, carriage_no, fault_type, start_time_range):
    log.info(f"[fault_warning_table_callback] 触发源: {callback_context.triggered_id if callback_context.triggered else '初始加载'}")
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    query_train_no = ''
    query_carriage_no = ''
    query_fault_type = ''
    query_start_time_range = None

    if trigger_id == 'url-params-store' and url_params:
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
    with db.atomic():
        data = list(query.order_by(Chart_view_fault_timed.start_time.desc()).offset(
            (pagination['current'] - 1) * pagination['pageSize']
        ).limit(pagination['pageSize']).dicts())

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
    return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize'],'showSizeChanger': pagination['showSizeChanger'],'pageSizeOptions': pagination['pageSizeOptions'],'showQuickJumper': pagination['showQuickJumper']}

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
    
    log.info(f"[sync_url_params_to_form] 函数被触发，收到参数: {url_params}")
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
    log.info(f"[sync_url_params_to_form] 同步到表单: 车号={train_no}, 车厢号={carriage_no}, 类型={fault_type}, 时间范围={start_time_range}")
    return train_no, carriage_no, fault_type, start_time_range

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
    with db.atomic():
        data = list(query.order_by(Chart_view_fault_timed.start_time.desc()).dicts())

    # 格式化数据
    formatted_data = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '故障名称': item['param_name'],
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