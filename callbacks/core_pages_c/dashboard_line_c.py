import dash
import random
from datetime import datetime
import feffery_antd_components as fac
from dash import set_props, Patch, callback
from dash.dependencies import Output, Input, State
from server import app
from dash.dependencies import Output, Input, State

@app.callback(
    [
        Output("today-sales-class-chart", "data"),
        Output("today-conversion-chart", "data"),
    ],
    Input("update-data-interval", "n_intervals"),
    [
        State("today-sales-class-chart", "data"),
        State("today-conversion-chart", "data"),
    ],
    prevent_initial_call=True,
)
def update_dashboard_data(
    n_intervals,
    origin_today_sales_class_chart_data,
    origin_today_conversion_chart_data,
):
    """处理仪表盘中各目标的实时数据更新"""
    # 销售额类别占比
    for i in range(len(origin_today_sales_class_chart_data)):
        origin_today_sales_class_chart_data[i]["value"] += random.randint(5, 20)

    # 流量转化情况
    for i in range(len(origin_today_conversion_chart_data)):
        origin_today_conversion_chart_data[i]["pv"] += random.randint(10, 20)

    return [
        origin_today_sales_class_chart_data,
        origin_today_conversion_chart_data,
    ]
