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


def render(themetoken):
    """数据大屏-折线图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="update-data-interval",
            interval=3000,  # 示例，每1秒更新一次
        ),
        # 添加主题模式存储 - 初始设为深色
        dcc.Store(id="theme-mode-store", data="dark"),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 展示数据更新时间
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量（已关联配置）
                        children=fac.AntdSpace(
                            [
                                fac.AntdText(
                                    [
                                        "数据最近更新时间：",
                                        fac.AntdText(
                                            datetime.now().strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                            id="update-datetime",
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
                # 展示列车图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]}, 
                        children=fac.AntdSpace(
                            [
                                # 地铁列车图 - 六节车厢（图片拼接版）
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "padding": "5px",
                                        "width": "100%"
                                    },
                                    children=[
                                        # 车头（左侧图片）
                                        html.Img(
                                            src="/assets/imgs/train_headL.png",  # 车头左侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "8px 0 0 8px",
                                                "objectFit": "cover"  # 保持图片比例并填充容器
                                            }
                                        ),
                                        # 车厢1-6（每节由左右图片拼接）
                                        *[html.Div(
                                            style={
                                                "flex": "1 1 auto",  # 等比例分配剩余空间
                                                "minWidth": "60px",  # 最小宽度限制，防止过度压缩
                                                "height": "74px",
                                                "display": "flex",  # 启用flex布局拼接左右图片
                                                "borderLeft": "0px dashed white"  # 车厢间分隔线
                                            },
                                            children=[
                                                # 车厢左侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyL.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                ),
                                                # 车厢右侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyR.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                )
                                            ]
                                        ) for i in range(6)],  # 6节车厢
                                        # 车尾（右侧图片）
                                        html.Img(
                                            src="/assets/imgs/train_headR.png",  # 车尾右侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "0 8px 8px 0",
                                                "borderLeft": "0px dashed white",  # 与前一节车厢分隔
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

                # 列车在线情况
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]}, 
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="列车在线情况",
                        chart=fac.AntdRow(
                            [
                                # 圆环1
                                fac.AntdCol(
                                    fact.AntdPie(
                                        id="today-hot-search-wordcloud-chart",
                                        key="dfdfsfsfds",
                                        data=[{"value": 75}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{75}",
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
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                ),
                                # 圆环2
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 60}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{60}",
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
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                ),
                                # 圆环3
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 85}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{85}",
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
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                )
                            ],
                            gutter=0
                        )
                    ),
                    span=24,
                    style={"marginBottom": "15px"}
                )
            ],
            gutter=10
        )
    ]