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
from components.macdacard import macda_card
import random

from configs import BaseConfig


def render(themetoken):
    components_name = ['新风温度-系统', '回风温度-系统', '目标温度', '载客量', '车厢温度-1', '车厢湿度-1', '车厢温度-2',
                     '车厢湿度-2', '空气质量-温度-U1', '空气质量-湿度-U1', '空气质量-CO2-U1', '空气质量-TVOC-U1',
                     '空气质量-PM2.5-U1', '空气质量-PM10-U1', '空调运行模式U1', '压差-U1', '新风温度-U1', '回风温度-U1',
                     '新风阀开度-U1', '回风阀开度-U1', '压缩机频率-U11', '压缩机电流-U11', '压缩机电压-U11',
                     '压缩机功率-U11', '吸气温度-U11', '吸气压力-U11', '过热度-U11', '电子膨胀阀开度-U11',
                     '高压压力-U11', '送风温度-U11', '压缩机频率-U12', '压缩机电流-U12', '压缩机电压-U12',
                     '压缩机功率-U12', '吸气温度-U12', '吸气压力-U12', '过热度-U12', '电子膨胀阀开度-U12',
                     '高压压力-U12', '送风温度-U12', '空气质量-温度-U2', '空气质量-湿度-U2', '空气质量-CO2-U2',
                     '空气质量-TVOC-U2', '空气质量-PM2.5-U2', '空气质量-PM10-U2', '空调运行模式U2', '压差-U2',
                     '新风温度-U2', '回风温度-U2', '新风阀开度-U2', '回风阀开度-U2', '压缩机频率-U21', '压缩机电流-U21',
                     '压缩机电压-U21', '压缩机功率-U21', '吸气温度-U21', '吸气压力-U21', '过热度-U21',
                     '电子膨胀阀开度-U21', '高压压力-U21', '送风温度-U21', '压缩机频率-U22', '压缩机电流-U22',
                     '压缩机电压-U22', '压缩机功率-U22', '吸气温度-U22', '吸气压力-U22', '过热度-U22',
                     '电子膨胀阀开度-U22', '高压压力-U22', '送风温度-U22', '通风机电流-U11', '通风机电流-U12',
                     '冷凝风机电流-U11', '冷凝风机电流-U12', '通风机电流-U21', '通风机电流-U22', '冷凝风机电流-U21',
                     '冷凝风机电流-U22', '总电流-机组1', '总电流-机组2', '空调机组能耗']
    """数据大屏-参数图页面主内容渲染"""
    return [
        # URL参数处理
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='p_url-params-store', data={}),
        # 消息提示输出目标
        fac.Fragment(id="message-target"),

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
                                                    {'label': f'16{i}车', 'value': f'16{i}'} for i in range(33, 45)
                                                ],
                                                style={'width': 100},
                                                id='p_train_no'
                                            ),
                                            label='车号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                options=[
                                                    {'label': f'{i}车厢', 'value': f'{i}'} for i in range(1, 7)
                                                ],
                                                style={'width': 100},
                                                id='p_carriage_no'
                                            ),
                                            label='车厢号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                 options=[{'label': name, 'value': name} for name in components_name],
                                                 style={'width': 400},
                                                 mode='multiple',
                                                 id='p_component',
                                            ),
                                            label='组件'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdDateRangePicker(
                                                placeholder=['从日期时间', '到日期时间'],
                                                showTime={'defaultValue': ['08:30:00', '17:30:00']},
                                                style={'width': 280},
                                                needConfirm=True,
                                                id='p_start_time_range'
                                            ),
                                            label='时间范围'
                                        ),
                                        fac.AntdFormItem(fac.AntdButton('查询', type='primary', ghost=True,
                                                                        icon=fac.AntdIcon(icon='antd-search'), id='p_query_button', nClicks=0)),
                                    ],
                                    layout='inline',
                                    style={'justifyContent': 'center'},
                                ),
                            ]
                        )
                    ),
                    span=24,
                ),
                # 参数运行数据
                fac.AntdCol(
                    macda_card(
                        rootStyle={"background": themetoken["colorBgCard"]},
                        titleStyle={"color": themetoken["colorText"]},
                        descriptionStyle={"color": themetoken["colorText"]},
                        title="参数运行数据",
                        description=html.A(
                            "一期运行参数",
                            href=BaseConfig.external_param_url,
                            target="_blank",
                            style={"textDecoration": "none"}
                        ),
                        height="calc(70vh - 20px)",
                        chart=fact.AntdLine(
                            id="param_operation-data-chart",
                            data=[],  # 初始为空，由回调填充
                            xField="time_minute",
                            yField="avg_value",
                            seriesField="param_name",
                            smooth=True,
                            slider={},
                            isStack=True,
                            color=["#1890ff", "#faad14", "#52c41a",
                                   "#ff4d4f", "#722ed1", "#fa8c16",
                                   "#13c2c2", "#7cb305", "#ff7a45",
                                   "#2f54eb", "#f5222d", "#fa8c16"],
                        ),
                    ),
                    span=24,
                ),
            ],
            gutter=[10, 10],
        )
    ]