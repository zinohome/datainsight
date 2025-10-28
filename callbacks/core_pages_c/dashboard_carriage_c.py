
import heapq
import random
import time
from datetime import datetime, timedelta
import pytz

from dash import callback, Output, Input, State, callback_context
from configs import BaseConfig
from orm.db import db, log_pool_status, _sentinel
from orm.chart_view_fault_timed import Chart_view_fault_timed
import pandas as pd
from collections import Counter
from utils.log import log as log
from orm.chart_health_equipment import ChartHealthEquipment
from configs.layout_config import LayoutConfig
from views.core_pages.train_chart_info import create_train_chart_info
from orm.chart_carriage_base import ChartCarriageBase
from orm.chart_carriage_param import ChartCarriageParam
from orm.chart_carriage_param_current import ChartCarriageParamCurrent


prefix = BaseConfig.project_prefix
# 解析URL参数回调
@callback(
    Output('c_url-params-store', 'data'),
    Input('url', 'search'),
    State('c_url-params-store', 'data'),
    prevent_initial_call=False
)
def update_url_params(search, current_data):
    log.debug(f"[update_url_params] 开始解析URL参数: {search}")
    
    # 如果search为空，保持当前数据不变
    if not search:
        return current_data or {'train_no': None, 'carriage_no': None}
    
    try:
        from urllib.parse import urlparse, parse_qs
        params = parse_qs(search.lstrip('?'))
        
        # 获取新参数
        new_train = params.get('train_no', [''])[0]
        new_carriage = params.get('carriage_no', [''])[0]
        
        # 如果参数没有实际变化，保持当前数据
        if (current_data and 
            current_data.get('train_no') == new_train and 
            current_data.get('carriage_no') == new_carriage):
            return current_data
            
        return {
            'train_no': new_train,
            'carriage_no': new_carriage
        }
    except Exception as e:
        log.error(f"[update_url_params] 解析URL参数错误: {e}")
        return current_data or {'train_no': None, 'carriage_no': None}

@callback(
    Output('param-link', 'href'),
    Input('c_url-params-store', 'data')
)
def update_param_link(url_params):
    if not url_params:
        return f"/{BaseConfig.project_prefix}/param"
    train_no = url_params.get('train_no', '')
    carriage_no = url_params.get('carriage_no', '')
    return f"/{BaseConfig.project_prefix}/param?train_no={train_no}&carriage_no={carriage_no}"


# 同步URL参数到表单回调
@callback(
    [Output('c_train_no', 'value'),
     Output('c_carriage_no', 'value')],
    [Input('c_url-params-store', 'modified_timestamp')],
    [State('c_url-params-store', 'data')],
    prevent_initial_call=True
)
def sync_url_params_to_form(modified_timestamp, url_params):
    # time.sleep(0.5)  # 等待前端元素加载
    log.debug(f"[sync_url_params_to_form] 同步URL参数到表单: {url_params}")
    if not isinstance(url_params, dict):
        return None, None

    train_no = url_params.get('train_no') or None
    carriage_no = url_params.get('carriage_no') or None
    # 添加参数验证
    if train_no is not None:
        train_no = str(train_no).strip()
    if carriage_no is not None:
        carriage_no = str(carriage_no).strip()
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
    return create_train_chart_info(themetoken, 'carriage', train_no)
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
    twenty_four_hours_ago = datetime.now(pytz.timezone('Asia/Shanghai')) - timedelta(hours=24)
    # 构建查询，获取所有故障类型的数据
    query = Chart_view_fault_timed.select().where((Chart_view_fault_timed.update_time >= twenty_four_hours_ago) & 
                                                  (Chart_view_fault_timed.status == '持续'))
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
        '预警部件': item['fault_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
        '操作': {'href': f'/{prefix}/fault?train_no={str(item["dvc_train_no"])}&carriage_no={str(item["dvc_carriage_no"])}&fault_type=预警', 'target': '_self'}
    } for item in warning_data]

    # 格式化故障数据
    formatted_fault = [{
        '车号': item['dvc_train_no'],
        '车厢号': item['dvc_carriage_no'],
        '故障部件': item['fault_name'],
        '开始时间': item['start_time'].strftime('%Y-%m-%d %H:%M:%S') if item['start_time'] else '',
        '操作': {'href': f'/{prefix}/fault?train_no={str(item["dvc_train_no"])}&carriage_no={str(item["dvc_carriage_no"])}&fault_type=故障', 'target': '_self'}
    } for item in fault_data]

    return (
        pd.DataFrame(formatted_warning).to_dict('records'),
        pd.DataFrame(formatted_fault).to_dict('records')
    )

# 获取车厢基础数据的函数
def get_carriage_base_data(train_no=None):
    # 构建查询
    query = ChartCarriageBase.select()

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartCarriageBase.dvc_train_no == train_no)
    else:
        return {}

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.dicts())
            # 按车厢号分组
            result = {}
            for item in data:
                carriage_no = item['dvc_carriage_no']
                # 保存原始运行模式值用于颜色映射
                original_mode = item['运行模式']
                
                # 运行模式映射
                mode_map = {
                    '0': '停机',
                    '1': '通风',
                    '2': '强冷',
                    '3': '弱冷',
                    '6': '紧急通风',
                    '7': '预冷'
                }
                # 确保运行模式是整数后再转为字符串
                mode_str = str(original_mode)
                
                item['运行模式'] = mode_map.get(mode_str, '未定义')
                item['original_mode'] = original_mode
                result[carriage_no] = item
            return result
    finally:
        # 强制将当前连接放回连接池
        try:
            conn = db.connection()
            key = db.conn_key(conn)
            with db._pool_lock:
                if key in db._in_use:
                    pool_conn = db._in_use.pop(key)
                    heapq.heappush(db._connections, (pool_conn.timestamp, _sentinel(), conn))
                    log.debug(f"显式放回连接 {key} 到连接池")
        except Exception as e:
            log.warning(f"显式释放连接失败: {str(e)}")


# 获取车厢参数数据的函数
def get_carriage_param_data(train_no=None, carriage_no=None):
    # 构建查询
    query = ChartCarriageParam.select()

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartCarriageParam.dvc_train_no == train_no)
    else:
        return None

    # 如果提供了carriage_no，添加筛选条件
    if carriage_no:
        query = query.where(ChartCarriageParam.dvc_carriage_no == carriage_no)

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.dicts())
            if data:
                return data[0]  # 返回第一条记录
            return None
    finally:
        # 强制将当前连接放回连接池
        try:
            conn = db.connection()
            key = db.conn_key(conn)
            with db._pool_lock:
                if key in db._in_use:
                    pool_conn = db._in_use.pop(key)
                    heapq.heappush(db._connections, (pool_conn.timestamp, _sentinel(), conn))
                    log.debug(f"显式放回连接 {key} 到连接池")
        except Exception as e:
            log.warning(f"显式释放连接失败: {str(e)}")


# 更新六个车厢信息表格的回调函数
@callback(
    [Output('c_i_info_table1', 'data'),
     Output('c_i_info_table2', 'data'),
     Output('c_i_info_table3', 'data'),
     Output('c_i_info_table4', 'data'),
     Output('c_i_info_table5', 'data'),
     Output('c_i_info_table6', 'data')],
    [Input('l-update-data-interval', 'n_intervals'),
     Input('c_url-params-store', 'data'),
     Input('c_query_button', 'nClicks')],
    [State('c_train_no', 'value')]
)
def update_carriage_info_tables(n_intervals, url_params, n_clicks, train_no):
    log.debug(f"[update_carriage_info_tables] 更新车厢信息表格，train_no: {train_no}")

    # 如果train_no不存在，全部返回空数组
    if not train_no:
        return [], [], [], [], [], []

    # 获取数据
    carriage_data = get_carriage_base_data(train_no)
    log.debug(f"[update_carriage_info_tables] 车厢数据: {carriage_data}")

    # 运行模式颜色映射
    mode_color_map = {
        '0': 'red',        # 停机
        '1': 'gray',       # 通风
        '2': 'blue',       # 强冷
        '3': 'lightblue',  # 弱冷
        '6': 'yellow',     # 紧急通风
        '7': 'green'       # 预冷
    }

    # 准备六个表格的数据
    table_data = []
    for i in range(1, 7):
        if i in carriage_data:
            item = carriage_data[i]
            # 使用原始运行模式值进行颜色映射
            mode_str = str(item['original_mode'])
            mode_text = item['运行模式']  # 直接使用已经转换好的中文文本
            mode_color = mode_color_map.get(mode_str, 'default')

            # 提取需要的字段并格式化为标签
            formatted_data = [{
                '运行模式': {'tag': mode_text, 'color': mode_color},
                '目标温度': {'tag': f"{item['目标温度']:.1f}°C" if item['目标温度'] is not None else "无数据", 'color': 'cyan'},
                '新风温度': {'tag': f"{item['新风温度']:.1f}°C" if item['新风温度'] is not None else "无数据", 'color': 'cyan'},
                '回风温度': {'tag': f"{item['回风温度']:.1f}°C" if item['回风温度'] is not None else "无数据", 'color': 'cyan'}
            }]
            table_data.append(formatted_data)
        else:
            table_data.append([])

    return tuple(table_data)


# 获取车厢当前参数数据的函数
def get_carriage_param_current_data(train_no=None, carriage_no=None, unit=None):
    # 构建查询
    query = ChartCarriageParamCurrent.select()

    # 如果提供了train_no，添加筛选条件
    if train_no:
        query = query.where(ChartCarriageParamCurrent.dvc_train_no == train_no)
    else:
        return []

    # 如果提供了carriage_no，添加筛选条件
    if carriage_no:
        query = query.where(ChartCarriageParamCurrent.dvc_carriage_no == carriage_no)

    # 如果提供了unit，添加筛选条件
    if unit:
        # 构建参数名称的like查询，例如'%U11%'
        query = query.where(ChartCarriageParamCurrent.param_name.contains(unit))

    # 执行查询并获取数据
    try:
        with db.atomic():
            data = list(query.dicts())
            return data
    finally:
        # 强制将当前连接放回连接池
        try:
            conn = db.connection()
            key = db.conn_key(conn)
            with db._pool_lock:
                if key in db._in_use:
                    pool_conn = db._in_use.pop(key)
                    heapq.heappush(db._connections, (pool_conn.timestamp, _sentinel(), conn))
                    log.debug(f"显式放回连接 {key} 到连接池")
        except Exception as e:
            log.warning(f"显式释放连接失败: {str(e)}")

# 更新机组信息表格的回调函数
@callback(
    [Output('c_i_info_unit1-table', 'data'),
     Output('c_i_info_unit2-table', 'data'),
     Output('c_i_unit1_supply_temp', 'percent'),
     Output('c_i_unit1_humidity', 'percent'),
     Output('c_i_unit1_car_temp', 'percent'),
     Output('c_i_unit2_supply_temp', 'percent'),
     Output('c_i_unit2_humidity', 'percent'),
     Output('c_i_unit2_car_temp', 'percent'),
     Output('c_i_unit1_current1', 'items'),
     Output('c_i_unit1_current2', 'items'),
     Output('c_i_unit2_current1', 'items'),
     Output('c_i_unit2_current2', 'items')],
    [Input('l-update-data-interval', 'n_intervals'),
     Input('c_url-params-store', 'data'),
     Input('c_query_button', 'nClicks'),
     Input('c_train_no', 'value'),
     Input('c_carriage_no', 'value')],
    prevent_initial_call=False
)
def update_unit_info_tables(n_intervals, url_params, n_clicks, train_no_value, carriage_no_value):
    # 使用新的输入参数值
    train_no = train_no_value
    carriage_no = carriage_no_value
    log.debug(f"[update_unit_info_tables] 更新机组信息表格，train_no: {train_no}, carriage_no: {carriage_no}")

    # 如果没有train_no或carriage_no，返回空数据
    if not train_no or not carriage_no:
        log.debug("[update_unit_info_tables] 未提供train_no或carriage_no，返回空数据和默认值")
        return [], [], 0, 0, 0, 0, 0, 0,[{'label': '0','content': '冷凝风机电流-U11'},
                                         {'label': '0','content': '压缩机电流-U11'},
                                         {'label': '0','content': '通风机电流-U11'}], \
               [{'label': '0','content': '冷凝风机电流-U12'},
                                         {'label': '0','content': '压缩机电流-U12'},
                                         {'label': '0','content': '通风机电流-U12'}], \
               [{'label': '0','content': '冷凝风机电流-U21'},
                                         {'label': '0','content': '压缩机电流-U21'},
                                         {'label': '0','content': '通风机电流-U21'}], \
               [{'label': '0','content': '冷凝风机电流-U22'},
                                         {'label': '0','content': '压缩机电流-U22'},
                                         {'label': '0','content': '通风机电流-U22'}]

    # 获取数据
    param_data = get_carriage_param_data(train_no, carriage_no)
    if not param_data:
        log.debug("[update_unit_info_tables] 未找到参数数据，返回空数据和默认值")
        return [], [], 0, 0, 0, 0, 0, 0,[{'label': '0','content': '冷凝风机电流-U11'},
                                         {'label': '0','content': '压缩机电流-U11'},
                                         {'label': '0','content': '通风机电流-U11'}], \
               [{'label': '0','content': '冷凝风机电流-U12'},
                                         {'label': '0','content': '压缩机电流-U12'},
                                         {'label': '0','content': '通风机电流-U12'}], \
               [{'label': '0','content': '冷凝风机电流-U21'},
                                         {'label': '0','content': '压缩机电流-U21'},
                                         {'label': '0','content': '通风机电流-U21'}], \
               [{'label': '0','content': '冷凝风机电流-U22'},
                                         {'label': '0','content': '压缩机电流-U22'},
                                         {'label': '0','content': '通风机电流-U22'}]

    log.debug(f"[update_unit_info_tables] 参数数据: {param_data}")

    # 格式化机组1表格数据
    unit1_data = [{
        'pressure1': {'tag': f"{param_data.get('吸气压力_u11', 0):.2f} MPa", 'color': 'cyan'},
        'pressure2': {'tag': f"{param_data.get('吸气压力_u12', 0):.2f} MPa", 'color': 'cyan'},
        'highPressure1': {'tag': f"{param_data.get('高压压力_u11', 0):.2f} MPa", 'color': 'cyan'},
        'highPressure2': {'tag': f"{param_data.get('高压压力_u12', 0):.2f} MPa", 'color': 'cyan'},
        'temp1': {'tag': f"{param_data.get('新风温度_u1', 0):.1f}°C", 'color': 'cyan'},
        'temp2': {'tag': f"{param_data.get('回风温度_u1', 0):.1f}°C", 'color': 'cyan'},
        'temp3': {'tag': f"{param_data.get('送风温度_u1', 0):.1f}°C", 'color': 'cyan'},
        'co2': {'tag': f"{param_data.get('co2_u1', 0):.0f} ppm", 'color': 'cyan'},
        'carTemp': {'tag': f"{param_data.get('车厢温度_1', 0):.1f}°C", 'color': 'cyan'},
        'humidity': {'tag': f"{param_data.get('车厢湿度_1', 0):.1f}%", 'color': 'cyan'}
    }]

    # 格式化机组2表格数据
    unit2_data = [{
        'pressure1': {'tag': f"{param_data.get('吸气压力_u21', 0):.2f} MPa", 'color': 'cyan'},
        'pressure2': {'tag': f"{param_data.get('吸气压力_u22', 0):.2f} MPa", 'color': 'cyan'},
        'highPressure1': {'tag': f"{param_data.get('高压压力_u21', 0):.2f} MPa", 'color': 'cyan'},
        'highPressure2': {'tag': f"{param_data.get('高压压力_u22', 0):.2f} MPa", 'color': 'cyan'},
        'temp1': {'tag': f"{param_data.get('新风温度_u2', 0):.1f}°C", 'color': 'cyan'},
        'temp2': {'tag': f"{param_data.get('回风温度_u2', 0):.1f}°C", 'color': 'cyan'},
        'temp3': {'tag': f"{param_data.get('送风温度_u2', 0):.1f}°C", 'color': 'cyan'},
        'co2': {'tag': f"{param_data.get('co2_u2', 0):.0f} ppm", 'color': 'cyan'},
        'carTemp': {'tag': f"{param_data.get('车厢温度_2', 0):.1f}°C", 'color': 'cyan'},
        'humidity': {'tag': f"{param_data.get('车厢湿度_2', 0):.1f}%", 'color': 'cyan'}
    }]
    # 计算各参数的百分比值（除以100并保留三位小数）
    unit1_supply_temp = float(f"{param_data.get('送风温度_u1', 0):.1f}")
    unit1_humidity = float(f"{param_data.get('车厢湿度_1', 0):.1f}")
    unit1_car_temp = float(f"{param_data.get('车厢温度_1', 0):.1f}")
    unit2_supply_temp = float(f"{param_data.get('送风温度_u2', 0):.1f}")
    unit2_humidity = float(f"{param_data.get('车厢湿度_2', 0):.1f}")
    unit2_car_temp = float(f"{param_data.get('车厢温度_2', 0):.1f}")

    # 获取各机组电流数据
    unit1_current1_data = get_carriage_param_current_data(train_no, carriage_no, 'U11')
    unit1_current2_data = get_carriage_param_current_data(train_no, carriage_no, 'U12')
    unit2_current1_data = get_carriage_param_current_data(train_no, carriage_no, 'U21')
    unit2_current2_data = get_carriage_param_current_data(train_no, carriage_no, 'U22')

    # 格式化电流数据为items结构
    def format_current_items(data, unit):
        # 创建参数名称到标签的映射
        param_map = {
            '冷凝风机电流': '冷凝风机电流-{}'.format(unit),
            '压缩机电流': '压缩机电流-{}'.format(unit),
            '通风机电流': '通风机电流-{}'.format(unit)
        }

        # 初始化结果字典
        result = {
            '冷凝风机电流-{}'.format(unit): {'label': '0', 'content': '冷凝风机电流-{}'.format(unit)},
            '压缩机电流-{}'.format(unit): {'label': '0', 'content': '压缩机电流-{}'.format(unit)},
            '通风机电流-{}'.format(unit): {'label': '0', 'content': '通风机电流-{}'.format(unit)}
        }

        # 填充数据
        for item in data:
            param_name = item.get('param_name', '')
            for key, value in param_map.items():
                if key in param_name:
                    result[value] = {'label': str(item.get('param_value', 0)), 'content': value}
                    break

        # 转换为列表并保持顺序
        return [
            result['冷凝风机电流-{}'.format(unit)],
            result['压缩机电流-{}'.format(unit)],
            result['通风机电流-{}'.format(unit)]
        ]

    # 格式化各机组电流数据
    unit1_current1_items = format_current_items(unit1_current1_data, 'U11')
    unit1_current2_items = format_current_items(unit1_current2_data, 'U12')
    unit2_current1_items = format_current_items(unit2_current1_data, 'U21')
    unit2_current2_items = format_current_items(unit2_current2_data, 'U22')

    return unit1_data, unit2_data, unit1_supply_temp, unit1_humidity, unit1_car_temp, unit2_supply_temp, unit2_humidity, unit2_car_temp, unit1_current1_items, unit1_current2_items, unit2_current1_items, unit2_current2_items
