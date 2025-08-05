import re
from typing import List, Union

from configs import BaseConfig


class RouterConfig:
    """路由配置参数"""

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
                        "key": "/macda/dashboard",  # 修正路径：/dashboard -> /macda/dashboard
                        "icon": "antd-bar-chart",
                        "href": "/macda/dashboard",  # 修正路径：/dashboard -> /macda/dashboard
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-线路图",
                        "key": "/macda/dashboard/line",
                        "icon": "antd-ordered-list",
                        "href": "/macda/dashboard/line",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "数据大屏-列车图",
                        "key": "/macda/dashboard/train",
                        "icon": "antd-alert",
                        "href": "/macda/dashboard/train",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "主要页面",
                        "key": "/macada/page1",
                        "icon": "antd-app-store",
                        "href": "/macada/page1",
                    },
                },
                {
                    "component": "Item",
                    "props": {
                        "title": "url参数示例",
                        "key": "/macada/url-params-page",
                        "icon": "antd-link",
                        "href": "/macada/url-params-page",
                    },
                },
            ],
        },
    ]

    # 有效页面pathname地址 -> 页面标题映射字典
    valid_pathnames: dict = {
        "/": "首页",
        index_pathname: "首页",
        # 数据大屏路由映射
        "/macada/dashboard": "数据大屏",
        "/macda/dashboard": "数据大屏入口页",
        "/macda/dashboard/line": "数据大屏-折线图",
        "/macda/dashboard/train": "数据大屏-列车图",
        "/macada/page1": "主要页面",
        "/macada/url-params-page": "url参数提取示例",
        "/404-demo": "404状态页演示",
        "/500-demo": "500状态页演示",
    }

    # 独立数据大屏的核心页面
    independent_core_pathnames: List[Union[str, re.Pattern]] = [
        "/macda/dashboard/line",
        "/macda/dashboard/train",
    ]


    # 部分页面pathname对应要展开的子菜单层级
    side_menu_open_keys: dict = {
        # 删除以下子菜单展开配置
        # "/macada/sub-menu-page1": ["子菜单演示"],
        # "/macada/sub-menu-page2": ["子菜单演示"],
        # "/macada/sub-menu-page3": ["子菜单演示"],
    }

