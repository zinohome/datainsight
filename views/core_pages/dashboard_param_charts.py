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
import random

def render(themetoken):
    """数据大屏-参数图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="param_update-data-interval",
            interval=3000,  # 示例，每3秒更新一次
        ),
        # 添加主题模式存储 - 初始设为深色
        dcc.Store(id="theme-mode-store", data="dark"),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 展示数据更新时间
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量
                        children=fac.AntdSpace(
                            [
                                fac.AntdText(
                                    [
                                        "数据最近更新时间：",
                                        fac.AntdText(
                                            datetime.now().strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                            id="param_update-datetime",
                                            type="secondary",
                                        ),
                                    ]
                                )
                            ],
                            style={"width": "100%", "display": "flex", "alignItems": "center"}
                        )
                    ),
                    span=24,
                    style={'display': 'none'}
                ),

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
                                                options=[
                                                    {'label': f'161{i}车', 'value': f'161{i}'} for i in range(1, 7)
                                                ],
                                                style={'width': 100},
                                            ),
                                            label='车号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=[
                                                    {'label': f'{i}车厢', 'value': f'{i}'} for i in range(1, 7)
                                                ],
                                                style={'width': 100},
                                            ),
                                            label='车厢号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=[
                                                    {'label': '故障', 'value': 'fault'},
                                                    {'label': '预警', 'value': 'warning'}
                                                ],
                                                style={'width': 100},
                                            ),
                                            label='组件'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdDateRangePicker(
                                                placeholder=['开始日期时间', '结束日期时间'],
                                                showTime={'defaultValue': ['08:30:00', '17:30:00']},
                                                needConfirm=True,
                                            ),
                                            label='时间范围'
                                        ),
                                        fac.AntdFormItem(fac.AntdButton('查询', type='primary', ghost=True,
                                                                        icon=fac.AntdIcon(icon='antd-search'))),
                                    ],
                                    layout='inline',
                                    style={'justifyContent': 'center'},
                                ),
                            ]
                        )
                    ),
                    span=24,
                ),
                # 参数运行数据
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="参数运行数据",
                        description=html.A(
                            "一期运行参数",
                            href="https://www.baidu.com",
                            target="_blank",
                            style={"textDecoration": "none"}
                        ),
                        chart=fact.AntdLine(
                            id="param_operation-data-chart",
                            data=(lambda: [
                                item for i in range(0, 24, 2)
                                for item in [
                                    {"time": f"{i}:00", "type": "speed", "value": random.randint(30, 80)},
                                    {"time": f"{i}:00", "type": "temperature", "value": random.randint(20, 30)}
                                ]
                            ])(),
                            xField="time",
                            yField="value",
                            seriesField="type",
                            smooth=True,
                            color=["#1890ff", "#faad14"],
                        ),
                        height=450,
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]