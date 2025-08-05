import random
from dash import html, dcc
from datetime import datetime
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    welcome_card,
    blank_card,
    index_card,
    simple_chart_card,
)

from components import dashboard_side_menu
# 新增导入LayoutConfig
from configs.layout_config import LayoutConfig
import callbacks.core_pages_c.dashboard_carriage_c
from views.core_pages import dashboard_carriage_charts


def render():
    """仪表盘渲染示例"""
    themetoken = LayoutConfig.dashboard_theme

    return fac.AntdConfigProvider(
        id="theme-config-provider",
        primaryColor="#1890ff",
        componentSize="middle",
        locale="zh-cn",
        algorithm="dark",
        token=themetoken,
        children=fac.AntdSpace(
            [
                html.Div(id="carriage-main-bg-div",
                        children=[
                            # 1. 侧边导航栏（固定定位，脱离文档流）
                            dashboard_side_menu.render(),
                            # 2. 主内容容器（背景色填充整个区域）
                            html.Div(
                                id="main-bg-div",
                                children=dashboard_carriage_charts.render(themetoken),  # 传入主题令牌
                                style=style(
                                    padding=15,
                                    # 背景图片配置（替换为你的图片路径）
                                    backgroundImage="url('/assets/imgs/dashboard-bg.png')",
                                    backgroundSize="cover",  # 图片覆盖容器
                                    backgroundRepeat="no-repeat",  # 不重复
                                    backgroundPosition="center",  # 居中显示
                                    backgroundColor=themetoken["colorBgContainer"],
                                    minHeight="100vh",
                                    boxSizing="border-box"
                                ),
                            ),
                        ],
                         style=style(
                             display="flex",
                             # 移除固定background="#f5f5f5"，由主题令牌控制
                             # background="#f5f5f5",
                             background=themetoken["colorBgContainer"],
                             # background="#141414",
                             minHeight="100vh",
                             boxSizing="border-box"
                         ),
                         ),
            ],
            direction="vertical",
            style=style(width="100%"),
        )

    )