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
from views.core_pages.train_chart_link import create_train_chart_link


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
                                html.Div(id='carriage-chart-link-container', children=create_train_chart_link(themetoken, 'param'))
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
                        chart=fac.AntdRow(
                            [''],
                            style={"height": "100px",
                                   "alignItems": "flex-start",
                                    "margin": 0,
                                    "padding": 0}
                        ),
                        height=350,
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
                                            maxHeight=280,
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
                                height=350,
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
                                            maxHeight=280,
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
                                    height=350,
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
                                    chart=fac.AntdSpin(
                                        fac.AntdTable(
                                            id='c_h_health_table',
                                            columns=[
                                                {
                                                    'title': column,
                                                    'dataIndex': column,
                                                    'width': '{:.2f}%'.format(100 / len(c_h_health_table_colnames)),
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
                                                    }} if column == '耗用率' else {})
                                                }
                                                for column in c_h_health_table_colnames
                                            ],
                                            size='small',
                                            pagination=False,
                                            bordered=False,
                                            maxHeight=250,
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
                                        text='数据加载中',
                                    ),
                                    height=350,
                                ),
                                span=8,
                            ),
                            # 典型故障图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="典型故障",
                                    chart=fac.AntdRow(
                                        [
                                            fact.AntdWordCloud(
                                                id="c_f_fault-wordcloud",
                                                wordField="word",
                                                weightField="value",
                                                height=300,
                                                colorField='word',
                                                wordStyle={'fontSize': [12, 36]},
                                            ),
                                        ],
                                        style={"height": "300px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0}
                                    ),
                                    height=350,
                                ),
                                span=8,
                            ),
                            # 典型预警图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="典型预警",
                                    chart=fac.AntdRow(
                                        [
                                            fact.AntdWordCloud(
                                                id="c_w_warning-wordcloud",
                                                wordField="word",
                                                weightField="value",
                                                height=300,
                                                colorField='word',
                                                wordStyle={'fontSize': [12, 36]},
                                            ),
                                        ],
                                        style={"height": "300px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0}
                                    ),
                                    height=350,
                                ),
                                span=8,
                            ),
                            # 部件寿命图表
                            fac.AntdCol(
                                macda_card(
                                    rootStyle={"background": themetoken["colorBgCard"]},
                                    titleStyle={"color": themetoken["colorText"]},
                                    descriptionStyle={"color": themetoken["colorText"]},
                                    title="部件耗用率%",
                                    chart=fac.AntdRow(
                                [
                                            fact.AntdBar(
                                                id='c_h_health_bar',
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
                                        style={"height": "300px",
                                               "alignItems": "flex-start",
                                               "margin": 0,
                                               "padding": 0}
                                    ),
                                    height=350,
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