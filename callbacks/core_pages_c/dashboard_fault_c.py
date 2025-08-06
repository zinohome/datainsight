import random
from datetime import datetime
from dash import Input, Output, callback

# 页面数据更新回调
@callback(
    Output('fault_update-datetime', 'children'),
    Input('fault_update-data-interval', 'n_intervals'),
    prevent_initial_call=False,
)
def update_dashboard_data(n_intervals):
    # 更新故障图页面数据
    # 更新时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        current_time,
    )