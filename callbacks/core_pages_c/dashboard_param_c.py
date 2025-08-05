import random
from datetime import datetime
from dash import Input, Output, callback

# 页面数据更新回调
@callback(
    Output('param_update-datetime', 'children'),
    Output('param_online-chart-1', 'data'),
    Output('param_online-chart-1', 'annotations'),
    Output('param_online-chart-2', 'data'),
    Output('param_online-chart-2', 'annotations'),
    Output('param_online-chart-3', 'data'),
    Output('param_online-chart-3', 'annotations'),
    Output('param_online-chart-4', 'data'),
    Output('param_online-chart-4', 'annotations'),
    Output('param_operation-data-chart', 'data'),
    Output('param_energy-chart', 'data'),
    Output('param_today-sales-class-chart', 'data'),
    Output('param_today-hot-search-wordcloud', 'data'),
    Output('param_today-comment-wordcloud-chart-1', 'data'),
    Output('param_today-comment-wordcloud-chart-1', 'annotations'),
    Output('param_today-comment-wordcloud-chart-2', 'data'),
    Output('param_today-comment-wordcloud-chart-2', 'annotations'),
    Output('param_today-comment-wordcloud-chart-3', 'data'),
    Output('param_today-comment-wordcloud-chart-3', 'annotations'),
    Output('param_today-comment-wordcloud-chart-4', 'data'),
    Output('param_today-comment-wordcloud-chart-4', 'annotations'),
    Output('param_today-conversion-chart', 'data'),
    Input('param_update-data-interval', 'n_intervals'),
    prevent_initial_call=False,
)
def update_dashboard_data(n_intervals):
    """更新参数图页面数据"""
    # 更新时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 在线情况数据 - 圆环1
    online_value1 = random.randint(70, 80)
    online_data1 = [{"value": online_value1}]
    online_annotations1 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线\n{online_value1}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    # 在线情况数据 - 圆环2
    online_value2 = random.randint(55, 65)
    online_data2 = [{"value": online_value2}]
    online_annotations2 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线\n{online_value2}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    # 在线情况数据 - 圆环3
    online_value3 = random.randint(80, 90)
    online_data3 = [{"value": online_value3}]
    online_annotations3 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线\n{online_value3}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    # 在线情况数据 - 圆环4
    online_value4 = random.randint(85, 95)
    online_data4 = [{"value": online_value4}]
    online_annotations4 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线\n{online_value4}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center", "whiteSpace": "pre"}}]

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

    # 能耗数据
    energy_data = [{"day": f"{i}日", "energy": random.randint(500, 1000)} for i in range(1, 8)]

    # 销售额类别占比数据
    sales_class_data = [
        {"type": "家用电器", "value": random.randint(3000, 5000)},
        {"type": "食用酒水", "value": random.randint(2000, 4000)},
        {"type": "个护健康", "value": random.randint(2000, 4000)},
        {"type": "服饰箱包", "value": random.randint(1000, 3000)},
        {"type": "母婴产品", "value": random.randint(500, 2000)},
        {"type": "其他", "value": random.randint(500, 2000)},
    ]

    # 热门搜索词云数据
    hot_search_data = [{"name": f"关键词{i}", "value": random.randint(10, 100)} for i in range(1, 31)]

    # 用户评论词云圆环数据
    comment_value1 = random.randint(70, 80)
    comment_data1 = [{"value": comment_value1}]
    comment_annotations1 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线：{comment_value1}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    comment_value2 = random.randint(55, 65)
    comment_data2 = [{"value": comment_value2}]
    comment_annotations2 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线：{comment_value2}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    comment_value3 = random.randint(80, 90)
    comment_data3 = [{"value": comment_value3}]
    comment_annotations3 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线：{comment_value3}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center"}}]

    comment_value4 = random.randint(85, 95)
    comment_data4 = [{"value": comment_value4}]
    comment_annotations4 = [{"type": "text", "position": ["50%", "50%"], "content": f"在线参数\n{comment_value4}", "style": {"fill": "white", "fontSize": 12, "textAlign": "center", "whiteSpace": "pre"}}]

    # 流量转化情况数据
    conversion_data = [
        {"action": "浏览网站", "pv": random.randint(40000, 60000)},
        {"action": "放入购物车", "pv": random.randint(30000, 40000)},
        {"action": "生成订单", "pv": random.randint(20000, 30000)},
        {"action": "支付订单", "pv": random.randint(10000, 20000)},
        {"action": "完成交易", "pv": random.randint(5000, 10000)},
    ]

    return (
        current_time,
        online_data1,
        online_annotations1,
        online_data2,
        online_annotations2,
        online_data3,
        online_annotations3,
        online_data4,
        online_annotations4,
        operation_data,
        energy_data,
        sales_class_data,
        hot_search_data,
        comment_data1,
        comment_annotations1,
        comment_data2,
        comment_annotations2,
        comment_data3,
        comment_annotations3,
        comment_data4,
        comment_annotations4,
        conversion_data
    )