from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc

from configs import BaseConfig
from configs.layout_config import LayoutConfig
from feffery_dash_utils.style_utils import style

def render():
    """渲染数据大屏专用侧边导航栏"""
    prefix = BaseConfig.project_prefix
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
                "title": "线路",
                "key": f"/{prefix}/line",
                "icon": "antd-ordered-list",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-line",
                "href": f"/{prefix}/line"
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "列车",
                "key": f"/{prefix}/train",
                "icon": "antd-alert",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-train",
                "href": f"/{prefix}/train"
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "车厢",
                "key": f"/{prefix}/carriage",
                "icon": "antd-sliders",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-carriage",
                "href": f"/{prefix}/carriage"
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "参数",
                "key": f"/{prefix}/param",
                "icon": "antd-line-chart",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-param",
                "href": f"/{prefix}/param"
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "故障",
                "key": f"/{prefix}/fault",
                "icon": "antd-disconnect",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-fault",
                "href": f"/{prefix}/fault"
            }
        },
        {
            "component": "Item",
            "props": {
                "title": "寿命",
                "key": f"/{prefix}/health",
                "icon": "antd-hourglass",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-health",
                "href": f"/{prefix}/health"
            }
        },
    ]

    return fac.AntdAffix(
        fuc.FefferyDiv(
            [
                # 侧边菜单
                fac.AntdMenu(
                    id="dashboard-side-menu",
                    menuItems=dash_menuItems,
                    mode="inline",
                    defaultOpenKeys=[],
                    inlineCollapsed=True,
                    style=style(
                        border="none",
                        width="100%",
                        padding="75px 2px 0 2px",
                        background="transparent",
                    ),
                )
            ],
            scrollbar="hidden",
            style=style(
                height="100vh",
                overflowY="hidden",
                borderRight="1px solid "+themetoken["colorBorder"],
                padding="0 0px",
                background="transparent",
            ),
        ),
        id="dashboard-side-menu-affix",
        offsetTop=17.1,
        # 关键更新：根据初始状态动态选择宽度参数
        style=style(
            width="48px",
            zIndex=1000,
            position="absolute",  # 将固定定位改为绝对定位
            left=0,
            top=0,
            background="transparent",
            #background=themetoken["colorBgCard"],  # 新增：确保背景色填充完整
        ),
    )

