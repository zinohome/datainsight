import logging
import random
from datetime import datetime
from dash import Input, Output, callback, State

from configs import LayoutConfig
from orm.db import db, monitored_connection
from utils.db_query import DBQuery
from utils.log import log as log
from orm.chart_view_fault_timed import Chart_view_fault_timed
from peewee import fn


# 页面数据更新回调
@callback(
    [Output('fault-warning-table', 'data'),
     Output('fault-warning-table', 'pagination')],
    [Input('query_button', 'nClicks')],
    [State('train_no', 'value'),
     State('carriage_no', 'value'),
     State('fault_type', 'value'),
     State('start_time_range', 'value'),
     State('fault-warning-table', 'pagination')],
    prevent_initial_call=False
)
def fault_warning_table_callback(nClicks, train_no, carriage_no, fault_type, start_time_range, pagination):
    # 设置默认分页参数
    pagination = pagination or {'current': 1, 'pageSize': 10}
    formatted_data = []
    total = 0
    # 使用上下文管理器确保连接正确释放
    with monitored_connection():
        query = Chart_view_fault_timed.select()
        # 应用筛选条件
        if train_no:
            query = query.where(Chart_view_fault_timed.dvc_train_no == train_no)
        if carriage_no:
            query = query.where(Chart_view_fault_timed.dvc_carriage_no == carriage_no)
        if fault_type:
            query = query.where(Chart_view_fault_timed.fault_type == fault_type)
        if start_time_range and len(start_time_range) == 2:
            start_time, end_time = start_time_range
            query = query.where(Chart_view_fault_timed.start_time >= start_time, Chart_view_fault_timed.start_time <= end_time)
        elif start_time_range:
            logging.warning(f"Invalid start_time_range format: {start_time_range}")

        # 计算总记录数
        total = query.count()

        # 添加查询超时控制
        with db.atomic():
            # 使用索引优化分页查询
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

    return formatted_data, {'total': total, 'current': pagination['current'], 'pageSize': pagination['pageSize']}