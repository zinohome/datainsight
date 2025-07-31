from dash import html
import feffery_antd_components as fac
import feffery_antd_charts as fact  # 修正：使用正确的库名和别名
from feffery_dash_utils.style_utils import style


def render():
    """数据大屏-折线图页面"""

    return html.Div(
        [
            fac.AntdBreadcrumb(items=[{"title": "数据大屏"}, {"title": "折线图展示"}]),
            fac.AntdTitle("数据可视化大屏", level=2, style=style(textAlign="center", margin="20px 0")),

            # 数据大屏内容区域
            fac.AntdGrid(
                [
                    # 顶部KPI指标卡片
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                fac.AntdCard(
                                    [
                                        fac.AntdText("总访问量", style=style(fontSize=14, color="#666")),
                                        fac.AntdText("1,234,567", strong=True, style=style(fontSize=28, color="#1890ff", marginTop=8))
                                    ],
                                    style=style(height=120, display="flex", flexDirection="column", justifyContent="center", padding="0 20px")
                                ),
                                xs=24, sm=12, md=6, lg=6
                            ),
                            # ... 可添加更多KPI卡片 ...
                        ],
                        gutter=16,
                        style=style(marginBottom=16)
                    ),

                    # 折线图区域
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                # 修正：将fcc改为fact
                                fact.FefferyLine(
                                    data=[
                                        {"x": "1月", "y": 120},
                                        {"x": "2月", "y": 210},
                                        {"x": "3月", "y": 180},
                                        {"x": "4月", "y": 240},
                                        {"x": "5月", "y": 300},
                                        {"x": "6月", "y": 270},
                                    ],
                                    xField="x",
                                    yField="y",
                                    height=400,
                                    title="月度数据趋势"
                                ),
                                xs=24
                            )
                        ]
                    )
                ],
                style=style(padding="20px")
            )
        ],
        style=style(width="100%", height="100%", backgroundColor="#f5f5f5")
    )
