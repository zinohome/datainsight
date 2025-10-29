import re
from typing import List, Union

from configs import BaseConfig


class RouterConfig:
    """路由配置参数"""
    prefix = BaseConfig.project_prefix
    # 与应用首页对应的pathname地址
    index_pathname: str = "/index"

    # 核心页面侧边菜单结构
    core_side_menu: List[dict] = [
        {
            "component": "ItemGroup",
            "props": {
                "title": f'v{BaseConfig.app_version}',
                "key": "版本号",
            },
            "children": [
                {
                    "component": "Item",
                    "props": {
                        "title": "首页",
                        "key": "/",
                        "icon": "antd-home",
                        "href": "/",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏",
                        "key": f"/{prefix}/",  # 修正路径：/dashboard -> /{prefix}
                        "icon": "antd-bar-chart",
                        "href": f"/{prefix}/",  # 修正路径：/dashboard -> /{prefix}
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-线路图",
                        "key": f"/{prefix}/line",
                        "icon": "antd-ordered-list",
                        "href": f"/{prefix}/line",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-列车图",
                        "key": f"/{prefix}/train",
                        "icon": "antd-alert",
                        "href": f"/{prefix}/train",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-车厢图",
                        "key": f"/{prefix}/carriage",
                        "icon": "antd-car",
                        "href": f"/{prefix}/carriage",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-参数图",
                        "key": f"/{prefix}/param",
                        "icon": "antd-sliders",
                        "href": f"/{prefix}/param",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-故障图",
                        "key": f"/{prefix}/fault",
                        "icon": "antd-exclamation-circle",
                        "href": f"/{prefix}/fault",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-寿命图",
                        "key": f"/{prefix}/health",
                        "icon": "antd-exclamation-circle",
                        "href": f"/{prefix}/health",
                    },
                },
            ],
        },
    ]

    # 有效页面pathname地址 -> 页面标题映射字典
    valid_pathnames: dict = {
        "/": "首页",
        f"/{prefix}/": "首页",  # 添加带前缀的首页路径
        index_pathname: "首页",
        # 数据大屏路由映射
        f"/{prefix}": "数据大屏",
        f"/{prefix}/": "数据大屏入口页",
        f"/{prefix}/line": "数据大屏-折线图",
        f"/{prefix}/train": "数据大屏-列车图",
        f"/{prefix}/carriage": "数据大屏-车厢图",
        f"/{prefix}/param": "数据大屏-参数图",
        f"/{prefix}/fault": "数据大屏-故障图",
        f"/{prefix}/health": "数据大屏-故障图",
        "/404-demo": "404状态页演示",
        "/500-demo": "500状态页演示",
    }

    # 独立数据大屏的核心页面
    independent_core_pathnames: List[Union[str, re.Pattern]] = [
        f"/{prefix}/line",
        f"/{prefix}/train",
        f"/{prefix}/carriage",
        f"/{prefix}/param",
        f"/{prefix}/fault",
        f"/{prefix}/health",
    ]


    # 部分页面pathname对应要展开的子菜单层级
    side_menu_open_keys: dict = {
        # 删除以下子菜单展开配置
        # "/macada/sub-menu-page1": ["子菜单演示"],
        # "/macada/sub-menu-page2": ["子菜单演示"],
        # "/macada/sub-menu-page3": ["子菜单演示"],
    }

