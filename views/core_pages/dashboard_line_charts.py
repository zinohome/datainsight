import random
from datetime import datetime
from dash import html, dcc
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    blank_card,
    index_card,
    simple_chart_card,
)

from components.macdacard import macda_card


def render(themetoken):
    """数据大屏-折线图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="update-data-interval",
            interval=3000,  # 示例，每1秒更新一次
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
                    style={'display': 'none'}
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
                            style={"width": "100%", "display": "flex", "justifyContent": "center",
                                   "alignItems": "center", "padding": "5px"}
                        )
                    ),
                    span=24,
                ),

                # 列车在线情况
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="列车在线情况",
                        chart=fac.AntdRow(
                            [
                                # 圆环1
                                fac.AntdCol(
                                    fact.AntdPie(
                                        id="today-hot-search-wordcloud-chart",
                                        key="dfdfsfsfds",
                                        data=[{"value": 75}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{75}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex",
                                           "justifyContent": "center",
                                           "alignItems": "flex-start",
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                ),
                                # 圆环2
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 60}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{60}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex",
                                           "justifyContent": "center",
                                           "alignItems": "flex-start",
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                ),
                                # 圆环3
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 85}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{85}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex",
                                           "justifyContent": "center",
                                           "alignItems": "flex-start",
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                ),
                                # 圆环4
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 90}],
                                        angleField="value",
                                        radius=0.75,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线\n{90}",
                                            "autoAdjust": True,
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center",
                                                "whiteSpace": "pre"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex",
                                           "justifyContent": "center",
                                           "alignItems": "flex-start",
                                           "padding": "10px 10px 0",
                                           "height": "100%"}
                                )
                            ],
                            style={"height": "100px",
                                   "alignItems": "flex-start",
                                    "margin": 0,
                                    "padding": 0}
                        ),
                        height=350,
                    ),
                    span=6,
                ),
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="故障/预警",
                        chart=fac.AntdTable(
                            columns=[
                                {'title': f'字段{i}',
                                 'dataIndex': f'字段{i}',
                                 'width': width,
                                 'headerCellStyle': {
                                     'fontWeight': 'bold',  # 表头文字加粗
                                     'borderRight': 'none'  # 隐藏表头单元格右侧竖线
                                 },
                                 # 单元格样式：隐藏右侧竖线
                                 'cellStyle': {
                                     'borderRight': 'none',  # 清除所有默认边框
                                     'borderBottom': '1px solid #e8e8e8'
                                 }
                                 }
                                for i, width in zip(
                                    range(1, 5), ['25%', '25%', '25%', '25%']
                                )
                            ],
                            data=[{f'字段{i}': '示例内容' for i in range(1, 5)}] * 3,
                            size="small",
                            bordered=False,
                            maxHeight=150,
                            maxWidth='max-content',
                            pagination=False,
                            style={
                                'border': 'none'
                            },
                        ),
                        height=350,
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
                    macda_card(
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
                    macda_card(
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
                # 环形图卡片
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="用户评论词云",
                        description="时间范围：今日",
                        chart=fac.AntdRow(
                            [
                                # 圆环1
                                fac.AntdCol(
                                    fact.AntdPie(
                                        id="today-hot-search-wordcloud-chart",
                                        key="dfdfsfsfds",
                                        data=[{"value": 75}],
                                        angleField="value",
                                        radius=0.3,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线：{75}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex", "justifyContent": "center", "alignItems": "center",
                                           "padding": "10px"}
                                ),
                                # 圆环2
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 60}],
                                        angleField="value",
                                        radius=0.3,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线：{60}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex", "justifyContent": "center", "alignItems": "center",
                                           "padding": "10px"}
                                ),
                                # 圆环3
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 85}],
                                        angleField="value",
                                        radius=0.3,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线：{85}",
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex", "justifyContent": "center", "alignItems": "center",
                                           "padding": "10px"}
                                ),
                                # 圆环4
                                fac.AntdCol(
                                    fact.AntdPie(
                                        data=[{"value": 90}],
                                        angleField="value",
                                        radius=0.3,  # 外半径设为0.3
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{
                                            "type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线列车\n{90}",
                                            "autoAdjust": True,
                                            "style": {
                                                "fill": "white",
                                                "fontSize": 12,
                                                "textAlign": "center",
                                                "whiteSpace": "pre"
                                            }
                                        }]
                                    ),
                                    span=6,
                                    style={"display": "flex", "justifyContent": "center", "alignItems": "center",
                                           "padding": "10px"}
                                )
                            ],
                            style={"height": "100%"}
                        ),
                        height=350,
                    ),
                    span=6,
                ),

                fac.AntdCol(
                    macda_card(
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
        )
    ]
