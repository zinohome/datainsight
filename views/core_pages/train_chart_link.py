from dash import html, dcc
import feffery_antd_components as fac


def create_train_chart_link(themetoken):
    """
    创建地铁列车图组件

    参数:
        themetoken: 主题令牌，包含颜色等样式信息

    返回:
        dash.html.Div: 包含列车图的Div组件
    """
    return html.Div(
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
            *[dcc.Link(  # 添加链接组件
                href=f"/macda/dashboard/carriage?carriage={i + 1}",
                children=html.Div(
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
            )
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