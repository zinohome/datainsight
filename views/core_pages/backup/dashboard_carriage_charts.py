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
    c_f_fault_table_colnames = ['车号', '车厢号', '故障部件', '开始时间']
    c_w_warning_table_colnames = ['车号', '车厢号', '预警部件', '开始时间']
    c_h_health_table_colnames = ['车号', '车厢号', '部件', '耗用率', '额定寿命', '已耗']
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
                                html.Div(id='carriage-chart-info-container', children=create_train_chart_info(themetoken, 'param'))
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
                                    fac.AntdSpin(
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
                                                    }
                                                }
                                                for column in c_f_fault_table_colnames
                                            ],
                                            size='small',
                                            pagination=False,
                                            bordered = False,
                                            maxHeight=200,
                                            mode = 'server-side',
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
                                    text='数据加载中',
                                    ),
                                height=280,
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
                                    chart=fac.AntdSpin(
                                        fac.AntdTable(
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
                                                    }
                                                }
                                                for column in c_w_warning_table_colnames
                                            ],
                                            size='small',
                                            pagination=False,
                                            bordered = False,
                                            maxHeight=200,
                                            mode = 'server-side',
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
                                    text='数据加载中',
                                    ),
                                    height=280,
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
                                    chart=fac.AntdRow(
                                        [
                                            fac.AntdCol(
                                                html.Img(
                                                    src="/assets/imgs/circle_svg_unit1.svg",
                                                    style={"width": "50%", "height": "50%", "objectFit": "contain"}
                                                ),
                                                span=24
                                            ),
                                            fac.AntdCol(
                                                html.Img(
                                                    src="/assets/imgs/circle_svg_unit1.svg",
                                                    style={"width": "50%", "height": "50%", "objectFit": "contain"}
                                                ),
                                                span=24
                                            )
                                        ],
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
                                    chart=fac.AntdRow(),
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
                                    chart=fac.AntdRow(),
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