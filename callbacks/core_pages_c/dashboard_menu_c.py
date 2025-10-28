import dash
from dash.dependencies import Input, Output, State, MATCH
from dash import no_update, dcc

from configs import BaseConfig

prefix = BaseConfig.project_prefix
menu_data = [
    {
        "title": "线路",
        "key": f"/{prefix}/line",
        "href": f"/{prefix}/line",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/line-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/line-icon-active.svg",
    },
    {
        "title": "列车",
        "key": f"/{prefix}/train",
        "href": f"/{prefix}/train",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/train-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/train-icon-active.svg",
    },
    {
        "title": "车厢",
        "key": f"/{prefix}/carriage",
        "href": f"/{prefix}/carriage",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/carriage-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/carriage-icon-active.svg",
    },
    {
        "title": "参数",
        "key": f"/{prefix}/param",
        "href": f"/{prefix}/param",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/param-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/param-icon-active.svg",
    },
    {
        "title": "故障",
        "key": f"/{prefix}/fault",
        "href": f"/{prefix}/fault",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/fault-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/fault-icon-active.svg",
    },
    {
        "title": "寿命",
        "key": f"/{prefix}/health",
        "href": f"/{prefix}/health",
        "icon_src": "/sz16phmHVAC2/assets/imgs/new-icon/health-icon.svg",
        "icon_src_active": "/sz16phmHVAC2/assets/imgs/new-icon/health-icon-active.svg",
    },
    ]

def register_dashboard_menu_callbacks(app):
    @app.callback(
        Output({"type": "menu-item-icon", "index": MATCH}, "src"),
        Input('current-key-store', 'data'),
        State({"type": "menu-item-icon", "index": MATCH}, "id"),
    )
    def update_icon(current_key, icon_id):
        for item in menu_data:
            if item["key"] == icon_id["index"]:
                return item["icon_src_active"] if current_key == item["key"] else item["icon_src"]
        return no_update

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
        Output('current-key-store', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True
    )
    def sync_menu_current_key(pathname):
        for item in menu_data:
            if pathname == item["key"]:
                print(f"Setting currentKey to: {item['key']}")
                return item["key"]
        # 默认返回线路页面
        return f'/{prefix}/line'


# 确保在app.py中导入并调用此函数
# from callbacks.core_pages_c.dashboard_menu_c import register_dashboard_menu_callbacks
# register_dashboard_menu_callbacks(app)