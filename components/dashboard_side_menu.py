from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from configs.layout_config import LayoutConfig
from feffery_dash_utils.style_utils import style

def render():
    """渲染数据大屏专用侧边导航栏"""
    themetoken = LayoutConfig.dashboard_theme
    dash_menuItem_style =  {
                    "padding": "16px 0",  # 保持垂直间距
                    "fontSize": "0",
                    "justifyContent": "center",  # 强制内容居中
                    "margin": "0 auto",  # 水平居中对齐
                    "minWidth": "40px",  # 固定点击区域宽度，避免文字影响
                    "background": "transparent"
    }
    dash_menuItems = [
        {
            "component": "Item",
            "props": {
                "title": "Line",
                "key": "nav-line",
                "icon": "antd-subway",
                "href": "/macda/dashboard/line",
                # 关键优化：统一水平内边距，确保图标居中
                "style": dash_menuItem_style
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "Train",
                "key": "nav-train",
                "icon": "antd-train",
                "href": "/macda/dashboard/train",
                "style": dash_menuItem_style
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "Carriage",
                "key": "nav-carriage",
                "icon": "antd-app-store",
                "href": "/macda/dashboard/carriage",
                "style": dash_menuItem_style
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "Param",
                "key": "nav-param",
                "icon": "antd-line-chart",
                "href": "/macda/dashboard/param",
                "style": dash_menuItem_style
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "Fault",
                "key": "nav-fault",
                "icon": "antd-app-store",
                "href": "/macda/dashboard/fault",
                "style": dash_menuItem_style
            }
        },
    ]

    return fac.AntdAffix(
        fuc.FefferyDiv(
            [
                # 侧边菜单
                fac.AntdMenu(
                    id="core-side-menu",
                    menuItems=dash_menuItems,
                    mode="inline",
                    defaultOpenKeys=[],
                    inlineCollapsed=True,
                    style=style(
                        border="none",
                        width="100%",
                        padding="0 2px"
                    ),
                )
            ],
            scrollbar="hidden",
            style=style(
                height="100vh",
                overflowY="auto",
                borderRight="1px solid "+themetoken["colorBorder"],
                padding="0 0px",
            ),
        ),
        id="dashboard-side-menu-affix",
        offsetTop=17.1,
        # 关键更新：根据初始状态动态选择宽度参数
        style=style(
            width="48px",
            zIndex=1000,
            #background=themetoken["colorBgCard"],  # 新增：确保背景色填充完整
        ),
    )

