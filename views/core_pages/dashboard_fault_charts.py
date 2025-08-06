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
    """数据大屏-故障图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="fault_update-data-interval",
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
                                            id="fault_update-datetime",
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
                # 展示故障图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]}, 
                        children=fac.AntdSpace(
                            [
                                # 故障详细展示
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "padding": "5px",
                                        "width": "100%"
                                    },
                                    children=[
                                        # 故障左侧图片
                                        html.Img(
                                            src="/assets/imgs/train_headL.png",  # 故障左侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "8px 0 0 8px",
                                                "objectFit": "cover"
                                            }
                                        ),
                                        # 故障1-6（每节由左右图片拼接）
                                        *[html.Div(
                                            style={
                                                "flex": "1 1 auto",  # 等比例分配剩余空间
                                                "minWidth": "60px",  # 最小宽度限制，防止过度压缩
                                                "height": "74px",
                                                "display": "flex",  # 启用flex布局拼接左右图片
                                                "borderLeft": "0px dashed white"  # 故障间分隔线
                                            },
                                            children=[
                                                # 故障左侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyL.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                ),
                                                # 故障右侧图片
                                                html.Img(
                                                    src="/assets/imgs/train_bodyR.png",
                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                )
                                            ]
                                        ) for i in range(6)],  # 6节故障
                                        # 车尾（右侧图片）
                                        html.Img(
                                            src="/assets/imgs/train_headR.png",  # 车尾右侧图片
                                            style={
                                                "flex": "0 0 44px",
                                                "height": "74px",
                                                "borderRadius": "0 8px 8px 0",
                                                "borderLeft": "0px dashed white",  # 与前一节故障分隔
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

                # 空调故障预警
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="空调故障预警",
                        description=html.A(
                            "一期故障",
                            href="https://www.baidu.com",
                            target="_blank",
                            style={"textDecoration": "none"}
                        ),
                        chart=fac.AntdTable(
                            columns=[
                                {'title': f'字段{i}',
                                 'dataIndex': f'字段{i}',
                                 'width': width,
                                 'headerCellStyle': {
                                     'fontWeight': 'bold',
                                     'border': 'none',
                                     'border-left': 'none !important',
                                     'border-right': 'none !important',
                                     'borderBottom': '1px solid #e8e8e8',
                                     'color': themetoken["colorText"]
                                 },
                                 'cellStyle': {
                                     'borderRight': 'none',
                                     'borderBottom': '1px solid #e8e8e8',
                                     'color': themetoken["colorText"],
                                     'fontSize': '10px'
                                 }
                                 }
                                for i, width in zip(
                                    range(1, 9), ['12.5%']*8
                                )
                            ],
                            data=[{f'字段{i}': '示例内容' for i in range(1, 9)}] * 3,
                            size="small",
                            bordered=False,
                            maxHeight=250,
                            maxWidth='max-content',
                            pagination=True,
                            className="fault-table",
                            style={
                                'border': 'none',
                                'border-collapse': 'collapse',
                                'border-spacing': '0'
                            },
                        ),
                        height=350,
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]