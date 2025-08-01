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
# 新增导入LayoutConfig
from configs.layout_config import LayoutConfig
import callbacks.core_pages_c.dashboard_c

def render():
    """仪表盘渲染示例"""
    # 移除本地themetoken定义，使用配置文件中的dashboard_theme
    themetoken = LayoutConfig.dashboard_theme


    return fac.AntdConfigProvider(
        id="theme-config-provider",
        primaryColor="#1890ff",
        componentSize="middle",
        locale="zh-cn",
        algorithm="dark",  # 保持深色主题算法
        token=themetoken,  # 使用配置文件中的主题
        children=fac.AntdSpace(
            [
                html.Div(id="main-bg-div",
                    children=[
                        # 消息提示输出目标
                        fac.Fragment(id="message-target"),
                        # 数据统一更新轮询
                        dcc.Interval(
                            id="update-data-interval",
                            interval=1000,  # 示例，3秒更新一次
                        ),
                        # 添加主题模式存储 - 初始设为深色
                        dcc.Store(id="theme-mode-store", data="dark"),
                        # 仪表盘网格布局
                        fac.AntdRow(
                            [
                                # 展示数据更新时间
                                fac.AntdCol(
                                    blank_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量（已关联配置）
                                        children=fac.AntdSpace(
                                            [
                                                fac.AntdText(
                                                    [
                                                        "数据最近更新时间：",
                                                        fac.AntdText(
                                                            datetime.now().strftime(
                                                                "%Y-%m-%d %H:%M:%S"
                                                            ),
                                                            id="update-datetime",
                                                            type="secondary",
                                                        ),
                                                    ]
                                                )
                                            ],
                                            style={"width": "100%", "display": "flex", "alignItems": "center"}
                                        )
                                    ),
                                    span=24,
                                ),
                                # 展示列车图
                                fac.AntdCol(
                                    blank_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        children=fac.AntdSpace(
                                            [
                                                # 地铁列车图 - 六节车厢（图片拼接版）
                                                html.Div(
                                                    style={
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "padding": "5px",
                                                        "width": "100%"
                                                    },
                                                    children=[
                                                        # 车头（左侧图片）
                                                        html.Img(
                                                            src="/assets/imgs/train_headL.png",  # 车头左侧图片
                                                            style={
                                                                "flex": "0 0 44px",
                                                                "height": "74px",
                                                                "borderRadius": "8px 0 0 8px",
                                                                "objectFit": "cover"  # 保持图片比例并填充容器
                                                            }
                                                        ),
                                                        # 车厢1-6（每节由左右图片拼接）
                                                        *[html.Div(
                                                            style={
                                                                "flex": "1 1 auto",  # 等比例分配剩余空间
                                                                "minWidth": "60px",  # 最小宽度限制，防止过度压缩
                                                                "height": "74px",
                                                                "display": "flex",  # 启用flex布局拼接左右图片
                                                                "borderLeft": "0px dashed white"  # 车厢间分隔线
                                                            },
                                                            children=[
                                                                # 车厢左侧图片
                                                                html.Img(
                                                                    src="/assets/imgs/train_bodyL.png",
                                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                                ),
                                                                # 车厢右侧图片
                                                                html.Img(
                                                                    src="/assets/imgs/train_bodyR.png",
                                                                    style={"width": "50%", "height": "100%", "objectFit": "cover"}
                                                                )
                                                            ]
                                                        ) for i in range(6)],  # 6节车厢
                                                        # 车尾（右侧图片）
                                                        html.Img(
                                                            src="/assets/imgs/train_headR.png",  # 车尾右侧图片
                                                            style={
                                                                "flex": "0 0 44px",
                                                                "height": "74px",
                                                                "borderRadius": "0 8px 8px 0",
                                                                "borderLeft": "0px dashed white",  # 与前一节车厢分隔
                                                                "objectFit": "cover"
                                                            }
                                                        )
                                                    ]
                                                )
                                            ],
                                            style={"width": "100%", "display": "flex", "justifyContent": "center", "alignItems": "center", "padding": "5px"}
                                        )
                                    ),
                                    span=24,
                                ),
                                # 指标卡片示例
                                fac.AntdCol(
                                    index_card(  # 移除外层html.Div包裹
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        indexNameStyle={"color": themetoken["colorText"]},
                                        footerContentStyle={"color": themetoken["colorText"]},
                                        extraContentStyle={"color": themetoken["colorText"]},
                                        index_name="当日销售额",
                                        index_value=[
                                            "¥ ",
                                            html.Span(
                                                102389,
                                                id="today-sales"
                                                # 移除指标值颜色style
                                            ),
                                        ],
                                        index_description="这是当日销售额的指标描述示例内容",
                                        footer_content="昨日销售额 ￥123456",
                                        # 移除卡片style参数
                                    ),
                                    span=6,
                                ),
                                fac.AntdCol(
                                    index_card(  # 移除外层html.Div包裹
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        indexNameStyle={"color": themetoken["colorText"]},
                                        footerContentStyle={"color": themetoken["colorText"]},
                                        extraContentStyle={"color": themetoken["colorText"]},
                                        index_name="当日访问量",
                                        index_value=html.Span(
                                            fuc.FefferyCountUp(end=8846, separator=""),
                                            id="today-visits",
                                        ),
                                        index_description="这是当日访问量的指标描述示例内容",
                                        extra_content=fact.AntdTinyArea(
                                            id="today-visits-chart",
                                            data=[
                                                random.randint(20, 50) for _ in range(10)
                                            ],
                                            height=60,
                                            smooth=True,
                                        ),
                                        footer_content="昨日访问量 6789",
                                    ),
                                    span=6,
                                ),
                                fac.AntdCol(
                                    index_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        indexNameStyle={"color": themetoken["colorText"]},
                                        footerContentStyle={"color": themetoken["colorText"]},
                                        extraContentStyle={"color": themetoken["colorText"]},
                                        index_name="当日支付笔数",
                                        index_value=html.Span(
                                            4678,
                                            id="today-orders",
                                        ),
                                        index_description="这是当日支付笔数的指标描述示例内容",
                                        extra_content=fact.AntdTinyColumn(
                                            id="today-orders-chart",
                                            data=[
                                                random.randint(50, 100) for _ in range(10)
                                            ],
                                            height=60,
                                            color="#2389ff",
                                            columnWidthRatio=0.75,
                                        ),
                                        footer_content="昨日支付笔数 5678",
                                    ),
                                    span=6,
                                ),
                                fac.AntdCol(
                                    index_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        indexNameStyle={"color": themetoken["colorText"]},
                                        footerContentStyle={"color": themetoken["colorText"]},
                                        extraContentStyle={"color": themetoken["colorText"]},
                                        index_name="当日活动转化率",
                                        index_value=html.Span(
                                            "78%",
                                            id="today-conversion-rate",
                                        ),
                                        index_description="这是运营活动效果的指标描述示例内容",
                                        extra_content=fac.AntdCenter(
                                            fac.AntdProgress(
                                                id="today-conversion-rate-chart",
                                                percent=78,
                                                status="active",
                                                strokeColor={
                                                    "from": "#128ee7",
                                                    "to": "#6cc085",
                                                },
                                            ),
                                            style=style(height="100%"),
                                        ),
                                        footer_content="昨日活动转化率 75%",
                                    ),
                                    span=6,
                                ),
                                # 图表卡片示例
                                fac.AntdCol(
                                    simple_chart_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        titleStyle={"color": themetoken["colorText"]},
                                        descriptionStyle={"color": themetoken["colorText"]},
                                        title="销售额类别占比",
                                        description="时间范围：今日",
                                        chart=fact.AntdPie(
                                            id="today-sales-class-chart",
                                            data=[
                                                {
                                                    "type": "家用电器",
                                                    "value": 4544,
                                                },
                                                {
                                                    "type": "食用酒水",
                                                    "value": 3321,
                                                },
                                                {
                                                    "type": "个护健康",
                                                    "value": 3113,
                                                },
                                                {
                                                    "type": "服饰箱包",
                                                    "value": 2341,
                                                },
                                                {
                                                    "type": "母婴产品",
                                                    "value": 1231,
                                                },
                                                {
                                                    "type": "其他",
                                                    "value": 1231,
                                                },
                                            ],
                                            colorField="type",
                                            angleField="value",
                                            radius=0.8,
                                            innerRadius=0.6,
                                            label={"type": "spider"},
                                        ),
                                        height=350,
                                    ),
                                    span=6,
                                ),
                                # 新增词云图卡片 1
                                fac.AntdCol(
                                    simple_chart_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        titleStyle={"color": themetoken["colorText"]},
                                        descriptionStyle={"color": themetoken["colorText"]},
                                        title="热门搜索词云",
                                        description="时间范围：今日",
                                        chart=fact.AntdWordCloud(
                                            id="today-hot-search-wordcloud",
                                            data=[
                                                {"name": f"关键词{i}", "value": random.randint(10, 100)}
                                                for i in range(1, 31)
                                            ],
                                            wordField="name",
                                            weightField="value",
                                            height=400,
                                            color="#1890ff"
                                        ),
                                        height=350,
                                    ),
                                    span=6,
                                ),
                                # 新增词云图卡片 2
                                fac.AntdCol(
                                    simple_chart_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        titleStyle={"color": themetoken["colorText"]},
                                        descriptionStyle={"color": themetoken["colorText"]},
                                        title="用户评论词云",
                                        description="时间范围：今日",
                                        chart=fact.AntdWordCloud(
                                            id="today-user-comment-wordcloud",
                                            data=[
                                                {"name": f"评价词{i}", "value": random.randint(10, 100)}
                                                for i in range(1, 31)
                                            ],
                                            wordField="name",
                                            weightField="value",
                                            height=400,
                                            color="#722ed1"
                                        ),
                                        height=350,
                                    ),
                                    span=6,
                                ),

                                fac.AntdCol(
                                    simple_chart_card(
                                        rootStyle={"background": themetoken["colorBgCard"]},
                                        titleStyle={"color": themetoken["colorText"]},
                                        descriptionStyle={"color": themetoken["colorText"]},
                                        title="流量转化情况",
                                        description="时间范围：今日",
                                        chart=fact.AntdColumn(
                                            id="today-conversion-chart",
                                            data=[
                                                {
                                                    "action": "浏览网站",
                                                    "pv": 50000,
                                                },
                                                {
                                                    "action": "放入购物车",
                                                    "pv": 35000,
                                                },
                                                {
                                                    "action": "生成订单",
                                                    "pv": 25000,
                                                },
                                                {
                                                    "action": "支付订单",
                                                    "pv": 15000,
                                                },
                                                {
                                                    "action": "完成交易",
                                                    "pv": 8500,
                                                },
                                            ],
                                            xField="action",
                                            yField="pv",
                                            conversionTag={},
                                            color="#2e8fff",
                                        ),
                                        height=350,
                                    ),
                                    span=6,
                                ),
                            ],
                            gutter=[10, 10],
                        ),
                    ],
                    style=style(
                        padding=15,
                        # 移除固定background="#f5f5f5"，由主题令牌控制
                        #background="#f5f5f5",
                        background=themetoken["colorBgContainer"],
                        #background="#141414",
                        minHeight="100vh",
                        boxSizing="border-box"
                    ),
                ),
            ],
            direction="vertical",
            style=style(width="100%"),
        )
    )

