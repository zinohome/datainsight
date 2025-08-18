import dash
from dash.dependencies import Input, Output, State
from dash import no_update

from configs import BaseConfig

prefix = BaseConfig.project_prefix
def register_dashboard_menu_callbacks(app):
    """注册仪表盘菜单相关回调"""
    # 线路菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-line', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_line_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update
        
        target_path = f'/{prefix}/line'
        if current_pathname != target_path:
            return target_path
        return no_update
    
    # 列车菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-train', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_train_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update
        
        target_path = f'/{prefix}/train'
        if current_pathname != target_path:
            return target_path
        return no_update
    
    # 车厢菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-carriage', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_carriage_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update
        
        target_path = f'/{prefix}/carriage'
        if current_pathname != target_path:
            return target_path
        return no_update
    
    # 参数菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-param', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_param_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update
        
        target_path = f'/{prefix}/param'
        if current_pathname != target_path:
            return target_path
        return no_update

    # 故障菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-fault', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_fault_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update

        target_path = f'/{prefix}/fault'
        if current_pathname != target_path:
            return target_path
        return no_update

    # 寿命菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-health', 'nClicks'),
        State('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def handle_fault_menu_click(nClicks, current_pathname):
        if nClicks is None:
            return no_update

        target_path = f'/{prefix}/health'
        if current_pathname != target_path:
            return target_path
        return no_update
    
    # 注册菜单状态同步回调
    @app.callback(
        Output('dashboard-side-menu', 'currentKey'),
        Input('root-url', 'pathname'),
        prevent_initial_call=True
    )
    def sync_menu_current_key(pathname):
        # 匹配路径
        if pathname == f'/{prefix}/line':
            return f'/{prefix}/line'
        elif pathname == f'/{prefix}/train':
            return f'/{prefix}/train'
        elif pathname == f'/{prefix}/carriage':
            return f'/{prefix}/carriage'
        elif pathname == f'/{prefix}/param':
            return f'/{prefix}/param'
        elif pathname == f'/{prefix}/fault':
            return f'/{prefix}/fault'
        elif pathname == f'/{prefix}/health':
            return f'/{prefix}/health'
        # 默认返回线路页面
        return f'/{prefix}/line'


# 确保在app.py中导入并调用此函数
# from callbacks.core_pages_c.dashboard_menu_c import register_dashboard_menu_callbacks
# register_dashboard_menu_callbacks(app)