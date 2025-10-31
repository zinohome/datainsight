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
from views.core_pages.train_chart_info import create_train_chart_info


def render(themetoken):
    """数据大屏-折线图页面主内容渲染"""
    c_f_fault_table_colnames = ['车号', '车厢号', '故障部件', '开始时间', '操作']
    c_w_warning_table_colnames = ['车号', '车厢号', '预警部件', '开始时间', '操作']
    return [
        # URL参数处理
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='c_url-params-store', data={}),
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="l-update-data-interval",
            interval=BaseConfig.line_update_data_interval,  # 示例，每10秒更新一次
        ),
        # 机组SVG首帧自启动一次性触发
        dcc.Interval(
            id='c_unit-svg-init',
            interval=200,
            n_intervals=0,
            max_intervals=1
        ),
        # 添加主题模式存储 - 初始设为深色
        dcc.Store(id="theme-mode-store", data="dark"),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 数据筛选
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量
                        children=fac.AntdSpace(
                            [
                                fac.AntdForm(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=BaseConfig.train_select_options,
                                                style={'width': 100},
                                                id='c_train_no'
                                            ),
                                            label='车号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=BaseConfig.carriage_select_options,
                                                style={'width': 100},
                                                id='c_carriage_no'
                                            ),
                                            label='车厢号'
                                        ),
                                        fac.AntdFormItem(fac.AntdButton('查询', type='primary', ghost=True,
                                                                        icon=fac.AntdIcon(icon='antd-search'),
                                                                        id='c_query_button', nClicks=0)),
                                    ],
                                    layout='inline',
                                    style={'justifyContent': 'center'},
                                ),
                            ]
                        )
                    ),
                    span=24,
                ),
                # 展示列车图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        children=fac.AntdSpace(
                            [
                                # 地铁列车图 - 六节车厢（图片拼接版）
                                html.Div(id='carriage-chart-info-container', children=create_train_chart_info(themetoken, 'carriage'))
                            ],
                            style={"width": "100%", "display": "flex", "justifyContent": "center",
                                   "alignItems": "center", "padding": "5px"}
                        )
                    ),
                    span=24,
                ),
                # 当前车厢空调状态区域 - 左侧单列，视觉上跨两行
                fac.AntdCol(
                    fac.AntdRow(
                        [
                            # 故障告警图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="故障告警",
                                    chart=
                                    fac.AntdTable(
                                        id='c_f_fault-table',
                                        columns=[
                                            {
                                                'title': column,
                                                'dataIndex': column,
                                                'width': '{:.2f}%'.format(100 / len(c_f_fault_table_colnames)),
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
                                            for column in c_f_fault_table_colnames
                                        ],
                                        size='small',
                                        pagination=False,
                                        bordered = False,
                                        maxHeight=180,
                                        mode = 'client-side',
                                        className = "fault-table",
                                        style = {
                                            'height': '100%',
                                            'width': '100%',
                                            'border': 'none',
                                            'border-collapse': 'collapse',
                                            'border-spacing': '0',
                                            'backgroundColor': 'transparent'
                                        },
                                    ),
                                height=260,
                                ),
                                span=24,
                            ),
                        # 状态预警图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="状态预警",
                                    chart=fac.AntdTable(
                                        id='c_w_warning-table',
                                        columns=[
                                            {
                                                'title': column,
                                                'dataIndex': column,
                                                'width': '{:.2f}%'.format(100 / len(c_w_warning_table_colnames)),
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
                                            for column in c_w_warning_table_colnames
                                        ],
                                        size='small',
                                        pagination=False,
                                        bordered = False,
                                        maxHeight=180,
                                        mode = 'client-side',
                                        className = "fault-table",
                                        style = {
                                            'height': '100%',
                                            'width': '100%',
                                            'border': 'none',
                                            'border-collapse': 'collapse',
                                            'border-spacing': '0',
                                            'backgroundColor': 'transparent'
                                        },
                                    ),
                                    height=260,
                                ),
                                span=24,
                            ),
                        ],
                    ),
                    span=8,
                ),
                # 右侧图表容器 - 宽度16列，包含3个图表，分两行两列排列
                fac.AntdCol(
                    fac.AntdRow(
                        [
                            # 机组实时信息
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="机组实时信息",
                                    description=html.A(
                                        id='param-link',
                                        children="更多",
                                        target=BaseConfig.external_link_target,
                                        style={
                                            # "color": themetoken["colorText"],  # 继承原文本颜色
                                            "textDecoration": "none"  # 可选：移除下划线
                                        }
                                    ),
                                    chart=fac.AntdRow(
                                            fac.AntdCol(
                                            [
                                                # 机组状态显示区域
                                                    fac.AntdRow(
                                                        [
                                                            fac.AntdCol(
                                                                fac.AntdTabs(
                                                                    id='c_unit-tabs',
                                                                    defaultActiveKey='unit1',
                                                                    tabPosition='left',
                                                                    destroyInactiveTabPane=False,
                                                                    tabPaneAnimated=False,
                                                                    inkBarAnimated=False,
                                                                    items=[
                                                                        {
                                                                            "key": "unit1",
                                                                            "label": "机组一",
                                                                            "children": fac.AntdRow(
                                                                                [
                                                                                    fac.AntdCol(
                                                                                        html.Div(
                                                                                            id='c_unit1-svg-container',
                                                                                            style={
                                                                                                "height": "240px",
                                                                                                "width": "100%",
                                                                                                "overflow": "hidden",
                                                                                                "marginTop": "-6px",
                                                                                                "position": "relative",
                                                                                                "zIndex": 0
                                                                                            }
                                                                                        ),
                                                                                        span=20
                                                                                    ),
                                                                                    fac.AntdCol(
                                                                                        html.Div(
                                                                                            id='c_unit1-co2-indicator',
                                                                                            style={
                                                                                                "width": "120px",
                                                                                                "height": "100%",
                                                                                                "display": "flex",
                                                                                                "alignItems": "center",
                                                                                                "justifyContent": "flex-end"
                                                                                            }
                                                                                        ),
                                                                                        style={
                                                                                            "textAlign": "right",
                                                                                            "overflow": "visible",
                                                                                            "display": "flex",
                                                                                            "alignItems": "flex-start",
                                                                                            "justifyContent": "flex-end",
                                                                                            "zIndex": 1
                                                                                        },
                                                                                        span=4
                                                                                    ),
                                                                                ],
                                                                                align="middle",
                                                                                justify="start",
                                                                                style={"height": "240px"}
                                                                            )
                                                                        },
                                                                        {
                                                                            "key": "unit2",
                                                                            "label": "机组二",
                                                                            "children": fac.AntdRow(
                                                                                [
                                                                                    fac.AntdCol(
                                                                                        html.Div(
                                                                                            id='c_unit2-svg-container',
                                                                                            style={
                                                                                                "height": "240px",
                                                                                                "width": "100%",
                                                                                                "overflow": "hidden",
                                                                                                "marginTop": "-6px",
                                                                                                "position": "relative",
                                                                                                "zIndex": 0
                                                                                            }
                                                                                        ),
                                                                                        span=20
                                                                                    ),
                                                                                    fac.AntdCol(
                                                                                        html.Div(
                                                                                            id='c_unit2-co2-indicator',
                                                                                            style={
                                                                                                "width": "120px",
                                                                                                "height": "100%",
                                                                                                "display": "flex",
                                                                                                "alignItems": "center",
                                                                                                "justifyContent": "flex-end"
                                                                                            }
                                                                                        ),
                                                                                        style={
                                                                                            "textAlign": "right",
                                                                                            "overflow": "visible",
                                                                                            "display": "flex",
                                                                                            "alignItems": "flex-start",
                                                                                            "justifyContent": "flex-end",
                                                                                            "zIndex": 1
                                                                                        },
                                                                                        span=4
                                                                                    ),
                                                                                ],
                                                                                align="middle",
                                                                                justify="start",
                                                                                style={"height": "240px"}
                                                                            )
                                                                        }
                                                                    ],
                                                                    style={"height": "240px"}
                                                                ),
                                                                span=24
                                                            )
                                                        ],
                                                        align="middle",
                                                        justify="center",
                                                        style={"height": "240px", "marginBottom": "5px"}
                                                    )
                                            ],
                                            span=24,
                                        ),
                                        justify="center",
                                        align="middle",
                                        style={"height": "100%"}
                                    ),
                                    height=250,
                                ),
                                span=24,
                            ),
                            # 关键指标：机组一
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="关键指标：机组一",
                                    chart=fac.AntdRow(
                                        fac.AntdCol(
                                            [
                                                fac.AntdRow(
                                                    [
                                                        # 机组一 送风温度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit1_supply_temp',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `送风温度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                        # 机组一 湿度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit1_humidity',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `湿度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                        # 机组一 车厢温度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit1_car_temp',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `车厢温度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                    ],
                                                    align="bottom",
                                                    justify="center",
                                                    style={"height": "100px", "marginBottom": "5px"}
                                                ),
                                                fac.AntdRow(
                                                    [
                                                        # 机组一 电流一 
                                                        fac.AntdCol(
                                                            fac.AntdSpace(
                                                                [
                                                                    fac.AntdTimeline(
                                                                        id='c_i_unit1_current1',
                                                                        items=[
                                                                            {
                                                                                'label': '0',
                                                                                'content': '冷凝风机电流-U11'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '压缩机电流-U11'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '通风机电流-U11'
                                                                            }
                                                                        ],
                                                                        mode='right'
                                                                    )
                                                                ],
                                                                direction='vertical',
                                                                style={
                                                                    'width': '100%',
                                                                },
                                                            ),
                                                            span=12,
                                                        ),
                                                        # 机组一 电流二
                                                        fac.AntdCol(
                                                            fac.AntdSpace(
                                                                [
                                                                    fac.AntdTimeline(
                                                                        id='c_i_unit1_current2',
                                                                        items=[
                                                                            {
                                                                                'label': '0',
                                                                                'content': '冷凝风机电流-U12'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '压缩机电流-U12'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '通风机电流-U12'
                                                                            }
                                                                        ],
                                                                        mode='right'
                                                                    )
                                                                ],
                                                                direction='vertical',
                                                                style={
                                                                    'width': '100%',
                                                                },
                                                            ),
                                                            span=12,
                                                        ),
                                                    ],
                                                    align="bottom",
                                                    justify="center",
                                                    style={"height": "100px", "marginBottom": "5px"}
                                                ),
                                            ],
                                            span=24,
                                        )
                                    ),
                                    height=250,
                                ),
                                span=12,
                            ),
                            # 关键指标：机组二
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="关键指标：机组二",
                                    chart=fac.AntdRow(
                                        fac.AntdCol(
                                            [
                                                fac.AntdRow(
                                                    [
                                                        # 机组二 送风温度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit2_supply_temp',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `送风温度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                        # 机组二 湿度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit2_humidity',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `湿度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                        # 机组二 车厢温度
                                                        fac.AntdCol(
                                                            fact.AntdGauge(
                                                                id='c_i_unit2_car_temp',
                                                                percent=0.5,
                                                                padding=[5,5,5,5],
                                                                renderer='svg',
                                                                range={
                                                                    'ticks': [0, 1 / 3, 2 / 3, 1],
                                                                    'color': ['#F4664A', '#FAAD14', '#30BF78'],
                                                                },
                                                                indicator={
                                                                    'pointer': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                    'pin': {
                                                                        'style': {
                                                                            'stroke': '#D0D0D0',
                                                                        },
                                                                    },
                                                                },
                                                                statistic={
                                                                    'content': {
                                                                        'formatter': {
                                                                            'func': """({ percent }) => `车厢温度: ${ percent }`"""
                                                                        },
                                                                        'style': {
                                                                            'color': 'cyan',
                                                                            'fontSize': '12px',
                                                                        },
                                                                    },
                                                                },
                                                            ),
                                                            span=8,
                                                        ),
                                                    ],
                                                    align="top",
                                                    justify="center",
                                                    style={"height": "100px", "marginBottom": "5px"}
                                                ),
                                                fac.AntdRow(
                                                    [
                                                        # 机组二 电流一 
                                                        fac.AntdCol(
                                                            fac.AntdSpace(
                                                                [
                                                                    fac.AntdTimeline(
                                                                        id='c_i_unit2_current1',
                                                                        items=[
                                                                            {
                                                                                'label': '0',
                                                                                'content': '冷凝风机电流-U21'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '压缩机电流-U21'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '通风机电流-U21'
                                                                            }
                                                                        ],
                                                                        mode='right'
                                                                    )
                                                                ],
                                                                direction='vertical',
                                                                style={
                                                                    'width': '100%',
                                                                },
                                                            ),
                                                            span=12,
                                                        ),
                                                        # 机组二 电流二
                                                        fac.AntdCol(
                                                            fac.AntdSpace(
                                                                [
                                                                    fac.AntdTimeline(
                                                                        id='c_i_unit2_current2',
                                                                        items=[
                                                                            {
                                                                                'label': '0',
                                                                                'content': '冷凝风机电流-U22'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '压缩机电流-U22'
                                                                            },
                                                                            {
                                                                                'label': '0',
                                                                                'content': '通风机电流-U22'
                                                                            }
                                                                        ],
                                                                        mode='right'
                                                                    )
                                                                ],
                                                                direction='vertical',
                                                                style={
                                                                    'width': '100%',
                                                                },
                                                            ),
                                                            span=12,
                                                        ),
                                                    ],
                                                    align="top",
                                                    justify="center",
                                                    style={"height": "100px", "marginBottom": "5px"}
                                                ),
                                            ],
                                            span=24,
                                        )
                                    ),
                                    height=250,
                                ),
                                span=12,
                            ),
                        ],
                        gutter=[10, 10],
                    ),
                    span=16,
                ),
            ],
            gutter=[10, 10],
        )
    ]