from typing import Literal


class LayoutConfig:
    """页面布局相关配置参数"""

    # 核心页面侧边栏像素宽度（展开状态）
    core_side_width: int = 330

    # 核心页面侧边栏像素宽度（折叠状态）
    core_side_collapsed_width: int = 90

    # 侧边栏初始折叠状态控制参数
    core_side_initial_collapsed: bool = False

    # 核心页面呈现类型
    core_layout_type: Literal["single", "tabs"] = "single"

    # 是否在页首中显示页面搜索框
    show_core_page_search: bool = False

    # 1. 定义深色主题配置
    dark_theme: dict = {
        "colorBgContainer": "#141414",  # 容器背景色
        "colorText": "#fff",             # 文本颜色
        "colorBgCard": "#2a2a2a",        # 卡片背景色
        "colorBorder": "#434343"         # 边框颜色
    }

    # 2. 定义浅色主题配置
    light_theme: dict = {
        "colorBgContainer": "#f5f5f5",  # 容器背景色
        "colorText": "#000",             # 文本颜色
        "colorBgCard": "#fff",           # 卡片背景色
        "colorBorder": "#dae0ea"         # 边框颜色
    }

    # 3. 主题切换控制变量（通过修改此值切换主题："dark" 或 "light"）
    current_theme: str = "dark"  # 默认使用深色主题

    # 4. 激活当前主题（根据current_theme自动选择）
    dashboard_theme: dict = dark_theme if current_theme == "dark" else light_theme
