import random
from datetime import datetime
from dash import Input, Output, callback

# 页面数据更新回调
@callback(
    Output('param_update-datetime', 'children'),
    Output('param_operation-data-chart', 'data'),
    Input('param_update-data-interval', 'n_intervals'),
    prevent_initial_call=False,
)
def update_dashboard_data(n_intervals):
    """更新参数图页面数据"""
    # 更新时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 运行数据
    operation_data = []
    for i in range(0, 24, 2):
        time = f"{i}:00"
        speed = random.randint(30, 80)
        temperature = random.randint(20, 30)
        operation_data.extend([
            {"time": time, "type": "speed", "value": speed},
            {"time": time, "type": "temperature", "value": temperature}
        ])

    return (
        current_time,
        operation_data,
    )