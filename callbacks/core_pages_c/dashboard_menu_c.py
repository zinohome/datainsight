import dash
from dash.dependencies import Input, Output, State
from dash import no_update


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
        
        target_path = '/macda/dashboard/line'
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
        
        target_path = '/macda/dashboard/train'
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
        
        target_path = '/macda/dashboard/carriage'
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
        
        target_path = '/macda/dashboard/param'
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
        
        target_path = '/macda/dashboard/fault'
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
        if pathname == '/macda/dashboard/line':
            return '/macda/dashboard/line'
        elif pathname == '/macda/dashboard/train':
            return '/macda/dashboard/train'
        elif pathname == '/macda/dashboard/carriage':
            return '/macda/dashboard/carriage'
        elif pathname == '/macda/dashboard/param':
            return '/macda/dashboard/param'
        elif pathname == '/macda/dashboard/fault':
            return '/macda/dashboard/fault'
        # 默认返回线路页面
        return '/macda/dashboard/line'


# 确保在app.py中导入并调用此函数
# from callbacks.core_pages_c.dashboard_menu_c import register_dashboard_menu_callbacks
# register_dashboard_menu_callbacks(app)