import re
from typing import List, Union


class RouterConfig:
    """路由配置参数"""

    # 与应用首页对应的pathname地址
    index_pathname: str = "/index"

    # 核心页面侧边菜单结构
    core_side_menu: List[dict] = [
        {
            "component": "ItemGroup",
            "props": {
                "title": "主要页面",
                "key": "主要页面",
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
                        "title": "主要页面",  # 修改："主要页面1" -> "主要页面"
                        "key": "/macada/page1",
                        "icon": "antd-app-store",
                        "href": "/macada/page1",
                    },
                },
                # 删除以下子菜单演示整个配置块
                # {
                #     "component": "SubMenu",
                #     "props": {
                #         "key": "子菜单演示",
                #         "title": "子菜单演示",
                #         "icon": "antd-catalog",
                #     },
                #     "children": [
                #         {
                #             "component": "Item",
                #             "props": {
                #                 "key": "/macada/sub-menu-page1",
                #                 "title": "子菜单演示1",
                #                 "href": "/macada/sub-menu-page1",
                #             },
                #         },
                #         {
                #             "component": "Item",
                #             "props": {
                #                 "key": "/macada/sub-menu-page2",
                #                 "title": "子菜单演示2",
                #                 "href": "/macada/sub-menu-page2",
                #             },
                #         },
                #         {
                #             "component": "Item",
                #             "props": {
                #                 "key": "/macada/sub-menu-page3",
                #                 "title": "子菜单演示3",
                #                 "href": "/macada/sub-menu-page3",
                #             },
                #         },
                #     ],
                # },
                {
                    "component": "Item",
                    "props": {
                        "title": "独立页面",  # 保持标题不变
                        "key": "/macada/independent-page",
                        "icon": "antd-bar-chart",
                        "href": "/macada/independent-page",
                    },
                },
                # 删除以下独立通配页面入口项
                # {
                #     "component": "Item",
                #     "props": {
                #         "title": "独立通配页面渲染入口页",
                #         "key": "/macada/independent-wildcard-page",
                #         "icon": "antd-app-store",
                #         "href": "/macada/independent-wildcard-page",
                #     },
                # },
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
        # 删除以下"其他页面"相关配置
        # {
        #     "component": "ItemGroup",
        #     "props": {
        #         "title": "其他页面",
        #         "key": "其他页面",
        #     },
        #     "children": [
        #         {
        #             "component": "Item",
        #             "props": {
        #                 "title": "其他页面1",
        #                 "key": "/macada/other-page1",
        #                 "icon": "antd-app-store",
        #                 "href": "/macada/other-page1",
        #             },
        #         }
        #     ],
        # },
    ]

    # 有效页面pathname地址 -> 页面标题映射字典
    valid_pathnames: dict = {
        "/": "首页",
        index_pathname: "首页",
        "/macada/page1": "主要页面",
        # 删除以下子菜单页面路由映射
        # "/macada/sub-menu-page1": "子菜单演示1",
        # "/macada/sub-menu-page2": "子菜单演示2",
        # "/macada/sub-menu-page3": "子菜单演示3",
        "/macada/independent-page": "独立页面",  # 恢复原标题
        # 删除数据大屏路由映射
        # "/macada/dashboard": "数据大屏",
        # 恢复独立页面演示路由
        "/macada/independent-page/demo": "独立页面演示示例",
        # 删除以下独立通配页面相关配置
        # "/macada/independent-wildcard-page": "独立通配页面渲染入口页",
        "/macada/url-params-page": "url参数提取示例",
        "/404-demo": "404状态页演示",
        "/500-demo": "500状态页演示",
        # 独立渲染页面 - 更新为数据大屏
        "/macada/dashboard": "数据大屏",  # 新增数据大屏路由映射
        # 删除旧的独立页面演示路由
        # "/macada/independent-page/demo": "独立页面演示示例",
        "/macda/dashboard": "数据大屏入口页",  # 修正路径：/dashboard -> /macda/dashboard
        "/macda/dashboard/line": "数据大屏-折线图",  # 修正路径：/dashboard/line -> /macda/dashboard/line
        # 删除旧的错误路径配置
        # "/dashboard": "数据大屏入口页",
        # "/dashboard/line": "数据大屏-折线图",
        # 删除旧路径映射
        # "/macada/independent-page": "独立页面渲染入口页",
    }

    # 独立渲染展示的核心页面
    independent_core_pathnames: List[Union[str, re.Pattern]] = [
        "/macda/dashboard/line",  # 修正路径：/dashboard/line -> /macda/dashboard/line
    ]

    # 删除以下通配页面模式字典
    # # 通配页面模式字典
    # wildcard_patterns: dict = {
    #     "独立通配页面演示": re.compile(r"^/macada/independent-wildcard-page/demo/(.*?)$")
    # }

    # 部分页面pathname对应要展开的子菜单层级
    side_menu_open_keys: dict = {
        # 删除以下子菜单展开配置
        # "/macada/sub-menu-page1": ["子菜单演示"],
        # "/macada/sub-menu-page2": ["子菜单演示"],
        # "/macada/sub-menu-page3": ["子菜单演示"],
    }

