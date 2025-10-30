
import heapq
import random
import time
import base64
from datetime import datetime, timedelta
import pytz

from dash import callback, Output, Input, State, callback_context, no_update
from dash import html
from configs import BaseConfig

# 获取项目前缀
prefix = BaseConfig.project_prefix
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


# 生成CO2条形指示器的SVG
def render_co2_indicator_svg(co2_value: float, unit_suffix: str, thresholds=None) -> html.ObjectEl:
    try:
        import base64 as _b64
        thresholds = thresholds or getattr(BaseConfig, 'co2_thresholds', [500, 1000, 1500, 2000, 2500, 3000])
        palette = getattr(BaseConfig, 'co2_colors', {})
        inactive_color = palette.get('inactive', '#1f3a6b')
        if co2_value < 1000:
            active_color = palette.get('low', '#31e6ff')
        elif co2_value < 2000:
            active_color = palette.get('mid', '#3aa0ff')
        elif co2_value < 3000:
            active_color = palette.get('warn', '#faad14')
        else:
            active_color = palette.get('high', '#f5222d')
        label_color = '#ffffff'

        n = len(thresholds)
        max_width = 92
        min_width = 18
        bar_height = 10
        gap = 6
        left_margin = 64
        top = 0
        rects = []
        for i, t in enumerate(thresholds):
            # 视觉从下到上：低阈值在下，高阈值在上
            y = top + (n - 1 - i) * (bar_height + gap)
            # 条长度从下到上逐渐变长
            width = int(min_width + (max_width - min_width) * (i + 1) / n)
            color = active_color if co2_value >= t else inactive_color
            rects.append(
                f'<rect x="{left_margin}" y="{y}" width="{width}" height="{bar_height}" rx="2" fill="{color}" />'
            )

        # 刻度文字从下到上：1000/2000/3000
        labels = []
        for t in (1000, 2000, 3000):
            if t in thresholds:
                i = thresholds.index(t)
                y = top + (n - 1 - i) * (bar_height + gap) + bar_height - 2
                labels.append(f'<text x="{left_margin-6}" y="{y}" text-anchor="end" fill="{label_color}" font-size="12px">{t}ppm</text>')
        bottom_y = top + n * (bar_height + gap) + 18
        labels.append(f'<text x="0" y="{bottom_y}" fill="{label_color}" font-size="12px">CO₂浓度 {int(co2_value)}ppm</text>')

        svg = (
            f'<svg width="140" height="{bottom_y+4}" viewBox="0 0 140 {bottom_y+4}" preserveAspectRatio="xMinYMin meet" '
            f'xmlns="http://www.w3.org/2000/svg">' + ''.join(rects) + ''.join(labels) + '</svg>'
        )
        b64 = _b64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return html.ObjectEl(
            data=f'data:image/svg+xml;base64,{b64}',
            type='image/svg+xml',
            key=f'co2-{unit_suffix}-{int(time.time()*1000)}',
            style={
                'width': '120px',
                'height': 'calc(100% - 40px)',
                'marginTop': '30px',
                'marginRight': '30px',
                'display': 'block',
                'border': 'none',
                'overflow': 'hidden'
            }
        )
    except Exception as e:
        log.error(f"[render_co2_indicator_svg] 生成失败: {e}")
        return html.Div("CO2指示器加载失败")

# 查询按钮点击时更新URL参数
@callback(
    Output('url', 'search', allow_duplicate=True),
    Input('c_query_button', 'nClicks'),
    [State('c_train_no', 'value'),
     State('c_carriage_no', 'value')],
    prevent_initial_call=True
)
def update_url_on_query(nClicks, train_no, carriage_no):
    """查询按钮点击时更新URL参数"""
    if nClicks is None or nClicks == 0:
        return no_update
    
    log.debug(f"[update_url_on_query] 查询按钮点击: train_no={train_no}, carriage_no={carriage_no}")
    
    # 构建URL参数
    params = []
    
    if train_no:
        params.append(f"train_no={train_no}")
    
    if carriage_no:
        params.append(f"carriage_no={carriage_no}")
    
    search = '?' + '&'.join(params) if params else ''
    log.debug(f"[update_url_on_query] 更新URL参数: {search}")
    return search
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
def create_svg_content(param_data, unit_suffix, key_suffix=None):
    """
    根据参数数据创建 SVG 内容
    unit_suffix: 'u1' 或 'u2'，用于区分机组一和机组二
    """
    try:
        # 读取 SVG 文件内容（改用更合适尺寸的 newAC_small.svg）
        with open('assets/imgs/newAC_small.svg', 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # 确保关键 id 存在（兼容无 id 的小尺寸源文件）
        try:
            import re as _re_id
            # 根 svg id：若已有其他 id，直接替换为 ac-unit-svg；若没有 id，则注入
            if 'id="ac-unit-svg"' not in svg_content:
                if _re_id.search(r'<svg[^>]*\sid="[^"]*"', svg_content):
                    svg_content = _re_id.sub(r'(<svg[^>]*\s)id="[^"]*"', r'\1id="ac-unit-svg"', svg_content, count=1)
                else:
                    svg_content = _re_id.sub(r'(<svg[^>]*)(>)', r'\1 id="ac-unit-svg"\2', svg_content, count=1)

            # tspan data-value -> id 映射
            dv_to_id = {
                'fan1-temp': 'fan1-temp-value',
                'fan2-temp': 'fan2-temp-value',
                'sys1-low-pressure': 'sys1-low-pressure-value',
                'sys1-high-pressure': 'sys1-high-pressure-value',
                'sys2-high-pressure': 'sys2-high-pressure-value',
                'sys2-low-pressure': 'sys2-low-pressure-value',
                'fresh-air-temp': 'fresh-air-temp-value',
                'return-air-temp': 'return-air-temp-value',
                'co2-level': 'co2-level-value',
                'humidity-level': 'humidity-level-value',
            }
            for dv, _id in dv_to_id.items():
                # 给对应 tspan 添加缺失的 id（若已有 id 则不处理）
                pattern = rf'(<tspan[^>]*data-value="{_re_id.escape(dv)}"(?![^>]*\sid=)[^>]*)(>)'
                svg_content = _re_id.sub(rf'\1 id="{_id}"\2', svg_content, count=1)

            # 按你的要求：将小图中湿度的 data-value 从 humidity 改为 humidity-level
            svg_content = _re_id.sub(r'data-value="humidity"', 'data-value="humidity-level"', svg_content)

            # 补齐外层 text 的 *-text id，规则：定位包含对应 data-value 的 <text> 节点
            dv_to_text_id = {
                'fan1-temp': 'fan1-temp-text',
                'fan2-temp': 'fan2-temp-text',
                'sys1-low-pressure': 'sys1-low-pressure-text',
                'sys1-high-pressure': 'sys1-high-pressure-text',
                'sys2-high-pressure': 'sys2-high-pressure-text',
                'sys2-low-pressure': 'sys2-low-pressure-text',
                'fresh-air-temp': 'fresh-air-temp-text',
                'return-air-temp': 'return-air-temp-text',
                'co2-level': 'co2-level-text',
                'humidity-level': 'humidity-level-text',
            }
            for dv, txt_id in dv_to_text_id.items():
                # 情况1：已有 id，则改为标准 id（只改含该 data-value 的那个 <text>）
                pattern_has_id = rf'(<text[^>]*\sid=")([^">]*)("[^>]*>)([\s\S]*?data-value="{_re_id.escape(dv)}"[\s\S]*?</text>)'
                svg_content = _re_id.sub(rf'\1{txt_id}\3\4', svg_content, count=1)
                # 情况2：没有 id，则插入 id
                pattern_no_id = rf'(<text(?![^>]*\sid=)[^>]*)(>)(?=[\s\S]*?data-value="{_re_id.escape(dv)}")'
                svg_content = _re_id.sub(rf'\1 id="{txt_id}"\2', svg_content, count=1)
        except Exception:
            pass
        
        # 为不同机组创建不同的 ID
        if unit_suffix == 'u1':
            svg_content = svg_content.replace('id="ac-unit-svg"', 'id="ac-unit-svg-1"')
            svg_content = svg_content.replace('id="fan1-temp-text"', 'id="fan1-temp-text-1"')
            svg_content = svg_content.replace('id="fan2-temp-text"', 'id="fan2-temp-text-1"')
            svg_content = svg_content.replace('id="fan1-temp-value"', 'id="fan1-temp-value-1"')
            svg_content = svg_content.replace('id="fan2-temp-value"', 'id="fan2-temp-value-1"')
            svg_content = svg_content.replace('id="sys1-low-pressure-text"', 'id="sys1-low-pressure-text-1"')
            svg_content = svg_content.replace('id="sys1-high-pressure-text"', 'id="sys1-high-pressure-text-1"')
            svg_content = svg_content.replace('id="sys2-high-pressure-text"', 'id="sys2-high-pressure-text-1"')
            svg_content = svg_content.replace('id="sys2-low-pressure-text"', 'id="sys2-low-pressure-text-1"')
            svg_content = svg_content.replace('id="fresh-air-temp-text"', 'id="fresh-air-temp-text-1"')
            svg_content = svg_content.replace('id="return-air-temp-text"', 'id="return-air-temp-text-1"')
            svg_content = svg_content.replace('id="co2-level-text"', 'id="co2-level-text-1"')
            svg_content = svg_content.replace('id="humidity-level-text"', 'id="humidity-level-text-1"')
            svg_content = svg_content.replace('id="sys1-low-pressure-value"', 'id="sys1-low-pressure-value-1"')
            svg_content = svg_content.replace('id="sys1-high-pressure-value"', 'id="sys1-high-pressure-value-1"')
            svg_content = svg_content.replace('id="sys2-high-pressure-value"', 'id="sys2-high-pressure-value-1"')
            svg_content = svg_content.replace('id="sys2-low-pressure-value"', 'id="sys2-low-pressure-value-1"')
            svg_content = svg_content.replace('id="fresh-air-temp-value"', 'id="fresh-air-temp-value-1"')
            svg_content = svg_content.replace('id="return-air-temp-value"', 'id="return-air-temp-value-1"')
            svg_content = svg_content.replace('id="co2-level-value"', 'id="co2-level-value-1"')
            svg_content = svg_content.replace('id="humidity-level-value"', 'id="humidity-level-value-1"')
        else:  # u2
            svg_content = svg_content.replace('id="ac-unit-svg"', 'id="ac-unit-svg-2"')
            svg_content = svg_content.replace('id="fan1-temp-text"', 'id="fan1-temp-text-2"')
            svg_content = svg_content.replace('id="fan2-temp-text"', 'id="fan2-temp-text-2"')
            svg_content = svg_content.replace('id="fan1-temp-value"', 'id="fan1-temp-value-2"')
            svg_content = svg_content.replace('id="fan2-temp-value"', 'id="fan2-temp-value-2"')
            svg_content = svg_content.replace('id="sys1-low-pressure-text"', 'id="sys1-low-pressure-text-2"')
            svg_content = svg_content.replace('id="sys1-high-pressure-text"', 'id="sys1-high-pressure-text-2"')
            svg_content = svg_content.replace('id="sys2-high-pressure-text"', 'id="sys2-high-pressure-text-2"')
            svg_content = svg_content.replace('id="sys2-low-pressure-text"', 'id="sys2-low-pressure-text-2"')
            svg_content = svg_content.replace('id="fresh-air-temp-text"', 'id="fresh-air-temp-text-2"')
            svg_content = svg_content.replace('id="return-air-temp-text"', 'id="return-air-temp-text-2"')
            svg_content = svg_content.replace('id="co2-level-text"', 'id="co2-level-text-2"')
            svg_content = svg_content.replace('id="humidity-level-text"', 'id="humidity-level-text-2"')
            svg_content = svg_content.replace('id="sys1-low-pressure-value"', 'id="sys1-low-pressure-value-2"')
            svg_content = svg_content.replace('id="sys1-high-pressure-value"', 'id="sys1-high-pressure-value-2"')
            svg_content = svg_content.replace('id="sys2-high-pressure-value"', 'id="sys2-high-pressure-value-2"')
            svg_content = svg_content.replace('id="sys2-low-pressure-value"', 'id="sys2-low-pressure-value-2"')
            svg_content = svg_content.replace('id="fresh-air-temp-value"', 'id="fresh-air-temp-value-2"')
            svg_content = svg_content.replace('id="return-air-temp-value"', 'id="return-air-temp-value-2"')
            svg_content = svg_content.replace('id="co2-level-value"', 'id="co2-level-value-2"')
            svg_content = svg_content.replace('id="humidity-level-value"', 'id="humidity-level-value-2"')
        
        # 在 SVG 中注入脚本：加载与可见时强制启动所有 SMIL 动画
        try:
            import re as _re
            _inject_script = (
                '<script><![CDATA[(function(){\n'
                '  function visible(){\n'
                '    var svg=document.documentElement;\n'
                '    var bb=svg.getBoundingClientRect();\n'
                '    return bb.width>0 && bb.height>0 && document.visibilityState==="visible";\n'
                '  }\n'
                '  function kick(){\n'
                '    var nodes=document.querySelectorAll("animate,animateTransform");\n'
                '    for(var i=0;i<nodes.length;i++){\n'
                '      var el=nodes[i];\n'
                '      var host=el.closest("[data-running-status]");\n'
                '      if(!host || host.getAttribute("data-running-status")!=="on"){continue;}\n'
                '      try{ if(el.beginElement){el.beginElement();} }catch(e){}\n'
                '    }\n'
                '    try{document.documentElement.setCurrentTime(0);}catch(e){}\n'
                '  }\n'
                '  function waitAndKick(n){ if(visible()||n<=0){kick();} else { requestAnimationFrame(function(){waitAndKick(n-1);}); } }\n'
                '  if(document.readyState!=="loading"){waitAndKick(120);}\n'
                '  document.addEventListener("DOMContentLoaded", function(){waitAndKick(120);});\n'
                '  document.addEventListener("visibilitychange", function(){ if(document.visibilityState==="visible"){waitAndKick(60);} });\n'
                '})();]]></script>'
            )
            # 注意：替换串中分组引用必须用 \1（单反斜杠），否则会输出字符“\1”破坏 SVG
            svg_content = _re.sub(r'(<svg[^>]*>)', r"\1" + _inject_script, svg_content, count=1)
        except Exception:
            pass

        # 更新数值
        if param_data:
            # 机组一数据映射
            if unit_suffix == 'u1':
                fan_temp = param_data.get('送风温度_u1', 0)
                sys1_low_pressure = param_data.get('吸气压力_u11', 0)
                sys1_high_pressure = param_data.get('高压压力_u11', 0)
                sys2_high_pressure = param_data.get('高压压力_u12', 0)
                sys2_low_pressure = param_data.get('吸气压力_u12', 0)
                fresh_air_temp = param_data.get('新风温度_u1', 0)
                return_air_temp = param_data.get('回风温度_u1', 0)
                co2_level = param_data.get('co2_u1', 0)
                humidity_level = param_data.get('车厢湿度_1', 0)
            else:  # u2
                fan_temp = param_data.get('送风温度_u2', 0)
                sys1_low_pressure = param_data.get('吸气压力_u21', 0)
                sys1_high_pressure = param_data.get('高压压力_u21', 0)
                sys2_high_pressure = param_data.get('高压压力_u22', 0)
                sys2_low_pressure = param_data.get('吸气压力_u22', 0)
                fresh_air_temp = param_data.get('新风温度_u2', 0)
                return_air_temp = param_data.get('回风温度_u2', 0)
                co2_level = param_data.get('co2_u2', 0)
                humidity_level = param_data.get('车厢湿度_2', 0)
            
            # 添加调试信息
            log.debug(f"[create_svg_content] {unit_suffix} 数据: fan_temp={fan_temp}, sys1_low={sys1_low_pressure}, sys1_high={sys1_high_pressure}, sys2_high={sys2_high_pressure}, sys2_low={sys2_low_pressure}, fresh_air={fresh_air_temp}, return_air={return_air_temp}, co2={co2_level}, humidity={humidity_level}")
            
            # 更新 SVG 中的数值（基于唯一 id 精确替换，避免重复文本替换冲突）
            import re as _re2

            def _replace_tspan_text(svg: str, tspan_id: str, new_text: str) -> str:
                pattern = rf'(\<tspan[^>]*id="{_re2.escape(tspan_id)}"[^>]*\>)([^<]*)(\</tspan\>)'
                return _re2.sub(pattern, lambda m: m.group(1) + new_text + m.group(3), svg, count=1)

            id_suffix = '-1' if unit_suffix == 'u1' else '-2'

            # 风机温度（两个送风值共用同一温度）
            svg_content = _replace_tspan_text(svg_content, f'fan1-temp-value{id_suffix}', f'{fan_temp:.1f}°C')
            svg_content = _replace_tspan_text(svg_content, f'fan2-temp-value{id_suffix}', f'{fan_temp:.1f}°C')

            # 压力值（分别定点替换）
            svg_content = _replace_tspan_text(svg_content, f'sys1-low-pressure-value{id_suffix}', f'{sys1_low_pressure:.2f}Mpa')
            svg_content = _replace_tspan_text(svg_content, f'sys1-high-pressure-value{id_suffix}', f'{sys1_high_pressure:.2f}Mpa')
            svg_content = _replace_tspan_text(svg_content, f'sys2-high-pressure-value{id_suffix}', f'{sys2_high_pressure:.2f}Mpa')
            svg_content = _replace_tspan_text(svg_content, f'sys2-low-pressure-value{id_suffix}', f'{sys2_low_pressure:.2f}Mpa')

            # 新风/回风温度、CO2、湿度
            svg_content = _replace_tspan_text(svg_content, f'fresh-air-temp-value{id_suffix}', f'{fresh_air_temp:.1f}°C')
            svg_content = _replace_tspan_text(svg_content, f'return-air-temp-value{id_suffix}', f'{return_air_temp:.1f}°C')
            svg_content = _replace_tspan_text(svg_content, f'co2-level-value{id_suffix}', f'{co2_level:.0f}ppm')
            svg_content = _replace_tspan_text(svg_content, f'humidity-level-value{id_suffix}', f'{humidity_level:.1f}%')
            
            # 始终显示动画和文字（不管数据是否为0）
            svg_content = svg_content.replace('data-running-status="off"', 'data-running-status="on"')
            # 可见性：统一把隐藏改为可见（属性形式与内联style形式）
            try:
                import re as _re_vis_all
                svg_content = _re_vis_all.sub(r'visibility\s*:\s*hidden', 'visibility: visible', svg_content)
                svg_content = _re_vis_all.sub(r'visibility\s*=\s*"hidden"', 'visibility="visible"', svg_content)
            except Exception:
                svg_content = svg_content.replace('visibility: hidden', 'visibility: visible').replace('visibility="hidden"', 'visibility="visible"')
            # 为箭头路径补充运行标记，允许脚本点火
            try:
                import re as _re_arrow_on
                svg_content = _re_arrow_on.sub(r'(<path[^>]*id="path89[^"]*"(?![^>]*data-running-status)[^>]*)(>)', r'\1 data-running-status="on"\2', svg_content)
            except Exception:
                pass
            # 触发所有动画开始
            svg_content = svg_content.replace('begin="indefinite"', 'begin="0s"')
        else:
            # 无数据时停止动画和隐藏
            svg_content = svg_content.replace('data-running-status="on"', 'data-running-status="off"')
            try:
                import re as _re_vis2
                svg_content = _re_vis2.sub(r'visibility\s*:\s*visible', 'visibility: hidden', svg_content)
                svg_content = _re_vis2.sub(r'visibility\s*=\s*"visible"', 'visibility="hidden"', svg_content)
            except Exception:
                svg_content = svg_content.replace('visibility: visible', 'visibility: hidden').replace('visibility="visible"', 'visibility="hidden"')
            # 箭头路径标记为 off，脚本将不会点火
            try:
                import re as _re_arrow_off
                svg_content = _re_arrow_off.sub(r'(<path[^>]*id="path89[^"]*"[^>]*data-running-status=)"on"', r'\1"off"', svg_content)
                svg_content = _re_arrow_off.sub(r'(<path[^>]*id="path89[^"]*"(?![^>]*data-running-status)[^>]*)(>)', r'\1 data-running-status="off"\2', svg_content)
            except Exception:
                pass
            # 恢复动画begin为indefinite，避免被脚本误触发
            svg_content = svg_content.replace('begin="0s"', 'begin="indefinite"')
        
        # 优化SVG：贴齐左上角，尽量填充容器，减少内边距留白
        import re, base64
        # 强制使用左上对齐
        if 'preserveAspectRatio' in svg_content:
            svg_content = re.sub(r'preserveAspectRatio="[^"]*"', 'preserveAspectRatio="xMinYMin meet"', svg_content, count=1)
        else:
            svg_content = svg_content.replace('<svg ', '<svg preserveAspectRatio="xMinYMin meet" ', 1)
        # 尽量让根节点宽高随容器撑满
        if 'width="' in svg_content:
            svg_content = re.sub(r'width="[^"]*"', 'width="100%"', svg_content, count=1)
        else:
            svg_content = svg_content.replace('<svg ', '<svg width="100%" ', 1)
        if 'height="' in svg_content:
            svg_content = re.sub(r'height="[^"]*"', 'height="100%"', svg_content, count=1)
        else:
            svg_content = svg_content.replace('<svg ', '<svg height="100%" ', 1)

        # 使用 html.ObjectEl 来渲染 SVG（支持动画，无滚动条）
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        
        return html.ObjectEl(
            data=f"data:image/svg+xml;base64,{svg_base64}",
            type="image/svg+xml",
            key=f"svg-{unit_suffix}-{key_suffix or 'static'}",
            style={
                "width": "100%",
                "height": "240px",
                "border": "none",
                "overflow": "hidden",
                "display": "block"  # 消除内联替换元素基线间隙
            }
        )
        
    except Exception as e:
        log.error(f"[create_svg_content] 创建 SVG 内容失败: {e}")
        return html.Div("SVG 加载失败")

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
    [Output('c_i_unit1_supply_temp', 'percent'),
     Output('c_i_unit1_humidity', 'percent'),
     Output('c_i_unit1_car_temp', 'percent'),
     Output('c_i_unit2_supply_temp', 'percent'),
     Output('c_i_unit2_humidity', 'percent'),
     Output('c_i_unit2_car_temp', 'percent'),
     Output('c_i_unit1_current1', 'items'),
     Output('c_i_unit1_current2', 'items'),
     Output('c_i_unit2_current1', 'items'),
     Output('c_i_unit2_current2', 'items'),
     Output('c_unit1-svg-container', 'children'),
     Output('c_unit2-svg-container', 'children'),
     Output('c_unit1-co2-indicator', 'children'),
     Output('c_unit2-co2-indicator', 'children')],
    [Input('l-update-data-interval', 'n_intervals'),
     Input('c_unit-svg-init', 'n_intervals'),
     Input('c_unit-tabs', 'activeKey'),
     Input('c_url-params-store', 'data'),
     Input('c_query_button', 'nClicks'),
     Input('c_train_no', 'value'),
     Input('c_carriage_no', 'value')],
    prevent_initial_call=False
)
def update_unit_info_tables(n_intervals, svg_init_tick, active_key, url_params, n_clicks, train_no_value, carriage_no_value):
    # 使用新的输入参数值
    train_no = train_no_value
    carriage_no = carriage_no_value
    log.debug(f"[update_unit_info_tables] 更新机组信息表格，train_no: {train_no}, carriage_no: {carriage_no}")

    # 如果没有train_no或carriage_no，返回空数据
    if not train_no or not carriage_no:
        log.debug("[update_unit_info_tables] 未提供train_no或carriage_no，返回空数据和默认值")
        # 创建空的 SVG 内容
        svg_key_seed = f"{svg_init_tick}-{active_key or ''}"
        empty_svg1 = create_svg_content(None, 'u1', svg_key_seed)
        empty_svg2 = create_svg_content(None, 'u2', svg_key_seed)
        co2_1 = render_co2_indicator_svg(0, f'u1-{svg_key_seed}')
        co2_2 = render_co2_indicator_svg(0, f'u2-{svg_key_seed}')
        return 0, 0, 0, 0, 0, 0, [{'label': '0','content': '冷凝风机电流-U11'},
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
                                         {'label': '0','content': '通风机电流-U22'}], \
               empty_svg1, empty_svg2, co2_1, co2_2

    # 获取数据
    param_data = get_carriage_param_data(train_no, carriage_no)
    if not param_data:
        log.debug("[update_unit_info_tables] 未找到参数数据，返回空数据和默认值")
        # 创建空的 SVG 内容
        svg_key_seed = f"{svg_init_tick}-{active_key or ''}"
        empty_svg1 = create_svg_content(None, 'u1', svg_key_seed)
        empty_svg2 = create_svg_content(None, 'u2', svg_key_seed)
        co2_1 = render_co2_indicator_svg(0, f'u1-{svg_key_seed}')
        co2_2 = render_co2_indicator_svg(0, f'u2-{svg_key_seed}')
        return 0, 0, 0, 0, 0, 0, [{'label': '0','content': '冷凝风机电流-U11'},
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
                                         {'label': '0','content': '通风机电流-U22'}], \
               empty_svg1, empty_svg2, co2_1, co2_2

    log.debug(f"[update_unit_info_tables] 参数数据: {param_data}")

    # 计算进度条数据（保留用于其他组件）
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

    # 创建 SVG 内容
    # 根据当前激活页签优先重建对应机组，触发首帧
    svg_key_seed = f"{svg_init_tick}-{active_key or ''}"
    svg1 = create_svg_content(param_data, 'u1', svg_key_seed)
    svg2 = create_svg_content(param_data, 'u2', svg_key_seed)
    # 覆盖调试：BaseConfig.co2_debug_u1/u2 不为 None 时使用调试值
    co2_val_u1 = BaseConfig.co2_debug_u1 if BaseConfig.co2_debug_u1 is not None else float(param_data.get('co2_u1', 0) or 0)
    co2_val_u2 = BaseConfig.co2_debug_u2 if BaseConfig.co2_debug_u2 is not None else float(param_data.get('co2_u2', 0) or 0)
    co2_1 = render_co2_indicator_svg(co2_val_u1, f'u1-{svg_key_seed}')
    co2_2 = render_co2_indicator_svg(co2_val_u2, f'u2-{svg_key_seed}')
    
    return unit1_supply_temp, unit1_humidity, unit1_car_temp, unit2_supply_temp, unit2_humidity, unit2_car_temp, unit1_current1_items, unit1_current2_items, unit2_current1_items, unit2_current2_items, svg1, svg2, co2_1, co2_2
