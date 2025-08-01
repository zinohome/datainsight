import dash
import random
from datetime import datetime
import feffery_antd_components as fac
from dash import set_props, Patch
from dash.dependencies import Input, Output, State

from server import app

@app.callback(
    [
        Output("update-datetime", "children"),
        Output("today-sales", "children"),
        Output("today-visits", "children"),
        Output("today-visits-chart", "data"),
        Output("today-orders", "children"),
        Output("today-orders-chart", "data"),
        Output("today-conversion-rate", "children"),
        Output("today-conversion-rate-chart", "percent"),
        Output("today-sales-class-chart", "data"),
        Output("today-conversion-chart", "data"),
    ],
    Input("update-data-interval", "n_intervals"),
    [
        State("today-sales", "children"),
        State("today-visits", "children"),
        State("today-orders", "children"),
        State("today-conversion-rate-chart", "percent"),
        State("today-sales-class-chart", "data"),
        State("today-conversion-chart", "data"),
    ],
    prevent_initial_call=True,
)
def update_dashboard_data(
    n_intervals,
    origin_today_sales,
    origin_today_visits,
    origin_today_orders,
    origin_today_conversion_rate,
    origin_today_sales_class_chart_data,
    origin_today_conversion_chart_data,
):
    """处理仪表盘中各目标的实时数据更新"""

    # 模拟最新实时数据的获取

    # 当日销售额
    next_today_sales = origin_today_sales + random.randint(50, 100)

    # 当日访问量
    today_visits_chunk = random.randint(20, 50)
    # 更新数字递增组件参数
    origin_today_visits["props"]["start"] = origin_today_visits["props"]["end"]
    origin_today_visits["props"]["end"] = (
        origin_today_visits["props"]["end"] + today_visits_chunk
    )
    next_today_visits = origin_today_visits

    # 当日访问量分时段图表数据
    today_visits_chart_data_patch = Patch()
    today_visits_chart_data_patch.append(today_visits_chunk)

    # 当日订单量
    today_orders_chunk = random.randint(50, 100)
    next_today_orders = origin_today_orders + today_orders_chunk

    # 当日订单量分时段图表数据
    today_orders_chart_data_patch = Patch()
    today_orders_chart_data_patch.append(today_orders_chunk)

    # 当日活动转化率
    next_today_conversion_rate = round(
        origin_today_conversion_rate + random.uniform(-1, 1), 1
    )
    # 修正模拟数据
    if next_today_conversion_rate > 100:
        next_today_conversion_rate = 100

    # 销售额类别占比
    for i in range(len(origin_today_sales_class_chart_data)):
        origin_today_sales_class_chart_data[i]["value"] += random.randint(5, 20)

    # 流量转化情况
    for i in range(len(origin_today_conversion_chart_data)):
        origin_today_conversion_chart_data[i]["pv"] += random.randint(10, 20)

    return [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        next_today_sales,
        next_today_visits,
        today_visits_chart_data_patch,
        next_today_orders,
        today_orders_chart_data_patch,
        f"{next_today_conversion_rate}%",
        next_today_conversion_rate,
        origin_today_sales_class_chart_data,
        origin_today_conversion_chart_data,
    ]
