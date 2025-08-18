from datetime import datetime
from dash import html, dcc
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import blank_card
from components.macdacard import macda_card
from configs import BaseConfig


# url_params通过dcc.Store输入给layout

def render(themetoken, url_params=None):
    colnames = [
        '车号', '车厢号', '故障名称', '开始时间', '结束时间',
        '状态', '故障等级', '类型', '维修建议', '操作'
    ]
    h_clean_table_columns=['车号', '车厢号', '部件', '已耗[秒/次]', '清除时间']
    return [
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='f_url-params-store', data={}),
        dcc.Store(id="theme-mode-store", data="dark"),
        dcc.Download(id='f_download-excel'),
        # 仪表盘网格布局
        fac.AntdRow(
            [
                # 数据筛选
                fac.AntdCol(
                    blank_card(
                        rootStyle={"background": themetoken["colorBgCard"]},  # 仍使用themetoken变量
                        children=fac.AntdSpace(
                            [
                                fac.AntdForm(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=BaseConfig.train_select_options,
                                                style={'width': 100},
                                                id='f_train_no',
                                            ),
                                            label='车号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=BaseConfig.carriage_select_options,
                                                style={'width': 100},
                                                id='f_carriage_no'
                                            ),
                                            label='车厢号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=[
                                                    {'label': '故障', 'value': '故障'},
                                                    {'label': '预警', 'value': '预警'}
                                                ],
                                                style={'width': 100},
                                                id='f_fault_type'
                                            ),
                                            label='类型'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdDateRangePicker(
                                                placeholder=['从日期时间', '到日期时间'],
                                                showTime={'defaultValue': ['08:30:00', '17:30:00']},
                                                style={'width': 280},
                                                needConfirm=True,
                                                id='f_start_time_range'
                                            ),
                                            label='开始时间'
                                        ),
                                        fac.AntdFormItem(fac.AntdButton('查询', id='f_query_button', type='primary', ghost=True, icon=fac.AntdIcon(icon='antd-search'), nClicks=0)),
                                        fac.AntdFormItem(fac.AntdButton('导出', id='f_export_button', type='primary', ghost=True, icon=fac.AntdIcon(icon='antd-download'), nClicks=0)),
                                    ],
                                    layout='inline',
                                    style={'justifyContent': 'center'},
                                    key=str(url_params) if url_params else 'default-key'  # 强制依赖url_params变化
                                ),
                            ]
                        )
                    ),
                    span=24,
                ),
                # 空调故障预警
                fac.AntdCol(
                    macda_card(
                        rootStyle={
                            "background": themetoken["colorBgCard"],
                        },
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="空调故障预警",
                        description=html.A(
                            "一期故障&预警",
                            href=BaseConfig.external_fault_url,
                            target=BaseConfig.external_link_target,
                            style={"textDecoration": "none"}
                        ),
                        height="calc(70vh - 20px)",
                        chart=
                        fac.AntdSpin(
                        fac.AntdTable(
                            id = 'f_fault-warning-table',
                            columns=[
                                        {
                                            'title': column,
                                            'dataIndex': column,
                                            'width': '{:.2f}%'.format(100/len(colnames)),
                                            'headerCellStyle': {
                                                'fontWeight': 'bold',
                                                'border': 'none',
                                                'borderBottom': '1px solid #e8e8e8',
                                                'color': themetoken["colorText"],
                                                'backgroundColor': 'transparent'
                                            },
                                            'cellStyle': {
                                                'borderRight': 'none',
                                                'borderBottom': '1px solid #e8e8e8',
                                                'color': themetoken["colorText"],
                                                'fontSize': '10px',
                                                'backgroundColor': 'transparent'
                                            },
                                                    **({
                                                        'renderOptions': {
                                                        'renderType': 'button',
                                                        'renderButtonPopConfirmProps': {
                                                                'title': '确认清除该预警/故障？',
                                                                'okText': '确认',
                                                                'cancelText': '取消',
                                                            },
                                                        }
                                                    } if column == '操作' else {})
                                        }
                                        for column in colnames
                                    ],
                            size="small",
                            bordered=False,
                            maxHeight="calc(55vh - 20px)",
                            maxWidth='100%',
                            mode='server-side',
                            pagination={
                                'pageSize': 10,
                                'showSizeChanger': True,
                                'pageSizeOptions': [10, 20, 50, 100],
                                'position': 'bottomRight',
                                'showQuickJumper': True,
                            },
                            className="fault-table",
                            style={
                                'border': 'none',
                                'border-collapse': 'collapse',
                                'border-spacing': '0',
                                'backgroundColor': 'transparent'
                            },
                        ),
                        text='数据加载中',
                        ),
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        ),
        fac.AntdRow(
                    style={
                        "width": "100%",
                        "marginTop": "1px"  # 减少顶部边距
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "padding": "0px",
                                "width": "100%"
                            },
                            children=[
                                fac.AntdAccordion(
                                    id='f_i_accordion-clean',
                                    items=[
                                        {
                                            'title': f'清除记录',
                                            'key': 1,
                                            'children': fac.AntdCol(
                                                [
                                                    fac.AntdRow(
                                                        [
                                                            fac.AntdCol(
                                                                fac.AntdSpin(
                                                                    fac.AntdTable(
                                                                        id='f_clean_table',
                                                                        columns=[
                                                                            {
                                                                                'title': column,
                                                                                'dataIndex': column,
                                                                                'width': '{:.2f}%'.format(100 / len(h_clean_table_columns)),
                                                                                'headerCellStyle': {
                                                                                    'fontWeight': 'bold',
                                                                                    'border': 'none',
                                                                                    'borderBottom': '1px solid #e8e8e8',
                                                                                    'color': themetoken["colorText"],
                                                                                    'backgroundColor': 'transparent'
                                                                                },
                                                                                'cellStyle': {
                                                                                    'borderRight': 'none',
                                                                                    'borderBottom': '1px solid #e8e8e8',
                                                                                    'color': themetoken["colorText"],
                                                                                    'backgroundColor': 'transparent'
                                                                                }
                                                                            }
                                                                            for column in h_clean_table_columns
                                                                        ],
                                                                        size='small',
                                                                        pagination={
                                                                            'pageSize': 10,
                                                                            'showSizeChanger': True,
                                                                            'pageSizeOptions': [10, 20, 50, 100],
                                                                            'position': 'bottomRight',
                                                                            'showQuickJumper': True,
                                                                        },
                                                                        bordered=False,
                                                                        maxHeight="calc(30vh - 20px)",
                                                                        mode='server-side',
                                                                        className="cfault-table",
                                                                        style={
                                                                            'height': '100%',
                                                                            'width': '100%',
                                                                            'border': 'none',
                                                                            'border-collapse': 'collapse',
                                                                            'border-spacing': '0',
                                                                            'backgroundColor': 'transparent'
                                                                        },
                                                                    ),
                                                                    text='数据加载中',
                                                                ),
                                                                span=24,
                                                                style={
                                                                    'maxHeight': "calc(30vh - 20px)",  # 调整表格最大高度
                                                                    'overflow': 'hidden',
                                                                    'padding': '0 2px'
                                                                }
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                span=24,
                                            ),
                                        }
                                    ],
                                    size='small',
                                    expandIconPosition='left',
                                    ghost=True,
                                )
                            ]
                        )
                    ]
                )
    ]