from datetime import datetime
from dash import html, dcc
import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    blank_card,
    index_card,
    simple_chart_card,
)
from peewee import fn

from components.macdacard import macda_card
import random
from utils.log import log as log

from configs import BaseConfig
from orm.chart_view_fault_timed import Chart_view_fault_timed


def render(themetoken):
    colnames = ['车号', '车厢号', '故障名称', '开始时间', '结束时间', '状态', '故障等级', '类型', '维修建议']
    """数据大屏-故障图页面主内容渲染"""
    return [
        # 消息提示输出目标
        fac.Fragment(id="message-target"),
        # 数据统一更新轮询
        dcc.Interval(
            id="fault_update-data-interval",
            interval=BaseConfig.fault_update_data_interval,  # 示例，每3秒更新一次
        ),
        # 添加主题模式存储 - 初始设为深色
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
                                                    {'label': f'161{i}车', 'value': f'161{i}'} for i in range(1, 7)
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
                                            #'width': 'calc((100% - 100px) / {})'.format(len(colnames)),
                                            'width': '{:.2f}%'.format(100/9),
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
                                'total': (Chart_view_fault_timed.select(fn.count(Chart_view_fault_timed.dvc_train_no)).scalar()),
                                'current': 1,
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
                        size='small',
                        ),
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]