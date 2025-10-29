
import heapq
import random
import time
from datetime import datetime, timedelta
import pytz

from dash import callback, Output, Input, State, callback_context, no_update
from configs import BaseConfig
from orm.db import db, log_pool_status, _sentinel

prefix = BaseConfig.project_prefix
from orm.chart_view_fault_timed import Chart_view_fault_timed
import pandas as pd
from collections import Counter
from utils.log import log as log
from orm.chart_health_equipment import ChartHealthEquipment
from orm.chart_view_train_opstatus import ChartViewTrainOpstatus
from orm.chart_line_fault_type import ChartLineFaultType
from orm.chart_line_fault_param_type import ChartLineFaultParamType
from orm.chart_line_health_status_count import ChartLineHealthStatusCount
# 导入共享的动态模型
from utils.dynamic_models import get_dynamic_health_model, get_dynamic_fault_model
from dash import dcc
from views.core_pages.train_chart_link import create_train_chart_link
from configs.layout_config import LayoutConfig


# 查询按钮点击时更新URL参数
@callback(
    Output('url', 'search', allow_duplicate=True),
    Input('t_query_button', 'nClicks'),
    [State('t_train_no', 'value')],
    prevent_initial_call=True
)
def update_url_on_query(nClicks, train_no):
    """查询按钮点击时更新URL参数"""
    if nClicks is None or nClicks == 0:
        return no_update
    
    log.debug(f"[update_url_on_query] 查询按钮点击: train_no={train_no}")
    
    # 构建URL参数
    params = []
    
    if train_no:
        params.append(f"train_no={train_no}")
    
    search = '?' + '&'.join(params) if params else ''
    log.debug(f"[update_url_on_query] 更新URL参数: {search}")
    return search

# 解析URL参数回调
@callback(
    Output('t_url-params-store', 'data'),
    Input('url', 'search'),
    prevent_initial_call=False
)
def update_url_params(search):
    log.debug(f"[update_url_params] 开始解析URL参数: {search}")
    parsed_train = ''

    if search:
        try:
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(search.lstrip('?'))
            parsed_train = params.get('train_no', [''])[0]
        except Exception as e:
            log.error(f"[update_url_params] 解析URL参数错误: {e}")

    result = {
        'train_no': parsed_train
    }

    # log.debug(f"[update_url_params] URL参数解析完成，存储结果: {result}")
    return result

# 同步URL参数到表单回调
@callback(
    Output('t_train_no', 'value'),
    [Input('t_url-params-store', 'modified_timestamp')],
    [State('t_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    time.sleep(0.5)  # 等待前端元素加载
    # log.debug(f"[sync_url_params_to_form] 同步URL参数到表单: {url_params}")
    if not isinstance(url_params, dict):
        return None

    train_no = url_params.get('train_no') or None
    return train_no


# 获取空调状态数据的方法
def get_opstatus_data(train_no=None):
    # 查询空调状态数据
    query = ChartViewTrainOpstatus.select()
    # 按车号排序
    query = query.order_by(ChartViewTrainOpstatus.dvc_train_no)
    
    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartViewTrainOpstatus.dvc_train_no == train_no)
    
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


# 获取故障类型数据的方法
def get_fault_type_data(train_no=None):
    # 查询故障类型数据
    query = ChartLineFaultType.select()
    # 按故障类型和车号排序
    query = query.order_by(ChartLineFaultType.故障类型, ChartLineFaultType.dvc_train_no)
    
    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartLineFaultType.dvc_train_no == train_no)
    
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


# 获取故障类型数据的方法
def get_fault_type_param_data(train_no=None):
    # 查询故障类型数据
    query = ChartLineFaultParamType.select()
    # 按故障类型和车号排序
    query = query.order_by(ChartLineFaultParamType.dvc_train_no, ChartLineFaultParamType.故障数量)

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartLineFaultParamType.dvc_train_no == train_no)
    
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


# 获取健康状态统计数据的方法
def get_health_status_count_data(train_no=None):
    # 查询健康状态统计数据
    query = ChartLineHealthStatusCount.select()
    # 按车号和健康状态排序
    query = query.order_by(ChartLineHealthStatusCount.dvc_train_no, ChartLineHealthStatusCount.device_health_status)
    
    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartLineHealthStatusCount.dvc_train_no == train_no)
    
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


# 从数据库获取所有故障数据的函数

def get_health_data(train_no=None):
    # 查询健康数据
    try:
        with db.atomic():  # 添加上下文管理器
            # 使用动态模型
            DynamicHealthModel = get_dynamic_health_model()
            
            # 根据配置选择正确的排序字段
            if BaseConfig.use_carriage_field:
                # 使用车厢字段排序
                health_query = DynamicHealthModel.select().order_by(
                    DynamicHealthModel.车号,
                    DynamicHealthModel.车厢,
                    DynamicHealthModel.耗用率.desc()
                )
            else:
                # 使用车厢号字段排序
                health_query = DynamicHealthModel.select().order_by(
                    DynamicHealthModel.车号,
                    DynamicHealthModel.车厢号,
                    DynamicHealthModel.耗用率.desc()
            )

            # 如果提供了train_no，添加筛选条件
            if train_no:
                health_query = health_query.where(DynamicHealthModel.车号 == train_no)

            # 根据配置选择车厢字段
            if BaseConfig.use_carriage_field:
                # 使用车厢字段
                formatted_health = [{
                    '车号': item.车号,
                    '车厢号': item.车厢,  # 使用车厢字段作为车厢号
                    '部件': item.部件,
                    '耗用率': item.耗用率,
                    '操作': {'href': f'/{prefix}/health?train_no={str(item.车号)}&carriage_no={str(item.车厢)}', 'target': '_self'}
                } for item in health_query]
            else:
                # 使用车厢号字段
                formatted_health = [{
                    '车号': item.车号,
                    '车厢号': item.车厢号,
                    '部件': item.部件,
                    '耗用率': item.耗用率,
                    '操作': {'href': f'/{prefix}/health?train_no={str(item.车号)}&carriage_no={str(item.车厢号)}', 'target': '_self'}
                } for item in health_query]

        # 构建t_h_health_bar数据
        bar_data = []

        # 从BaseConfig.health_bar_data_rnd按轮播顺序选择一个数给select_train
        if not hasattr(get_health_data, 'select_index'):
            get_health_data.select_index = 0
        health_bar_data = BaseConfig.health_bar_data_rnd
        select_train = health_bar_data[get_health_data.select_index % len(health_bar_data)] if health_bar_data else None
        get_health_data.select_index += 1

        # 如果提供了train_no，使用它作为select_train
        if train_no:
            select_train = train_no

        # 筛选出select_train的车厢数据
        for item in formatted_health:
            if item['车号'] == select_train:
                bar_data.append({
                    'carriage': f"{item['车号']}-{item['车厢号']}",
                    'ratio': round(item['耗用率'] * 100, 2),
                    'param': item['部件'].replace('-', '')
                })

        return formatted_health, bar_data
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


def get_all_fault_data(train_no=None):
    # 构建查询，获取所有故障类型的数据
    # 使用动态模型
    DynamicFaultModel = get_dynamic_fault_model()
    # 构建查询，获取24小时内所有故障类型的数据
    # 计算24小时前的时间点
    twenty_four_hours_ago = datetime.now(pytz.timezone('Asia/Shanghai')) - timedelta(hours=24)
    # query = DynamicFaultModel.select().where((DynamicFaultModel.update_time >= twenty_four_hours_ago) & 
    #                                               (DynamicFaultModel.status == '持续'))
    query = DynamicFaultModel.select().where((DynamicFaultModel.status == '持续'))
    # 按开始时间降序排序
    query = query.order_by(DynamicFaultModel.start_time.desc())

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(DynamicFaultModel.dvc_train_no == train_no)

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


# 合并更新故障和预警表格数据及词云的回调函数
@callback(
    [Output('t_w_warning-table', 'data'),
     Output('t_f_fault-table', 'data'),
    #  Output('t_f_fault-wordcloud', 'data'),
    #  Output('t_w_warning-wordcloud', 'data'),
     Output('t_h_health_table', 'data'),
    #  Output('t_h_health_bar', 'data'),
     Output('t_c_warning_count', 'end'),
     Output('t_c_alarm_count', 'end'),
     Output('t_c_total_exception_count', 'end'),
     Output('t_c_healthy_count', 'end'),
     Output('t_c_subhealthy_count', 'end'),
     Output('t_c_faulty_count', 'end'),
     Output('fault_type_param_data', 'data')
     ],
    [Input('l-update-data-interval', 'n_intervals'),
     Input('t_url-params-store', 'data'),
     Input('t_query_button', 'nClicks')],
    [State('t_train_no', 'value')]
)
def update_both_tables(n_intervals, url_params, n_clicks, train_no):
    """
    更新故障和预警表格数据，只执行一次SQL查询
    :param n_intervals: 定时器触发次数
    :param url_params: URL参数存储
    :param n_clicks: 查询按钮点击次数
    :param train_no: 表单中的车号值
    :return: 预警数据列表和故障数据列表
    """
    # 连接池状态监控
    status = log_pool_status()  # 记录连接池状态日志

    # 连接池耗尽预警
    if status['utilization'] >= 80:  # 使用率超过80%时触发延迟
        log.warning(f"连接池使用率过高 ({status['utilization']}%)，延迟查询...")
        time.sleep(3)  # 延迟1秒

    # 确定要使用的train_no值（优先使用表单中的值，其次是URL参数中的值）
    selected_train_no = train_no
    if not selected_train_no and isinstance(url_params, dict):
        selected_train_no = url_params.get('train_no')
    log.debug(f"[update_both_tables] 使用的train_no: {selected_train_no}")

    # 如果没有train_no，则返回空数据
    if not selected_train_no:
        log.debug("[update_both_tables] 未提供train_no，返回空数据")
        return (
            [],  # 预警表格数据
            [],  # 故障表格数据
            [],  # 健康表格数据
            0,   # 预警数量
            0,   # 告警数量
            0,   # 总异常数量
            0,   # 健康期空调数量
            0,   # 亚健康期空调数量
            0,   # 故障期空调数量
            []   # 故障部件统计
        )

    all_data = get_all_fault_data(selected_train_no)

    # 拆分数据为预警和故障
    warning_data = [item for item in all_data if item['fault_type'] == '预警']
    fault_data = [item for item in all_data if item['fault_type'] == '故障']

    # 格式化预警数据
    if BaseConfig.use_carriage_field:
        # 使用车厢字段
        formatted_warning = [{
            '车号': item['dvc_train_no'],
            '车厢号': item['msg_calc_dvc_no'],  # 使用车厢字段作为车厢号
            '预警部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '操作': {'href': f'/{prefix}/fault?train_no=' + str(item['dvc_train_no'])+'&carriage_no='+str(item['msg_calc_dvc_no'])+'&fault_type=预警', 'target': '_self'}
        } for item in warning_data]

        # 格式化故障数据
        formatted_fault = [{
            '车号': item['dvc_train_no'],
            '车厢号': item['msg_calc_dvc_no'],  # 使用车厢字段作为车厢号
            '故障部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '操作': {'href': f'/{prefix}/fault?train_no=' + str(item['dvc_train_no'])+'&carriage_no='+str(item['msg_calc_dvc_no'])+'&fault_type=故障', 'target': '_self'}
        } for item in fault_data]
    else:
        # 使用车厢号字段
        formatted_warning = [{
            '车号': item['dvc_train_no'],
            '车厢号': item['dvc_carriage_no'],
            '预警部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '操作': {'href': f'/{prefix}/fault?train_no=' + str(item['dvc_train_no'])+'&carriage_no='+str(item['dvc_carriage_no'])+'&fault_type=预警', 'target': '_self'}
        } for item in warning_data]

    # 格式化故障数据
    formatted_fault = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '故障部件': item['fault_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
        '操作': {'href': f'/{prefix}/fault?train_no=' + str(item['dvc_train_no'])+'&carriage_no='+str(item['dvc_carriage_no'])+'&fault_type=故障', 'target': '_self'}
    } for item in fault_data]

    # 统计故障部件词频用于词云
    if fault_data:
        # 提取所有故障部件名称
        param_names = [item['fault_name'] for item in fault_data]
        # 计算词频
        param_counter = Counter(param_names)
        # 格式化词云数据
        fault_wordcloud_data = [{
            'word': name,
            'value': random.randint(10, 100) ** 3 * count
        } for name, count in param_counter.items()]
    else:
        fault_wordcloud_data = []

    # 统计预警部件词频用于词云
    if warning_data:
        # 提取所有预警部件名称
        warning_param_names = [item['fault_name'] for item in warning_data]
        # 计算词频
        warning_counter = Counter(warning_param_names)
        # 格式化词云数据
        warning_wordcloud_data = [{
            'word': name,
            'value': random.randint(10, 100) ** 3 * count
        } for name, count in warning_counter.items()]
    else:
        warning_wordcloud_data = []

    # 调用独立的健康数据查询函数
    formatted_health, bar_data = get_health_data(selected_train_no)

    # 调用get_opstatus_data方法获取空调状态数据
    # opstatus_data = get_opstatus_data(selected_train_no)

    # 调用get_fault_type_data方法获取故障类型数据
    fault_type_data = get_fault_type_data(selected_train_no)

    fault_type_param_data_rows = get_fault_type_param_data(selected_train_no)

    fault_type_param_data = [{"name": r["故障部件"], "value": r["故障数量"]} for r in fault_type_param_data_rows]

    # 调用get_health_status_count_data方法获取健康状态统计数据
    health_status_count_data = get_health_status_count_data(selected_train_no)

    # 计算预警数量
    warning_count = sum(item['故障数量'] for item in fault_type_data if item['故障类型'] == '预警')

    # 计算告警数量
    alarm_count = sum(item['故障数量'] for item in fault_type_data if item['故障类型'] == '故障')

    # 计算总异常数量
    total_exception_count = sum(item['故障数量'] for item in fault_type_data)

    # 计算健康期空调数量
    healthy_count = sum(item['device_count'] for item in health_status_count_data if item['device_health_status'] == '健康')

    # 计算亚健康期空调数量
    subhealthy_count = sum(item['device_count'] for item in health_status_count_data if item['device_health_status'] == '亚健康')

    # 计算故障期空调数量
    faulty_count = sum(item['device_count'] for item in health_status_count_data if item['device_health_status'] == '非健康')


    # 转换为DataFrame并返回字典列表
    # log.debug(f"fault_wordcloud_data: {fault_wordcloud_data}")
    # log.debug(f"warning_wordcloud_data: {warning_wordcloud_data}")
    # log.debug(f"bar_data: {bar_data}")
    return (
        pd.DataFrame(formatted_warning).to_dict('records'),
        pd.DataFrame(formatted_fault).to_dict('records'),
        # fault_wordcloud_data,
        # warning_wordcloud_data,
        pd.DataFrame(formatted_health).to_dict('records'),
        # bar_data,
        warning_count,
        alarm_count,
        total_exception_count,
        healthy_count,
        subhealthy_count,
        faulty_count,
        fault_type_param_data
    )


# 更新列车图链接回调
@callback(
    Output('train-chart-link-container', 'children'),
    [Input('t_train_no', 'value')],
    [State('theme-mode-store', 'data')]
)
def update_train_chart_link(train_no, theme_mode):
    """
    根据车号更新列车图链接
    :param train_no: 车号
    :param theme_mode: 主题模式
    :return: 更新后的列车图链接组件
    """
    log.debug(f"[update_train_chart_link] 更新列车图链接，train_no: {train_no}")
    themetoken = LayoutConfig.dashboard_theme
    # 创建新的列车图链接
    return create_train_chart_link(themetoken, 'carriage', train_no)
