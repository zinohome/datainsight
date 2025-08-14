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
from views.core_pages.train_chart_link import create_train_chart_link


def render(themetoken):
    """数据大屏-车厢图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="carriage_update-data-interval",
            interval=3000,  # 示例，每3秒更新一次
        ),
        # 添加主题模式存储 - 初始设为深色
        dcc.Store(id="theme-mode-store", data="dark"),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 展示数据更新时间
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量
                        children=fac.AntdSpace(
                            [
                                fac.AntdText(
                                    [
                                        "数据最近更新时间：",
                                        fac.AntdText(
                                            datetime.now().strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                            id="carriage_update-datetime",
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
                # 展示车厢图
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]}, 
                        children=fac.AntdSpace(
                            [
                                # 地铁列车图 - 六节车厢（图片拼接版）
                                create_train_chart_link(themetoken)
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
                        title="车厢在线情况",
                        chart=fac.AntdRow(
                            [
                                # 圆环1
                                fac.AntdCol(
                                    fact.AntdPie(
                                        id="carriage_online-chart-1",
                                        data=[{"value": 75}],
                                        angleField="value",
                                        radius=0.75,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_online-chart-2",
                                        data=[{"value": 60}],
                                        angleField="value",
                                        radius=0.75,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_online-chart-3",
                                        data=[{"value": 85}],
                                        angleField="value",
                                        radius=0.75,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_online-chart-4",
                                        data=[{"value": 90}],
                                        angleField="value",
                                        radius=0.75,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                # 空调故障
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="空调故障",
                        description=html.A(
                            "一期故障",
                            href="https://www.baidu.com",
                            target="_blank",
                            style={"textDecoration": "none"}
                        ),
                        chart=fac.AntdTable(
                            columns=[
                                {'title': f'字段{i}',
                                 'dataIndex': f'字段{i}',
                                 'width': width,
                                 'headerCellStyle': {
                                     'fontWeight': 'bold',
                                     'borderRight': 'none'
                                 },
                                 'cellStyle': {
                                     'borderRight': 'none',
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
                # 空调预警
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="空调预警",
                        chart=fac.AntdTable(
                            columns=[
                                {'title': f'字段{i}',
                                 'dataIndex': f'字段{i}',
                                 'width': width,
                                 'headerCellStyle': {
                                     'fontWeight': 'bold',
                                     'borderRight': 'none'
                                 },
                                 'cellStyle': {
                                     'borderRight': 'none',
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
                # 部件寿命
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="部件寿命",
                        chart=fac.AntdTable(
                            columns=[
                                {'title': f'字段{i}',
                                 'dataIndex': f'字段{i}',
                                 'width': width,
                                 'headerCellStyle': {
                                     'fontWeight': 'bold',
                                     'borderRight': 'none'
                                 },
                                 'cellStyle': {
                                     'borderRight': 'none',
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
                # 销售额类别占比
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="销售额类别占比",
                        description="时间范围：今日",
                        chart=fact.AntdPie(
                            id="carriage_today-sales-class-chart",
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
                # 热门搜索词云
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="热门搜索词云",
                        description="时间范围：今日",
                        chart=fact.AntdWordCloud(
                            id="carriage_today-hot-search-wordcloud",
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
                # 用户评论词云
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
                                        id="carriage_today-comment-wordcloud-chart-1",
                                        data=[{"value": 75}],
                                        angleField="value",
                                        radius=0.3,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_today-comment-wordcloud-chart-2",
                                        data=[{"value": 60}],
                                        angleField="value",
                                        radius=0.3,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_today-comment-wordcloud-chart-3",
                                        data=[{"value": 85}],
                                        angleField="value",
                                        radius=0.3,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
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
                                        id="carriage_today-comment-wordcloud-chart-4",
                                        data=[{"value": 90}],
                                        angleField="value",
                                        radius=0.3,
                                        innerRadius=0.75,
                                        color="#52c41a",
                                        tooltip=False,
                                        statistic=False,
                                        label=False,
                                        annotations=[{"type": "text",
                                            "position": ["50%", "50%"],
                                            "content": f"在线车厢\n{90}",
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
                # 流量转化情况
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="流量转化情况",
                        description="时间范围：今日",
                        chart=fact.AntdColumn(
                            id="carriage_today-conversion-chart",
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
                # 车厢运行数据
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="车厢运行数据",
                        chart=fact.AntdLine(
                            id="carriage_operation-data-chart",
                            data=(lambda: [
                                item for i in range(0, 24, 2)
                                for item in [
                                    {"time": f"{i}:00", "type": "speed", "value": random.randint(30, 80)},
                                    {"time": f"{i}:00", "type": "temperature", "value": random.randint(20, 30)}
                                ]
                            ])(),
                            xField="time",
                            yField="value",
                            seriesField="type",
                            smooth=True,
                            color=["#1890ff", "#faad14"],
                        ),
                        height=350,
                    ),
                    span=12,
                ),
                # 能耗统计
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="车厢能耗统计",
                        chart=fact.AntdColumn(
                            id="carriage_energy-chart",
                            data=[
                                {"day": f"{i}日", "energy": random.randint(500, 1000)}
                                for i in range(1, 8)
                            ],
                            xField="day",
                            yField="energy",
                            color="#52c41a",
                        ),
                        height=350,
                    ),
                    span=12,
                ),
            ],
            gutter=[10, 10],
        )
    ]