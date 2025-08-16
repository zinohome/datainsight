# 添加 _sentinel 类定义
class _sentinel:
    def __lt__(self, other):
        return True


import heapq
import random
import time
from datetime import datetime, timedelta
import pytz

from dash import callback, Output, Input, State, callback_context
from configs import BaseConfig
from orm.db import db, log_pool_status
from orm.chart_view_fault_timed import Chart_view_fault_timed
import pandas as pd
from collections import Counter
from utils.log import log as log
from orm.chart_health_equipment import ChartHealthEquipment
from configs.layout_config import LayoutConfig
from views.core_pages.train_chart_info import create_train_chart_info


# 解析URL参数回调
@callback(
    Output('c_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.debug(f"[update_url_params] 开始解析URL参数: {search}")
    parsed_train = ''
    parsed_carriage = ''

    if search:
        try:
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
            parsed_carriage = params.get('carriage_no', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train,
        'carriage_no': parsed_carriage
    }

    log.debug(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

# 同步URL参数到表单回调
@callback(
    [Output('c_train_no', 'value'),
     Output('c_carriage_no', 'value')],
    [Input('c_url-params-store', 'modified_timestamp')],
    [State('c_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    time.sleep(0.5)  # 等待前端元素加载
    log.debug(f"[sync_url_params_to_form] 同步URL参数到表单: {url_params}")
    if not isinstance(url_params, dict):
        return None, None

    train_no = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    return train_no, carriage_no

# 更新车厢图链接回调
@callback(
    Output('carriage-chart-info-container', 'children'),
    [Input('c_train_no', 'value')],
    [State('theme-mode-store', 'data')]
)
def update_carriage_chart_info(train_no, theme_mode):
    log.debug(f"[update_carriage_chart_info] 更新列车图链接，train_no: {train_no}")
    themetoken = LayoutConfig.dashboard_theme
    # 创建新的列车图链接
    return create_train_chart_info(themetoken, 'param', train_no)
    """
    根据车号和车厢号更新列车图链接
    :param train_no: 车号
    :param theme_mode: 主题模式
    :return: 更新后的列车图链接组件
    """
    log.debug(f"[update_carriage_chart_link] 更新列车图链接，train_no: {train_no}")
    themetoken = LayoutConfig.dashboard_theme
    # 创建新的列车图链接
    return create_train_chart_link(themetoken, 'param', train_no)

# 从数据库获取所有故障数据的函数

def get_all_fault_data(train_no=None, carriage_no=None):
    # 构建查询，获取所有故障类型的数据
    query = Chart_view_fault_timed.select()
    # 按开始时间降序排序
    query = query.order_by(Chart_view_fault_timed.start_time.desc())

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(Chart_view_fault_timed.dvc_train_no == train_no)

    # 如果提供了carriage_no，添加筛选条件
    if carriage_no:
        query = query.where(Chart_view_fault_timed.dvc_carriage_no == carriage_no)

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.dicts())
            return data
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


# 合并更新故障和预警表格数据的回调函数
@callback(
    [Output('c_w_warning-table', 'data'),
     Output('c_f_fault-table', 'data'),
     ],
    [Input('l-update-data-interval', 'n_intervals'),
     Input('c_url-params-store', 'data'),
     Input('c_query_button', 'nClicks')],
    [State('c_train_no', 'value'),
     State('c_carriage_no', 'value')]
)
def update_both_tables(n_intervals, url_params, n_clicks, train_no, carriage_no):
    """
    更新故障和预警表格数据，只执行一次SQL查询
    :param n_intervals: 定时器触发次数
    :param url_params: URL参数存储
    :param n_clicks: 查询按钮点击次数
    :param train_no: 表单中的车号值
    :param carriage_no: 表单中的车厢号值
    :return: 预警数据列表和故障数据列表
    """
    # 连接池状态监控
    status = log_pool_status()  # 记录连接池状态日志

    # 连接池耗尽预警
    if status['utilization'] >= 80:  # 使用率超过80%时触发延迟
        log.warning(f"连接池使用率过高 ({status['utilization']}%)，延迟查询...")
        time.sleep(3)  # 延迟1秒

    # 确定要使用的train_no和carriage_no值（优先使用表单中的值，其次是URL参数中的值）
    selected_train_no = train_no
    selected_carriage_no = carriage_no
    if not selected_train_no and isinstance(url_params, dict):
        selected_train_no = url_params.get('train_no')
    if not selected_carriage_no and isinstance(url_params, dict):
        selected_carriage_no = url_params.get('carriage_no')
    log.debug(f"[update_both_tables] 使用的train_no: {selected_train_no}, carriage_no: {selected_carriage_no}")

    # 如果没有train_no或carriage_no，则返回空数据
    if not selected_train_no or not selected_carriage_no:
        log.debug("[update_both_tables] 未提供train_no或carriage_no，返回空数据")
        return [], []

    all_data = get_all_fault_data(selected_train_no, selected_carriage_no)

    # 拆分数据为预警和故障
    warning_data = [item for item in all_data if item['fault_type'] == '预警']
    fault_data = [item for item in all_data if item['fault_type'] == '故障']

    # 格式化预警数据
    formatted_warning = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '预警部件': item['param_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else ''
    } for item in warning_data]

    # 格式化故障数据
    formatted_fault = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '故障部件': item['param_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else ''
    } for item in fault_data]

    return (
        pd.DataFrame(formatted_warning).to_dict('records'),
        pd.DataFrame(formatted_fault).to_dict('records')
    )