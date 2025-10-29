import heapq
import random
import time

from datetime import datetime, timedelta
import pytz

from dash import callback, Output, Input, State

from configs import BaseConfig
from orm.db import db, log_pool_status, _sentinel
from orm.chart_view_fault_timed import Chart_view_fault_timed
import pandas as pd
from collections import Counter
from utils.log import log as log
from orm.chart_health_equipment import ChartHealthEquipment
from orm.chart_view_train_opstatus import ChartViewTrainOpstatus
from orm.chart_line_fault_type import ChartLineFaultType
from orm.chart_line_health_status_count import ChartLineHealthStatusCount
# 导入共享的动态模型
from utils.dynamic_models import get_dynamic_health_model, get_dynamic_fault_model


prefix = BaseConfig.project_prefix
# 从数据库获取所有故障数据的函数

def get_all_fault_data():
    # 构建查询，获取所有故障类型的数据
    # 使用动态模型
    DynamicFaultModel = get_dynamic_fault_model()
    # 构建查询，获取24小时内所有故障类型的数据
    # 计算24小时前的时间点
    twenty_four_hours_ago = datetime.now(pytz.timezone('Asia/Shanghai')) - timedelta(hours=24)
    query = DynamicFaultModel.select().where((DynamicFaultModel.update_time >= twenty_four_hours_ago) &
                                             (DynamicFaultModel.status == '持续'))
    # 按开始时间降序排序
    query = query.order_by(DynamicFaultModel.start_time.desc())
    
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


# 获取空调状态数据的方法
def get_opstatus_data():
    # 查询空调状态数据
    query = ChartViewTrainOpstatus.select()
    # 按车号排序
    query = query.order_by(ChartViewTrainOpstatus.dvc_train_no)
    
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
def get_fault_type_data():
    # 查询故障类型数据
    query = ChartLineFaultType.select()
    # 按故障类型和车号排序
    query = query.order_by(ChartLineFaultType.故障类型, ChartLineFaultType.dvc_train_no)
    
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
def get_health_status_count_data():
    # 查询健康状态统计数据
    query = ChartLineHealthStatusCount.select()
    # 按车号和健康状态排序
    query = query.order_by(ChartLineHealthStatusCount.dvc_train_no, ChartLineHealthStatusCount.device_health_status)
    
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


# 获取健康数据的方法
def get_health_data():
    # 查询健康数据
    try:
        with db.atomic():  # 添加上下文管理器
            # 使用动态模型
            DynamicHealthModel = get_dynamic_health_model()
            health_query = DynamicHealthModel.select().order_by(
                DynamicHealthModel.耗用率.desc()
            )
            
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
                
                new_formatted_health = [{
                    '车厢': item.车厢,
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
                
                new_formatted_health = [{
                    '车厢': str(item.车厢号),
                    '部件': item.部件,
                    '耗用率': item.耗用率,
                    '操作': {'href': f'/{prefix}/health?train_no={str(item.车号)}&carriage_no={str(item.车厢号)}', 'target': '_self'}
                } for item in health_query]

        # 构建l_h_health_bar数据
        bar_data = []
        
        # 从BaseConfig.health_bar_data_rnd按轮播顺序选择一个数给select_train
        if not hasattr(get_health_data, 'select_index'):
            get_health_data.select_index = 0
        health_bar_data = BaseConfig.health_bar_data_rnd
        select_train = health_bar_data[get_health_data.select_index % len(health_bar_data)] if health_bar_data else None
        get_health_data.select_index += 1

        # 筛选出select_train的车厢数据
        for item in formatted_health:
            if item['车号'] == select_train:
                bar_data.append({
                    'carriage': f"{item['车号']}-{item['车厢号']}",
                    'ratio': round(item['耗用率'] * 100, 2),
                    'param': item['部件'].replace('-', '')
                })
        
        return new_formatted_health, bar_data
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
    [Output('l_w_warning-table', 'data'),
     Output('l_f_fault-table', 'data'),
    #  Output('l_f_fault-wordcloud', 'data'),
    #  Output('l_w_warning-wordcloud', 'data'),
     Output('l_h_health_table', 'data'),
     Output('l_h_health_bar', 'data'),
     Output('l_c_opstatus-table', 'data'),
     Output('l_c_opstatus_online-badge', 'count'),
     Output('l_c_opstatus_maintenance-badge', 'count'),
     Output('l_c_opstatus_offline-badge', 'count'),
     Output('l_c_warning_count', 'end'),
     Output('l_c_alarm_count', 'end'),
     Output('l_c_total_exception_count', 'end'),
     Output('l_c_healthy_count', 'end'),
     Output('l_c_subhealthy_count', 'end'),
     Output('l_c_faulty_count', 'end'),
     Output('l_c_opstatus_normal-pie', 'annotations'),
     Output('l_c_opstatus_l1main-pie', 'annotations'),
     Output('l_c_opstatus_l2main-pie', 'annotations'),
     Output('l_c_opstatus_l3main-pie', 'annotations')
     ],
    Input('l-update-data-interval', 'n_intervals')
)
def update_both_tables(n_intervals):
    """
    更新故障和预警表格数据，只执行一次SQL查询
    :param n_intervals: 定时器触发次数
    :return: 预警数据列表和故障数据列表
    """
    # 连接池状态监控
    status = log_pool_status()  # 记录连接池状态日志

    # 连接池耗尽预警
    if status['utilization'] >= 80:  # 使用率超过80%时触发延迟
        log.warning(f"连接池使用率过高 ({status['utilization']}%)，延迟查询...")
        time.sleep(3)  # 延迟1秒

    all_data = get_all_fault_data()
    
    # 拆分数据为预警和故障
    warning_data = [item for item in all_data if item['fault_type'] == '预警']
    fault_data = [item for item in all_data if item['fault_type'] == '故障']
    
    # 格式化预警数据
    if BaseConfig.use_carriage_field:
        # 使用车厢字段
        formatted_warning = [{
            '车厢': item['msg_calc_dvc_no'],
            '预警部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '维修建议': item['repair_suggestion']
        } for item in warning_data]
        
        # 格式化故障数据
        formatted_fault = [{
            '车厢': item['msg_calc_dvc_no'],
            '故障部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '维修建议': item['repair_suggestion']
        } for item in fault_data]
    else:
        # 使用车厢号字段
        formatted_warning = [{
            '车厢': str(item['dvc_carriage_no']),
            '预警部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '维修建议': item['repair_suggestion']
        } for item in warning_data]
        
        # 格式化故障数据
        formatted_fault = [{
            '车厢': str(item['dvc_carriage_no']),
            '故障部件': item['fault_name'],
            '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
            '维修建议': item['repair_suggestion']
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

    # 调用get_health_data方法获取健康数据
    formatted_health, bar_data = get_health_data()
    
    # 调用get_opstatus_data方法获取空调状态数据
    opstatus_data = get_opstatus_data()

    # 调用get_fault_type_data方法获取故障类型数据
    fault_type_data = get_fault_type_data()

    # 调用get_health_status_count_data方法获取健康状态统计数据
    health_status_count_data = get_health_status_count_data()

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
    
    # 格式化空调状态数据
    formatted_opstatus = []
    
    # 初始化状态计数器
    train_online_num = 0
    train_maintenance_num = 0
    train_offline_num = 0
    
    # 初始化圆环图计数器
    normal_count = 0
    l1main_count = 0
    l2main_count = 0
    l3main_count = 0
    # 获取带时区的当前时间（使用上海时区）
    tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(tz)
    five_minutes_ago = current_time - timedelta(minutes=5)

    for item in opstatus_data:
        latest_time = item['latest_time']
        # 确保latest_time是datetime类型并添加时区信息
        if isinstance(latest_time, str):
            latest_time = datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
        # 仅当latest_time没有时区信息时才添加
        if latest_time and latest_time.tzinfo is None:
            latest_time = tz.localize(latest_time)
        
        if latest_time is None or latest_time < five_minutes_ago:
            status = '离线'
        else:
            if item['latest_op_condition'] == 1:
                status = '库内'
            else:
                status = '在线'
        
        # 根据状态设置对应的status值并更新计数器
        if status == '离线':
            badge_status = 'default'
            train_offline_num += 1
        elif status == '在线':
            badge_status = 'success'
            train_online_num += 1
        elif status == '库内':
            badge_status = 'processing'
            train_maintenance_num += 1
        
        # 添加10个相同的字典数据
        '''
        test_formatted_opstatus=[]
        for _ in range(10):
            test_formatted_opstatus.append({
                '车号': {'status': badge_status, 'text': item['dvc_train_no']},
                '立即维修': item['立即维修'],
                '加强跟踪': item['加强跟踪'],
                '计划维修': item['计划维修'],
                '操作': {'href': f'/{prefix}/train?train_no=' + item['dvc_train_no'], 'target': '_self'}
            })
        formatted_opstatus.extend(test_formatted_opstatus)
        '''
        # 更新圆环图计数器
        normal_count += item['正常运营']
        l3main_count += item['立即维修']
        l1main_count += item['加强跟踪']
        l2main_count += item['计划维修']

        if int(item['dvc_train_no']) <= 1632:
            op_link = {'href': BaseConfig.external_main_status_url, 'target': '_self'}
        else:
            op_link = {'href': f'/{prefix}/train?train_no=' + item['dvc_train_no'], 'target': '_self'}

        formatted_opstatus.append({
            '车号': {'status': badge_status, 'text': item['dvc_train_no']},
            '立即维修': item['立即维修'],
            '加强跟踪': item['加强跟踪'],
            '计划维修': item['计划维修'],
            '操作': op_link
        })
    
    # 转换为DataFrame并返回字典列表
    log.debug(f"fault_wordcloud_data: {fault_wordcloud_data}")
    log.debug(f"warning_wordcloud_data: {warning_wordcloud_data}")
    log.debug(f"bar_data: {bar_data}")
    log.debug(f"opstatus_data: {opstatus_data}")
    # 构建圆环图annotations数据
    normal_annotations = [{
        "type": "text",
        "position": ["50%", "50%"],
        "content": f"正常运营\n{normal_count}",
        "style": {
            "fill": "white",
            "fontSize": 12,
            "textAlign": "center"
        }
    }]
    
    l1main_annotations = [{
        "type": "text",
        "position": ["50%", "50%"],
        "content": f"加强跟踪\n{l1main_count}",
        "style": {
            "fill": "white",
            "fontSize": 12,
            "textAlign": "center"
        }
    }]
    
    l2main_annotations = [{
        "type": "text",
        "position": ["50%", "50%"],
        "content": f"计划维修\n{l2main_count}",
        "style": {
            "fill": "white",
            "fontSize": 12,
            "textAlign": "center"
        }
    }]
    
    l3main_annotations = [{
        "type": "text",
        "position": ["50%", "50%"],
        "content": f"立即维修\n{l3main_count}",
        "autoAdjust": True,
        "style": {
            "fill": "white",
            "fontSize": 12,
            "textAlign": "center",
            "whiteSpace": "pre"
        }
    }]
    
    return (
        pd.DataFrame(formatted_warning).to_dict('records'),
        pd.DataFrame(formatted_fault).to_dict('records'),
        # fault_wordcloud_data,
        # warning_wordcloud_data,
        pd.DataFrame(formatted_health).to_dict('records'),
        bar_data,
        pd.DataFrame(formatted_opstatus).to_dict('records'),
        train_online_num,
        train_maintenance_num,
        train_offline_num,
        warning_count,
        alarm_count,
        total_exception_count,
        healthy_count,
        subhealthy_count,
        faulty_count,
        normal_annotations,
        l1main_annotations,
        l2main_annotations,
        l3main_annotations
    )
