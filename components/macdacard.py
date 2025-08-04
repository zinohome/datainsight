from dash import html
from typing import Union
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style
from dash.development.base_component import Component

_Component = Union[Component, str, int, float, list]


def macda_card(
        title: _Component = None,
        description: _Component = None,
        chart: _Component = None,
        extra: _Component = None,
        height: Union[int, float, str] = 300,
        root_id: Union[str, dict] = None,
        rootStyle: dict = None,
        rootClassName: str = None,
        titleStyle: dict = None,
        titleClassName: str = None,
        descriptionStyle: dict = None,
        descriptionClassName: str = None,
) -> Component:
    """MACDA风格图表卡片（默认顶部对齐）

    基于simple_chart_card改造，强制图表区域内容顶部对齐

    Args:
        title: 标题元素
        description: 标题右侧辅助描述
        chart: 图表内容元素
        extra: 额外操作区元素
        height: 卡片高度，默认300
        root_id: 根元素id
        rootStyle: 根元素样式
        rootClassName: 根元素类名
        titleStyle: 标题样式
        titleClassName: 标题类名
        descriptionStyle: 描述样式
        descriptionClassName: 描述类名

    Returns:
        Component: 构造完成的顶部对齐图表卡片
    """
    return html.Div(
        fac.AntdFlex(
            [
                # 标题区域（与simple_chart_card保持一致）
                fac.AntdFlex(
                    [
                        fac.AntdSpace(
                            [
                                # 新增容器：统一控制图标和标题的文本颜色
                                html.Div(
                                    [
                                        fac.AntdIcon(
                                            icon="antd-menu",
                                            style={
                                                "marginRight": 4,
                                                "color": "inherit",  # 继承容器文本颜色
                                                "fontSize": 14,
                                                "verticalAlign": "baseline"
                                            }
                                        ),
                                        fac.AntdText(
                                            title,
                                            strong=True,
                                            className=titleClassName,
                                            style={
                                                **dict(fontSize=14),
                                                **(titleStyle or {}),
                                            },
                                        ),
                                    ],
                                    # 容器文本颜色 = 标题文本颜色（优先取 titleStyle 中的 color，无则用默认文本色）
                                    style={"color": (titleStyle or {}).get("color", "rgba(0, 0, 0, 0.85)")}
                                ),
                                (
                                        description
                                        and fac.AntdText(
                                    description,
                                    type='secondary',
                                    className=descriptionClassName,
                                    style=descriptionStyle,
                                )
                                ),
                            ],
                            size=4,
                            align='baseline',
                        ),
                        extra,
                    ],
                    justify='space-between',
                ),
                # 分隔线
                fac.AntdDivider(
                    lineColor='#dae0ea',
                    style=style(marginTop=6,
                                marginBottom=6,
                                borderTopWidth=1),
                    size="small",
                ),
                # 图表区域（核心修改：强制顶部对齐）
                html.Div(
                    chart,
                    style=style(
                        height='100%',
                        flex=1,
                        minHeight=0,
                        display='flex',  # 启用flex布局
                        flexDirection='column',  # 纵向排列
                        justifyContent='flex-start',  # 强制内容顶部对齐
                        alignItems='stretch',  # 拉伸子元素宽度
                        marginTop=0  # 移除顶部间距
                    )
                ),
            ],
            vertical=True,
            gap=0,
            style=style(width='100%', height='100%'),
        ),
        className=rootClassName,
        style={
            **dict(
                height=height,
                padding=20,
                background='#fff',
                borderRadius=8,
                boxSizing='border-box',
                boxShadow='0 1px 2px 0 rgba(0, 0, 0, 0.03),0 1px 6px -1px rgba(0, 0, 0, 0.02),0 2px 4px 0 rgba(0, 0, 0, 0.02)',
            ),
            **(rootStyle or {}),
        },
        **(dict(id=root_id) if root_id else {}),
    )