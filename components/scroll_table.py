import dash
from dash import html, dcc, callback, Output, Input, State
from dash.dependencies import ClientsideCallback
import feffery_antd_components as fac
from typing import List, Dict, Optional, Union, Any

class ScrollTable:
    """
    自动上下滚动的AntdTable组件
    实现表格内容的自动滚动效果，支持自定义滚动速度、方向和循环模式
    """
    def __init__(
        self,
        id: str,
        columns: List[Dict],
        data: List[Dict],
        scroll_speed: int = 50,
        scroll_direction: str = 'down',
        cycle: bool = True,
        height: str = '500px',
        **kwargs
    ):
        """
        参数:
            id: 组件唯一标识
            columns: 表格列配置，同AntdTable
            data: 表格数据，同AntdTable
            scroll_speed: 滚动速度，单位为毫秒/步
            scroll_direction: 滚动方向，'up'或'down'
            cycle: 是否循环滚动
            height: 表格容器高度
            **kwargs: 传递给AntdTable的其他参数
        """
        self.id = id
        self.columns = columns
        self.data = data
        self.scroll_speed = scroll_speed
        self.scroll_direction = scroll_direction
        self.cycle = cycle
        self.height = height
        self.kwargs = kwargs
        self.container_id = f"{id}-container"
        self.interval_id = f"{id}-interval"

    def render(self):
        # 添加一个隐藏的dummy组件用于回调输出
        dummy_component_id = f"{self.id}-dummy"
        
        """渲染组件"""
        return html.Div(
            [
                html.Div(
                    fac.AntdTable(
                        id=self.id,
                        columns=self.columns,
                        data=self.data,
                        **self.kwargs
                    ),
                    id=self.container_id,
                    style={
                        'height': self.height,
                        'overflow': 'auto',
                        'position': 'relative'
                    }
                ),
                dcc.Interval(
                id=self.interval_id,
                interval=self.scroll_speed,
                n_intervals=0
            ),
            # 隐藏的dummy组件，用于接收回调输出
            html.Div(id=dummy_component_id, style={'display': 'none'})
            ]
        )

    def register_callbacks(self, app: dash.Dash):
        """注册回调函数"""
        # 客户端回调实现滚动逻辑
        # 注册客户端回调实现滚动逻辑
        ClientsideCallback(
            # 使用模板字符串格式化组件ID
            """
            function(n_intervals, direction, cycle, containerId) {
from dash import html, dcc, callback, Output, Input, State, ClientsideCallback                // 获取容器元素
                const container = document.getElementById(containerId);
                if (!container) return {};

                // 获取表格主体元素
                const tableBody = container.querySelector('.ant-table-body');
                if (!tableBody) return {};

                // 计算滚动相关参数
                const currentScrollTop = tableBody.scrollTop;
                const scrollHeight = tableBody.scrollHeight;
                const clientHeight = tableBody.clientHeight;
                const maxScroll = scrollHeight - clientHeight;

                // 计算新的滚动位置
                let newScrollTop;
                if (direction === 'down') {
                    newScrollTop = currentScrollTop + 1;
                    // 到达底部时根据循环设置决定是否回到顶部
                    if (newScrollTop >= maxScroll) {
                        newScrollTop = cycle ? 0 : maxScroll;
                    }
                } else {
                    newScrollTop = currentScrollTop - 1;
                    // 到达顶部时根据循环设置决定是否回到底部
                    if (newScrollTop <= 0) {
                        newScrollTop = cycle ? maxScroll : 0;
                    }
                }

                // 设置新的滚动位置
                tableBody.scrollTop = newScrollTop;
                return {};
            }
            """,
            Output(f"{self.id}-dummy", 'children'),
              Input(self.interval_id, 'n_intervals'),
              State(self.id, 'scroll_direction'),
              State(self.id, 'cycle'),
              State(self.container_id, 'id'),
            prevent_initial_call=True
        )

# 示例使用代码
"""
使用示例:

from components.scroll_table import ScrollTable

scroll_table = ScrollTable(
    id='my-scroll-table',
    columns=[
        {'title': '姓名', 'dataIndex': 'name', 'key': 'name'},
        {'title': '年龄', 'dataIndex': 'age', 'key': 'age'},
    ],
    data=[
        {'key': '1', 'name': '张三', 'age': 32},
        {'key': '2', 'name': '李四', 'age': 45},
        # 更多数据...
    ],
    scroll_speed=50,
    height='400px'
)

app.layout = html.Div([scroll_table.render()])
scroll_table.register_callbacks(app)
"""