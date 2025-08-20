from dash import Dash, html
from components.scroll_table import scrollTable

sample_data = [
    {"序号": i + 1, "内容": f"测试第{i+1}行", "A": f"a{i+1}", "B": f"b{i+1}", "C": f"c{i+1}"} for i in range(50)
]
sample_cols = [
    {"title": "序号", "dataIndex": "序号"},
    {"title": "内容", "dataIndex": "内容"},
    {"title": "A列", "dataIndex": "A"},
    {"title": "B列", "dataIndex": "B"},
    {"title": "C列", "dataIndex": "C"},
]

app = Dash(__name__)
app.layout = html.Div([
    scrollTable(
        table_id="demo-scroll-table",
        data=sample_data,
        columns=sample_cols,
        scroll_interval=1200,      # 1200ms滚一行
        visible_rows=10,           # 显示10行
        row_height=24             # 每行24高度，请结合表格实际高度微调
    )
])

if __name__ == '__main__':
    app.run(debug=True)