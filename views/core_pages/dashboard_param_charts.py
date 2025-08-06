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
                # 展示参数图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]}, 
                        children=fac.AntdSpace(
                            [
                                # 参数详细展示
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "padding": "5px",
                                        "width": "100%"
                                    },
                                    children=[
                                        # 参数左侧图片
                                        html.Img(
                                            src="/assets/imgs/train_headL.png",  # 参数左侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "8px 0 0 8px",
                                                "objectFit": "cover"
                                            }
                                        ),
                                        # 参数1-6（每节由左右图片拼接）
                                        *[html.Div(
                                            style={
                                                "flex": "1 1 auto",  # 等比例分配剩余空间
                                                "minWidth": "60px",  # 最小宽度限制，防止过度压缩
                                                "height": "74px",
                                                "display": "flex",  # 启用flex布局拼接左右图片
                                                "borderLeft": "0px dashed white"  # 参数间分隔线
                                            },
                                            children=[
                                                # 参数左侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyL.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                ),
                                                # 参数右侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyR.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                )
                                            ]
                                        ) for i in range(6)],  # 6个参数
                                        # 参数右侧图片
                                        html.Img(
                                            src="/assets/imgs/train_headR.png",  # 参数右侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "0 8px 8px 0",
                                                "borderLeft": "0px dashed white",  # 与前一个参数分隔
                                                "objectFit": "cover"
                                            }
                                        )
                                    ]
                                )
                            ],
                            style={"width": "100%", "display": "flex", "justifyContent": "center",
                                   "alignItems": "center", "padding": "5px"}
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
                        height=350,
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]