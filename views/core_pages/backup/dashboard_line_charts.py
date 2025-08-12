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
from .train_chart import create_train_chart


def render(themetoken):
    """数据大屏-折线图页面主内容渲染"""
    l_f_fault_table_colnames = ['车号', '车厢号', '故障部件', '开始时间']
    l_w_warning_table_colnames = ['车号', '车厢号', '预警部件', '开始时间']
    l_h_health_table_colnames = ['车号', '车厢号', '部件', '耗用率', '额定寿命', '已耗']
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="l-update-data-interval",
            interval=10000,  # 示例，每10秒更新一次
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
                            href="https://www.baidu.com",
                            target="_blank",  # 新窗口打开
                            style={
                                #"color": themetoken["colorText"],  # 继承原文本颜色
                                "textDecoration": "none"  # 可选：移除下划线
                            }
                        ),
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
                                    description=html.A(
                                        "一期故障",
                                        href="https://www.baidu.com",
                                        target="_blank",  # 新窗口打开
                                        style={
                                            #"color": themetoken["colorText"],  # 继承原文本颜色
                                            "textDecoration": "none"  # 可选：移除下划线
                                        }
                                    ),
                                    chart=
                                    fac.AntdSpin(
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
                                                    }
                                                }
                                                for column in l_f_fault_table_colnames
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
                                    description=html.A(
                                        "一期预警",
                                        href="https://www.baidu.com",
                                        target="_blank",  # 新窗口打开
                                        style={
                                            #"color": themetoken["colorText"],  # 继承原文本颜色
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
                                                    }
                                                }
                                                for column in l_w_warning_table_colnames
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
                                                    }} if column == '耗用率' else {})
                                                }
                                                for column in l_h_health_table_colnames
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
                                                id="l_f_fault-wordcloud",
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
                                                id="l_w_warning-wordcloud",
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
                                    title="部件寿命",
                                    chart=fac.AntdRow(
                                [
                                            fact.AntdBar(
                                                id='l_h_health_bar',
                                                data=[
                                                    {
                                                        'date': f'2020-0{i}',
                                                        'x': random.randint(0, 100),
                                                        'type': f'item{j}',
                                                    }
                                                    for i in range(1, 10)
                                                    for j in range(1, 4)
                                                ],
                                                xField='x',
                                                yField='date',
                                                seriesField='type',
                                                isStack=True,
                                                isPercent=True,
                                                label={'formatter': {'func': '(item) => item.x.toFixed(2)'}},
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