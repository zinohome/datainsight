import random
from datetime import datetime
from dash import html, dcc
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    blank_card,
    index_card,
    simple_chart_card,
)
from components.macdacard import macda_card
from configs import BaseConfig
from .train_chart import create_train_chart


def render(themetoken):
    """数据大屏-折线图页面主内容渲染"""
    l_c_opstatus_table_colnames = ['车号', '立即维修', '加强跟踪', '计划维修', '操作']
    l_f_fault_table_colnames = ['车号', '车厢号', '故障部件', '开始时间', '操作']
    l_w_warning_table_colnames = ['车号', '车厢号', '预警部件', '开始时间', '操作']
    l_h_health_table_colnames = ['车号', '车厢号', '部件', '耗用率', '操作']
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="l-update-data-interval",
            interval=BaseConfig.line_update_data_interval,  # 示例，每10秒更新一次
        ),
        # 添加主题模式存储 - 初始设为深色
        dcc.Store(id="theme-mode-store", data="dark"),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 展示列车图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        children=fac.AntdSpace(
                            [
                                # 地铁列车图 - 六节车厢（图片拼接版）
                                create_train_chart(themetoken)
                            ],
                            style={"width": "100%", "display": "flex", "justifyContent": "center",
                                   "alignItems": "center", "padding": "5px"}
                        )
                    ),
                    span=24,
                ),
                # 当前空调状态区域 - 左侧单列，视觉上跨两行
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="当前空调状态",
                        description=html.A(
                            "一期空调状态",
                            href=BaseConfig.external_main_status_url,
                            target=BaseConfig.external_link_target,
                            style={
                                # "color": themetoken["colorText"],  # 继承原文本颜色
                                "textDecoration": "none"  # 可选：移除下划线
                            }
                        ),
                        chart=fac.AntdRow(
                            [
                                # 空调状态统计
                                fac.AntdCol(
                                    blank_card(
                                        rootStyle={
                                            "background": themetoken["colorBgCard"]},
                                        children=fac.AntdRow(
                                            [
                                                # 圆环图1-正常运营
                                                fac.AntdCol(
                                                    fact.AntdPie(
                                                        id="l_c_opstatus_normal-pie",
                                                        data=[{"value": 100}],
                                                        angleField="value",
                                                        radius=0.9,  # 外半径设为0.9
                                                        innerRadius=0.8,
                                                        pieStyle={'stroke': 'transparent', 'lineWidth': 0},  # 移除边框
                                                        color="#22c55e",
                                                        tooltip=False,
                                                        statistic=False,
                                                        label=False,
                                                        annotations=[{
                                                            "type": "text",
                                                            "position": ["50%", "50%"],
                                                            "content": f"正常运营\n{0}",
                                                            "style": {
                                                                "fill": "white",
                                                                "fontSize": 12,
                                                                "textAlign": "center"
                                                            }
                                                        }]
                                                    ),
                                                    span=6,
                                                    style={"display": "flex",
                                                           "justifyContent": "center",
                                                           "alignItems": "flex-start",
                                                           "padding": "5px 10px 0",
                                                           "height": "100%"}
                                                ),
                                                # 圆环图2-加强跟踪
                                                fac.AntdCol(
                                                    fact.AntdPie(
                                                        id="l_c_opstatus_l1main-pie",
                                                        data=[{"value": 100}],
                                                        angleField="value",
                                                        radius=0.9,  # 外半径设为0.9
                                                        innerRadius=0.8,
                                                        pieStyle={'stroke': 'transparent', 'lineWidth': 0},  # 移除边框
                                                        color="#eab308",
                                                        tooltip=False,
                                                        statistic=False,
                                                        label=False,
                                                        annotations=[{
                                                            "type": "text",
                                                            "position": ["50%", "50%"],
                                                            "content": f"加强跟踪\n{0}",
                                                            "style": {
                                                                "fill": "white",
                                                                "fontSize": 12,
                                                                "textAlign": "center"
                                                            }
                                                        }]
                                                    ),
                                                    span=6,
                                                    style={"display": "flex",
                                                           "justifyContent": "center",
                                                           "alignItems": "flex-start",
                                                           "padding": "5px 10px 0",
                                                           "height": "100%"}
                                                ),
                                                # 圆环图3-计划维修
                                                fac.AntdCol(
                                                    fact.AntdPie(
                                                        id="l_c_opstatus_l2main-pie",
                                                        data=[{"value": 100}],
                                                        angleField="value",
                                                        radius=0.9,  # 外半径设为0.9
                                                        innerRadius=0.8,
                                                        pieStyle={'stroke': 'transparent', 'lineWidth': 0},  # 移除边框
                                                        color="#f97316",
                                                        tooltip=False,
                                                        statistic=False,
                                                        label=False,
                                                        annotations=[{
                                                            "type": "text",
                                                            "position": ["50%", "50%"],
                                                            "content": f"计划维修\n{0}",
                                                            "style": {
                                                                "fill": "white",
                                                                "fontSize": 12,
                                                                "textAlign": "center"
                                                            }
                                                        }]
                                                    ),
                                                    span=6,
                                                    style={"display": "flex",
                                                           "justifyContent": "center",
                                                           "alignItems": "flex-start",
                                                           "padding": "5px 10px 0",
                                                           "height": "100%"}
                                                ),
                                                # 圆环图4-立即维修
                                                fac.AntdCol(
                                                    fact.AntdPie(
                                                        id="l_c_opstatus_l3main-pie",
                                                        data=[{"value": 100}],
                                                        angleField="value",
                                                        radius=0.9,  # 外半径设为0.9
                                                        innerRadius=0.8,
                                                        pieStyle={'stroke': 'transparent', 'lineWidth': 0},  # 移除边框
                                                        color="#ef4444",
                                                        tooltip=False,
                                                        statistic=False,
                                                        label=False,
                                                        annotations=[{
                                                            "type": "text",
                                                            "position": ["50%", "50%"],
                                                            "content": f"立即维修\n{0}",
                                                            "autoAdjust": True,
                                                            "style": {
                                                                "fill": "white",
                                                                "fontSize": 12,
                                                                "textAlign": "center",
                                                                "whiteSpace": "pre"
                                                            }
                                                        }]
                                                    ),
                                                    span=6,
                                                    style={"display": "flex",
                                                           "justifyContent": "center",
                                                           "alignItems": "flex-start",
                                                           "padding": "5px 10px 0",
                                                           "height": "100%"}
                                                )
                                            ],
                                            style={"height": "100px",
                                                   "alignItems": "flex-start",
                                                   "margin": 0,
                                                   "padding": 0}
                                        ),
                                    ),
                                    span=24,
                                ),
                                # 空调状态表
                                fac.AntdCol(
                                    blank_card(
                                        rootStyle={
                                            "background": themetoken["colorBgCard"]},
                                        children=fac.AntdRow(
                                            [
                                                fac.AntdCol(
                                                    [
                                                        fac.AntdSpace(
                                                            [
                                                                fac.AntdBadge(
                                                                    id='l_c_opstatus_online-badge',
                                                                    color='green',
                                                                    status='success',
                                                                    count=0,
                                                                    showZero=True
                                                                ),
                                                                fac.AntdText(
                                                                    '在线', style={'fontSize': '12px'}),
                                                                fac.AntdBadge(
                                                                    id='l_c_opstatus_maintenance-badge',
                                                                    color='blue',
                                                                    status='processing',
                                                                    count=0,
                                                                    showZero=True
                                                                ),
                                                                fac.AntdText(
                                                                    '库内', style={'fontSize': '12px'}),
                                                                fac.AntdBadge(
                                                                    id='l_c_opstatus_offline-badge',
                                                                    color='gray',
                                                                    status='default',
                                                                    count=0,
                                                                    showZero=True
                                                                ),
                                                                fac.AntdText(
                                                                    '离线', style={'fontSize': '12px'}),
                                                            ],
                                                            size=20,
                                                        ),
                                                        fac.AntdSpin(
                                                            fac.AntdTable(
                                                                id='l_c_opstatus-table',
                                                                columns=[
                                                                    {
                                                                        'title': column,
                                                                        'dataIndex': column,
                                                                        'width': '{:.2f}%'.format(100 / len(l_c_opstatus_table_colnames)),
                                                                        'headerCellStyle': {
                                                                            'fontWeight': 'bold',
                                                                            'border': 'none',
                                                                            'borderBottom': '1px solid #e8e8e8',
                                                                            'color': themetoken["colorText"],
                                                                            'backgroundColor': 'transparent'
                                                                        },
                                                                        'cellStyle': {
                                                                            'borderRight': 'none',
                                                                            'borderBottom': '1px solid #e8e8e8',
                                                                            'color': themetoken["colorText"],
                                                                            'backgroundColor': 'transparent'
                                                                        },
                                                                        **({
                                                                            'renderOptions': {
                                                                                'renderType': 'status-badge'
                                                                            }
                                                                        } if column == '车号' else {
                                                                            'renderOptions': {
                                                                                'renderType': 'link',
                                                                                'renderLinkText': '详情'
                                                                            }
                                                                        } if column == '操作' else {})
                                                                    }
                                                                    for column in l_c_opstatus_table_colnames
                                                                ],
                                                                size='small',
                                                                pagination=True,
                                                                bordered=False,
                                                                maxHeight=240,
                                                                mode='server-side',
                                                                className="fault-table",
                                                                style={
                                                                    'height': '100%',
                                                                    'width': '100%',
                                                                    'border': 'none',
                                                                    'border-collapse': 'collapse',
                                                                    'border-spacing': '0',
                                                                    'backgroundColor': 'transparent'
                                                                },
                                                            ),
                                                            text='',
                                                        )
                                                    ],
                                                    span=24
                                                )
                                            ],
                                            style={"height": "240px",
                                                   "alignItems": "flex-start",
                                                   "margin": 0,
                                                   "padding": 0}
                                        ),
                                    ),
                                    span=24,
                                ),
                                # 空调数量统计
                                fac.AntdCol(
                                    blank_card(
                                        rootStyle={
                                            "background": themetoken["colorBgCard"]},
                                        children=fac.AntdRow(
                                            [
                                                fac.AntdCol(
                                                    fac.AntdDivider(
                                                        '今日预警/报警空调数量', innerTextOrientation='left'),
                                                    span=24,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='预警数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_warning_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#f97316',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='告警数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_alarm_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#ef4444',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='总异常数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_total_exception_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#ef4444',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='健康期空调数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_healthy_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#22c55e',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='亚健康期空调数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_subhealthy_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#f97316',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                                fac.AntdCol(
                                                    fac.AntdStatistic(
                                                        title='故障期空调数量',
                                                        value=fuc.FefferyCountUp(
                                                            id='l_c_faulty_count',
                                                            end=0, duration=3),
                                                        valueStyle={
                                                            'color': '#ef4444',
                                                            'fontSize': '28px',
                                                            'fontWeight': 'bold',
                                                        },
                                                    ),
                                                    span=8,
                                                ),
                                            ],
                                            style={"height": "60px",
                                                "alignItems": "flex-start",
                                                "margin": 0,
                                                "padding": 0}
                                        ),
                                    ),
                                    span=24,
                                style={"marginTop": "180px"},
                                ),
                            ],
                            style={"height": "120px",
                                   "alignItems": "flex-start",
                                   "margin": 0,
                                   "padding": 0}
                        ),
                    ),
                    span=6,
                ),
                # 右侧图表容器 - 宽度18列，包含6个图表，分两行三列排列
                fac.AntdCol(
                    fac.AntdRow(
                        [
                            # 故障告警图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={
                                        "background": themetoken["colorBgCard"]},
                                    titleStyle={
                                        "color": themetoken["colorText"]},
                                    descriptionStyle={
                                        "color": themetoken["colorText"]},
                                    title="故障告警",
                                    description=html.A(
                                        "一期故障",
                                        href=BaseConfig.external_main_fault_url,
                                        target=BaseConfig.external_link_target,
                                        style={
                                            # "color": themetoken["colorText"],  # 继承原文本颜色
                                            "textDecoration": "none"  # 可选：移除下划线
                                        }
                                    ),
                                    chart=fac.AntdSpin(
                                        fac.AntdTable(
                                            id='l_f_fault-table',
                                            columns=[
                                                {
                                                    'title': column,
                                                    'dataIndex': column,
                                                    'width': '{:.2f}%'.format(100 / len(l_f_fault_table_colnames)),
                                                    'headerCellStyle': {
                                                        'fontWeight': 'bold',
                                                        'border': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    'cellStyle': {
                                                        'borderRight': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    **({
                                                        'renderOptions': {
                                                        'renderType': 'link',
                                                            'renderLinkText': '详情'
                                                        }
                                                    } if column == '操作' else {})
                                                }
                                                for column in l_f_fault_table_colnames
                                            ],
                                            size='small',
                                            pagination=True,
                                            bordered=False,
                                            maxHeight=400,
                                            mode='server-side',
                                            className="fault-table",
                                            style={
                                                'height': '100%',
                                                'width': '100%',
                                                'border': 'none',
                                                'border-collapse': 'collapse',
                                                'border-spacing': '0',
                                                'backgroundColor': 'transparent'
                                            },
                                        ),
                                        text='',
                                    ),
                                    height=400,
                                ),
                                span=8,
                            ),
                            # 状态预警图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="状态预警",
                                    description=html.A(
                                        "一期预警",
                                        href=BaseConfig.external_main_predict_url,
                                        target=BaseConfig.external_link_target,
                                        style={
                                            # "color": themetoken["colorText"],  # 继承原文本颜色
                                            "textDecoration": "none"  # 可选：移除下划线
                                        }
                                    ),
                                    chart=fac.AntdSpin(
                                        fac.AntdTable(
                                            id='l_w_warning-table',
                                            columns=[
                                                {
                                                    'title': column,
                                                    'dataIndex': column,
                                                    'width': '{:.2f}%'.format(100 / len(l_w_warning_table_colnames)),
                                                    'headerCellStyle': {
                                                        'fontWeight': 'bold',
                                                        'border': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    'cellStyle': {
                                                        'borderRight': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    **({
                                                        'renderOptions': {
                                                        'renderType': 'link',
                                                            'renderLinkText': '详情'
                                                        }
                                                    } if column == '操作' else {})
                                                }
                                                for column in l_w_warning_table_colnames
                                            ],
                                            size='small',
                                            pagination=True,
                                            bordered=False,
                                            maxHeight=400,
                                            mode='server-side',
                                            className="fault-table",
                                            style={
                                                'height': '100%',
                                                'width': '100%',
                                                'border': 'none',
                                                'border-collapse': 'collapse',
                                                'border-spacing': '0',
                                                'backgroundColor': 'transparent'
                                            },
                                        ),
                                        text='',
                                    ),
                                    height=400,
                                ),
                                span=8,
                            ),
                            # 寿命预测图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="寿命预测",
                                    description=html.A(
                                        "一期寿命",
                                        href=BaseConfig.external_main_health_url,
                                        target=BaseConfig.external_link_target,
                                        style={
                                            # "color": themetoken["colorText"],  # 继承原文本颜色
                                            "textDecoration": "none"  # 可选：移除下划线
                                        }
                                    ),
                                    chart=fac.AntdSpin(
                                        fac.AntdTable(
                                            id='l_h_health_table',
                                            columns=[
                                                {
                                                    'title': column,
                                                    'dataIndex': column,
                                                    'width': '{:.2f}%'.format(100 / len(l_h_health_table_colnames)),
                                                    'headerCellStyle': {
                                                        'fontWeight': 'bold',
                                                        'border': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    'cellStyle': {
                                                        'borderRight': 'none',
                                                        'borderBottom': '1px solid #e8e8e8',
                                                        'color': themetoken["colorText"],
                                                        'backgroundColor': 'transparent'
                                                    },
                                                    **({'renderOptions': {
                                                        'renderType': 'mini-progress',
                                                        'progressOneHundredPercentColor': '#f08c00',
                                                    }} if column == '耗用率' else {
                                                        'renderOptions': {
                                                            'renderType': 'link',
                                                            'renderLinkText': '详情'
                                                        }
                                                    } if column == '操作' else {})                                                    
                                                }
                                                for column in l_h_health_table_colnames
                                            ],
                                            size='small',
                                            pagination=True,
                                            bordered=False,
                                            maxHeight=280,
                                            mode='server-side',
                                            className="fault-table",
                                            style={
                                                'height': '100%',
                                                'width': '100%',
                                                'border': 'none',
                                                'border-collapse': 'collapse',
                                                'border-spacing': '0',
                                                'backgroundColor': 'transparent'
                                            },
                                        ),
                                        text='',
                                    ),
                                    height=400,
                                ),
                                span=8,
                            ),
                            # 典型故障图表
                            fac.AntdCol(
                                blank_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    children=fac.AntdRow(
                                        [
                                            fact.AntdWordCloud(
                                                id="l_f_fault-wordcloud",
                                                wordField="word",
                                                weightField="value",
                                                height=220,
                                                colorField='word',
                                                wordStyle={'fontSize': [12, 36]},
                                            ),
                                        ],
                                        style={"height": "220px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0}
                                    ),
                                ),
                                span=8,
                            ),
                            # 典型预警图表
                            fac.AntdCol(
                                blank_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    children=fac.AntdRow(
                                        [
                                            fact.AntdWordCloud(
                                                id="l_w_warning-wordcloud",
                                                wordField="word",
                                                weightField="value",
                                                height=220,
                                                colorField='word',
                                                wordStyle={'fontSize': [12, 36]},
                                            ),
                                        ],
                                        style={"height": "220px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0}
                                    ),
                                ),
                                span=8,
                            ),
                            # 部件寿命图表
                            fac.AntdCol(
                                blank_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    children=fac.AntdRow(
                                        [
                                            fact.AntdBar(
                                                id='l_h_health_bar',
                                                data=[
                                                    {
                                                        'carriage': f'12101-{i}',
                                                        'ratio': random.randint(0, 10),
                                                        'param': f'item{j}',
                                                    }
                                                    for i in range(1, 7)
                                                    for j in range(1, 15)
                                                ],
                                                xField='ratio',
                                                yField='carriage',
                                                seriesField='param',
                                                isStack=True,
                                                isPercent=False,
                                                label={'formatter': {'func': '(item) => item.ratio.toFixed(2)'}},
                                                style={
                                                    'height': '100%',
                                                    'width': '100%',
                                                    'border': 'none',
                                                    'border-collapse': 'collapse',
                                                    'border-spacing': '0',
                                                    'backgroundColor': 'transparent'
                                                },
                                            )
                                        ],
                                        style={"height": "250px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0,
                                               "width": "100%",}
                                    ),
                                ),
                                span=8,
                            ),
                        ],
                        gutter=[10, 10],
                    ),
                    span=18,
                ),
            ],
            gutter=[10, 10],
        )
    ]
