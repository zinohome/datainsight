from datetime import datetime
from dash import html, dcc
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import blank_card
from components.macdacard import macda_card

# url_params通过dcc.Store输入给layout

def render(themetoken, url_params=None):
    colnames = [
        '车号', '车厢号', '故障名称', '开始时间', '结束时间',
        '状态', '故障等级', '类型', '维修建议'
    ]
    return [
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='url-params-store', data={}),
        html.Div(id='init-trigger'),  # 添加初始化触发器
        fac.Fragment(id="message-target"),
        dcc.Store(id="theme-mode-store", data="dark"),
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
                                                options=[
                                                    {'label': f'1210{i}车', 'value': f'1210{i}'} for i in range(1, 10)
                                                ],
                                                style={'width': 100},
                                                id='train_no',
                                            ),
                                            label='车号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=[
                                                    {'label': f'{i}车厢', 'value': f'{i}'} for i in range(1, 7)
                                                ],
                                                style={'width': 100},
                                                id='carriage_no'
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
                                                id='fault_type'
                                            ),
                                            label='类型'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdDateRangePicker(
                                                placeholder=['从日期时间', '到日期时间'],
                                                showTime={'defaultValue': ['08:30:00', '17:30:00']},
                                                needConfirm=True,
                                                id='start_time_range'
                                            ),
                                            label='开始时间'
                                        ),
                                        fac.AntdFormItem(fac.AntdButton('查询', id='query_button', type='primary', ghost=True, icon=fac.AntdIcon(icon='antd-search'), nClicks=0)),
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
                            href="https://www.baidu.com",
                            target="_blank",
                            style={"textDecoration": "none"}
                        ),
                        height=450,
                        chart=
                        fac.AntdSpin(
                        fac.AntdTable(
                            id = 'fault-warning-table',
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
                                            }
                                        }
                                        for column in colnames
                                    ],
                            size="small",
                            bordered=False,
                            maxHeight=450,
                            maxWidth='100%',
                            mode='server-side',
                            pagination={
                                'total': 0,   # 初始化为0，交由callback更新
                                'current': 1,
                                'pageSize': 5,
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
                        size='small',
                        ),
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]