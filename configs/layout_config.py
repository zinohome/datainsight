from typing import Literal

# 自定义类属性装饰器（放在LayoutConfig类定义前）
class classproperty:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        return self.func(owner)

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
        #"colorBgCard": "transparent",        # 卡片背景透明
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

    # 4. 卡片透明控制变量（通过修改此值切换卡片透明：True 或 False）
    card_transparent: bool = False  # 默认不透明

    # 5. 激活当前主题（修改为类属性，支持直接通过类访问）
    @classproperty
    def dashboard_theme(cls):
        # 使用类变量current_theme选择基础主题
        base_theme = cls.dark_theme if cls.current_theme == "dark" else cls.light_theme
        # 复制基础主题配置
        theme = base_theme.copy()
        # 根据类变量card_transparent控制透明度
        if cls.card_transparent:
            theme["colorBgCard"] = "transparent"
        return theme



