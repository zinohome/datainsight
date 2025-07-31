from dash import html
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style


def render():
    """子页面：数据大屏入口页"""  # 更新文档字符串

    return fac.AntdSpace(
        [
            fac.AntdBreadcrumb(
                items=[{"title": "主要页面"}, {"title": "数据大屏入口页"}]  # 更新面包屑标题
            ),
            fac.AntdAlert(
                type="info",
                showIcon=True,
                message="这里是数据大屏入口页",  # 更新提示标题
                description=fac.AntdText(
                    [
                        "点击",
                        html.A(
                            "此处", href="/dashboard/line", target="_blank"  # 更新链接路径
                        ),
                        "打开数据大屏页面。",  # 更新描述文本
                        html.Br(),
                        "本页面模块路径：",
                        fac.AntdText(
                            "views/core_pages/dashboard.py", strong=True  # 更新模块路径提示
                        ),
                    ]
                ),
            ),
        ],
        direction="vertical",
        style=style(width="100%"),
    )
