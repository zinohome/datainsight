from dash import html, dcc
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style


def horizontal_timeline(
        items,
        mode='center',
        reverse=False,
        item_gap=20,
        line_color=None,
        themetoken=None
):
    """
    横向时间轴组件

    参数:
    - items: 时间轴项列表，格式同AntdTimeline
    - mode: 对齐方式，可选'left'/'center'/'right'
    - reverse: 是否反转顺序
    - item_gap: 时间轴项间距(px)
    - line_color: 连接线颜色，默认使用主题色
    - themetoken: 主题令牌，用于样式适配
    """
    # 处理反转
    display_items = items[::-1] if reverse else items

    # 主题适配
    if not line_color and themetoken:
        line_color = themetoken.get('colorPrimary', '#1890ff')

    # 构建时间轴项
    timeline_items = []
    for i, item in enumerate(display_items):
        # 连接线样式
        line_style = {
            'flex': '1 1 auto',
            'height': '1px',
            'background': line_color or '#e8e8e8',  # 确保默认颜色
            'alignSelf': 'center',
            'minWidth': '20px'  # 新增：设置最小宽度，防止被完全挤压
        }

        # 节点样式
        dot_style = {
            'width': '12px',
            'height': '12px',
            'borderRadius': '50%',
            'background': item.get('color', line_color),
            # 移除节点左右margin，消除间隙
            'margin': '0',  # 修改前：f'0 {item_gap // 2}px'
            'alignSelf': 'center'
        }

        # 时间轴项内容
        item_content = html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': mode,
                'minWidth': '100px',
                'maxWidth': '100px',  # 新增：限制项容器最大宽度，防止内容过宽
                'margin': f'0 {item_gap // 2}px',
                'flexShrink': 0  # 新增：防止项容器被压缩
            },
            children=[
                # 标签
                html.Div(
                    item.get('label', ''),
                    style={
                        'marginBottom': '8px',
                        'color': themetoken.get('colorText') if themetoken else '#333',
                        'overflow': 'hidden',  # 新增：防止标签文本溢出
                        'textOverflow': 'ellipsis',
                        'whiteSpace': 'nowrap'
                    }
                ),
                # 图标/节点
                html.Div(
                    item.get('icon', html.Div(style=dot_style)),
                    style={'marginBottom': '8px'}
                ),
                # 内容
                html.Div(
                    item.get('content', ''),
                    style={
                        'color': themetoken.get('colorTextSecondary') if themetoken else '#666',
                        'overflow': 'hidden',  # 新增：防止内容文本溢出
                        'textOverflow': 'ellipsis',  # 文本过长时显示省略号
                        'whiteSpace': 'nowrap',  # 强制单行显示
                        'fontSize': '12px'  # 可选：缩小字体进一步防止溢出
                    }
                )
            ]
        )

        timeline_items.append(item_content)

        # 添加连接线（最后一项不加）
        if i < len(display_items) - 1:
            timeline_items.append(html.Div(style=line_style))

    # 容器样式
    container_style = {
        'display': 'flex',
        'alignItems': 'center',
        'width': '100%',
        'minWidth': 'fit-content',  # 新增：确保容器宽度足够容纳所有内容
        'padding': '20px 0',
        'overflowX': 'auto'  # 支持横向滚动
    }

    return html.Div(
        style=container_style,
        children=timeline_items
    )