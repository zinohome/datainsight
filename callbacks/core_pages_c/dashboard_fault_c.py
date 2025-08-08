import logging
import random
from datetime import datetime
from dash import Input, Output, callback, State

from configs import LayoutConfig
from utils.db_query import DBQuery
from utils.log import log as log


# 页面数据更新回调
@callback(
    [Output('fault_update-datetime', 'children'),
     Output('fault-warning-table', 'data'),
     Output('fault-warning-table', 'loading')],
    Input('query_button', 'nClicks'),  # 改为按钮点击触发
    [State('train_no', 'value'),          # 车号
     State('carriage_no', 'value'),       # 车厢号
     State('fault_type', 'value'),        # 类型
     State('start_time_range', 'value')], # 时间范围
    prevent_initial_call=False,  # 防止初始加载触发
)
def update_dashboard_data(n_clicks, train_no, carriage_no, fault_type, start_time_range):
    # 更新故障图页面数据
    # 更新时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    themetoken = LayoutConfig.dashboard_theme
    fault_data = []
    loading = True
    try:
        # 初始化DBQuery实例
        db_query = DBQuery()
        # 执行SQL查询
        fault_sql = """
                    SELECT 
                        dvc_train_no as 车号,
                        dvc_carriage_no as 车厢号,
                        param_name as 故障名称,
                        TO_CHAR(start_time AT TIME ZONE 'Asia/Shanghai', 'YYYY-MM-DD HH24:MI:SS') as 开始时间,
                        TO_CHAR(end_time AT TIME ZONE 'Asia/Shanghai', 'YYYY-MM-DD HH24:MI:SS') as 结束时间,
                        status as 状态,
                        fault_level as 故障等级,
                        fault_type as 类型,
                        repair_suggestion as 维修建议
                    FROM public.chart_view_fault_timed
                """.strip()

        # 动态构建筛选条件
        conditions = []
        params = {}
        
        if train_no:  # 车号筛选
            conditions.append("dvc_train_no = %(train_no)s")
            params['train_no'] = train_no
        if carriage_no:  # 车厢号筛选
            conditions.append("dvc_carriage_no = %(carriage_no)s")
            params['carriage_no'] = carriage_no
        if fault_type:  # 类型筛选
            conditions.append("fault_type = %(fault_type)s")
            params['fault_type'] = fault_type
        if start_time_range:  # 时间范围筛选
            start, end = start_time_range
            conditions.append("start_time BETWEEN %(start_time)s AND %(end_time)s")
            params['start_time'] = start
            params['end_time'] = end
        
        # 添加WHERE子句
        if conditions:
            fault_sql += " WHERE " + " AND ".join(conditions)

        # 执行带参数的查询
        log.debug(params)
        log.debug(conditions)
        log.debug(fault_sql)
        result = db_query.execute_query(fault_sql, params)
        fault_data = result if result else []
        if result:
            # 获取所有列名
            log.debug(result[0].keys())
            log.debug(fault_data)
    except Exception as e:
        # 记录错误日志
        import logging
        logging.error(f'获取故障数据失败: {str(e)}')
    return (
        current_time,
        fault_data,
        False
    )