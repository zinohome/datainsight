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

def render():
    """仪表盘渲染示例"""

    return fac.AntdSpace(
        [
            fac.AntdBreadcrumb(items=[{"title": "主要页面"}, {"title": "仪表盘"}]),
            html.Div(
                [
                    # 消息提示输出目标
                    fac.Fragment(id="message-target"),
                    # 数据统一更新轮询
                    dcc.Interval(
                        id="update-data-interval",
                        interval=1000,  # 示例，3秒更新一次
                    ),
                    # 仪表盘网格布局
                    fac.AntdRow(
                        [
                            # 欢迎卡片
                            fac.AntdCol(
                                welcome_card(
                                    title="欢迎访问本应用，用户：张三",
                                    description=fac.AntdText(
                                        [
                                            "您有5个事项待处理，点击",
                                            html.A("此处", id="demo-link1"),
                                            "查看。",
                                        ]
                                    ),
                                    avatar=fac.AntdAvatar(
                                        src="/assets/imgs/demo-avatar.png",
                                        mode="image",
                                        size=72,
                                        style=style(background="#1890ff"),
                                    ),
                                    extra=fac.AntdButton(
                                        "更多信息", id="demo-link2", type="link"
                                    ),
                                ),
                                span=24,
                            ),
                            # 展示数据更新时间
                            fac.AntdCol(
                                blank_card(
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
                                ),
                                span=24,
                            ),
                            # 指标卡片示例
                            fac.AntdCol(
                                index_card(
                                    index_name="当日销售额",
                                    index_value=[
                                        "¥ ",
                                        html.Span(
                                            102389,
                                            id="today-sales",
                                        ),
                                    ],
                                    index_description="这是当日销售额的指标描述示例内容",
                                    footer_content="昨日销售额 ￥123456",
                                ),
                                span=6,
                            ),
                            fac.AntdCol(
                                index_card(
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
                                    height=450,
                                ),
                                span=12,
                            ),
                            fac.AntdCol(
                                simple_chart_card(
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
                                    height=450,
                                ),
                                span=12,
                            ),
                            # 空白卡片示例
                            fac.AntdCol(
                                blank_card(
                                    fac.AntdCenter(
                                        fac.AntdText(
                                            [
                                                fac.AntdText("玩转Dash", italic=True),
                                                "知识星球出品",
                                            ]
                                        )
                                    )
                                ),
                                span=24,
                            ),
                        ],
                        gutter=[18, 18],
                    ),
                ],
                style=style(
                    padding=50,
                    background="#f5f5f5",
                    minHeight="100vh",
                    boxSizing="border-box",
                ),
            ),
        ],
        direction="vertical",
        style=style(width="100%"),
    )
