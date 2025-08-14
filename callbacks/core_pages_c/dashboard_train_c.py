import random

from dash import callback, Output, Input, State

from configs import BaseConfig
from orm.db import db
from orm.chart_view_fault_timed import Chart_view_fault_timed
import pandas as pd
from collections import Counter
from utils.log import log as log
from orm.chart_health_equipment import ChartHealthEquipment


# 从数据库获取所有故障数据的函数

def get_all_fault_data():
    # 构建查询，获取所有故障类型的数据
    query = Chart_view_fault_timed.select()
    # 按开始时间降序排序
    query = query.order_by(Chart_view_fault_timed.start_time.desc())

    # 执行查询并获取数据
    with db.atomic():
        #data = query.dicts()
        data = list(query.dicts())

    return data


# 合并更新故障和预警表格数据及词云的回调函数
@callback(
    [Output('t_w_warning-table', 'data'),
     Output('t_f_fault-table', 'data'),
     Output('t_f_fault-wordcloud', 'data'),
     Output('t_w_warning-wordcloud', 'data'),
     Output('t_h_health_table', 'data'),
     Output('t_h_health_bar', 'data')
     ],
    Input('l-update-data-interval', 'n_intervals')
)
def update_both_tables(n_intervals):
    """
    更新故障和预警表格数据，只执行一次SQL查询
    :param n_intervals: 定时器触发次数
    :return: 预警数据列表和故障数据列表
    """
    all_data = get_all_fault_data()

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

    # 统计故障部件词频用于词云
    if fault_data:
        # 提取所有故障部件名称
        param_names = [item['param_name'] for item in fault_data]
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
        warning_param_names = [item['param_name'] for item in warning_data]
        # 计算词频
        warning_counter = Counter(warning_param_names)
        # 格式化词云数据
        warning_wordcloud_data = [{
            'word': name,
            'value': random.randint(10, 100) ** 3 * count
        } for name, count in warning_counter.items()]
    else:
        warning_wordcloud_data = []

    # 查询健康数据
    with db.atomic():  # 添加上下文管理器
        health_query = ChartHealthEquipment.select().order_by(
            ChartHealthEquipment.车号,
            ChartHealthEquipment.车厢号,
            ChartHealthEquipment.耗用率.desc()
        )
        # 立即加载所有数据
        formatted_health = [{
            '车号': item.车号,
            '车厢号': item.车厢号,
            '部件': item.部件,
            '耗用率': item.耗用率,
            '额定寿命': item.额定寿命,
            '已耗': item.已耗
        } for item in health_query]

    # 构建t_h_health_bar数据
    bar_data = []

    # 从BaseConfig.health_bar_data_rnd按轮播顺序选择一个数给select_train
    if not hasattr(update_both_tables, 'select_index'):
        update_both_tables.select_index = 0
    health_bar_data = BaseConfig.health_bar_data_rnd
    select_train = health_bar_data[update_both_tables.select_index % len(health_bar_data)] if health_bar_data else None
    update_both_tables.select_index += 1

    # 筛选出select_train的车厢数据
    for item in formatted_health:
        if item['车号'] == select_train:
            bar_data.append({
                'carriage': f"{item['车号']}-{item['车厢号']}",
                'ratio': round(item['耗用率'] * 100, 2),
                'param': item['部件'].replace('-', '')
            })

    # 转换为DataFrame并返回字典列表
    log.info(f"fault_wordcloud_data: {fault_wordcloud_data}")
    log.info(f"warning_wordcloud_data: {warning_wordcloud_data}")
    log.info(f"bar_data: {bar_data}")
    return (
        pd.DataFrame(formatted_warning).to_dict('records'),
        pd.DataFrame(formatted_fault).to_dict('records'),
        fault_wordcloud_data,
        warning_wordcloud_data,
        pd.DataFrame(formatted_health).to_dict('records'),
        bar_data
    )