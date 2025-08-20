from dash import html
import feffery_antd_components as fac

def scrollTable(
        table_id: str,
        data: list,
        columns: list,
        scroll_interval: int = 1200,
        visible_rows: int = 10,
        row_height: int = 24,
        style: dict = None,
        **kwargs
):
    container_height = visible_rows * row_height
    antdtable_args = dict(
        columns=columns,
        style=style or {}
    )
    antdtable_args.update(kwargs)
    table_head = fac.AntdTable(
        id=f'{table_id}-head',
        data=[],  # **注意：无需假数据也会渲染完整表头**
        showHeader=True,
        pagination=False,
        **antdtable_args
    )
    table_body = fac.AntdTable(
        id=table_id,
        data=data,
        showHeader=False,
        pagination=False,
        **antdtable_args
    )
    return html.Div([
        html.Div(table_head, style={
            'overflow': 'hidden',
            'width': '100%'
        },
        className="scroll-table-wrapper"
        ),
        html.Div(table_body, id=f'{table_id}-outer', style={
            'height': f'{container_height}px',
            'overflowY': 'auto',
            'width': '100%'
        }, **{
            'data-scroll-table': '1',
            'data-scroll-interval': str(scroll_interval),
            'data-row-height': str(row_height),
            'data-visible-rows': str(visible_rows)
        })
    ])