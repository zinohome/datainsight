from dash import html
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style


def render():
    """子页面：独立页面渲染入口页简单示例"""

    return fac.AntdSpace(
        [
            fac.AntdBreadcrumb(
                items=[{"title": "主要页面"}, {"title": "独立页面渲染入口页"}]
            ),
            fac.AntdAlert(
                type="info",
                showIcon=True,
                message="这里是数据大屏入口页",  # 更新标题
                description=fac.AntdText(
                    [
                        "点击",
                        html.A(
                            "此处", href="/macada/dashboard", target="_blank"  # 更新链接路径
                        ),
                        "打开数据大屏页面。",  # 更新描述文本
                        html.Br(),
                        "本页面模块路径：",
                        fac.AntdText(
                            "views/core_pages/independent_page.py", strong=True
                        ),
                    ]
                ),
            ),
        ],
        direction="vertical",
        style=style(width="100%"),
    )
