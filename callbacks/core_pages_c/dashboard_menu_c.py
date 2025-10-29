import dash
from dash.dependencies import Input, Output, State, MATCH
from dash import no_update, dcc
import time

from configs import BaseConfig

# 全局变量存储上次回调时间，用于防抖
last_menu_click_time = {}

def filter_params_for_page(page_name, search_params):
    """根据页面过滤相关参数 - 客户要求携带所有参数"""
    if not search_params:
        return {}
    
    # 解析search参数
    from urllib.parse import parse_qs
    params = parse_qs(search_params.lstrip('?'))
    
    # 展平参数（parse_qs返回列表）
    flat_params = {k: v[0] if v else '' for k, v in params.items()}
    
    # 客户要求：所有页面都携带完整参数，不过滤
    # 只过滤空值
    return {k: v for k, v in flat_params.items() if v}

def build_search_string(params):
    """构建search字符串"""
    if not params:
        return ''
    
    # 过滤空值
    filtered_params = {k: v for k, v in params.items() if v}
    if not filtered_params:
        return ''
    
    return '?' + '&'.join([f"{k}={v}" for k, v in filtered_params.items()])

prefix = BaseConfig.project_prefix
menu_data = [
    {
        "title": "线路",
        "key": f"/{prefix}/line",
        "href": f"/{prefix}/line",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/line-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/line-icon-active.svg",
    },
    {
        "title": "列车",
        "key": f"/{prefix}/train",
        "href": f"/{prefix}/train",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/train-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/train-icon-active.svg",
    },
    {
        "title": "车厢",
        "key": f"/{prefix}/carriage",
        "href": f"/{prefix}/carriage",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/carriage-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/carriage-icon-active.svg",
    },
    {
        "title": "参数",
        "key": f"/{prefix}/param",
        "href": f"/{prefix}/param",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/param-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/param-icon-active.svg",
    },
    {
        "title": "故障",
        "key": f"/{prefix}/fault",
        "href": f"/{prefix}/fault",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/fault-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/fault-icon-active.svg",
    },
    {
        "title": "寿命",
        "key": f"/{prefix}/health",
        "href": f"/{prefix}/health",
        "icon_src": f"/{prefix}/assets/imgs/new-icon/health-icon.svg",
        "icon_src_active": f"/{prefix}/assets/imgs/new-icon/health-icon-active.svg",
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
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_line_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'line_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_line_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_line_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/line'
        if current_pathname != target_path:
            # line页面不需要参数，直接跳转
            return target_path
        return no_update
    
    # 列车菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-train', 'nClicks'),
        State('root-url', 'pathname'),
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_train_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'train_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_train_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_train_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/train'
        if current_pathname != target_path:
            # 过滤并保持相关参数
            filtered_params = filter_params_for_page('train', current_search)
            search_string = build_search_string(filtered_params)
            return target_path + search_string
        return no_update
    
    # 车厢菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-carriage', 'nClicks'),
        State('root-url', 'pathname'),
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_carriage_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'carriage_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_carriage_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_carriage_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/carriage'
        if current_pathname != target_path:
            # 过滤并保持相关参数
            filtered_params = filter_params_for_page('carriage', current_search)
            search_string = build_search_string(filtered_params)
            return target_path + search_string
        return no_update
    
    # 参数菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-param', 'nClicks'),
        State('root-url', 'pathname'),
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_param_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'param_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_param_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_param_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/param'
        if current_pathname != target_path:
            # 过滤并保持相关参数
            filtered_params = filter_params_for_page('param', current_search)
            search_string = build_search_string(filtered_params)
            return target_path + search_string
        return no_update

    # 故障菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-fault', 'nClicks'),
        State('root-url', 'pathname'),
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_fault_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'fault_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_fault_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_fault_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/fault'
        if current_pathname != target_path:
            # 过滤并保持相关参数
            filtered_params = filter_params_for_page('fault', current_search)
            search_string = build_search_string(filtered_params)
            return target_path + search_string
        return no_update

    # 寿命菜单回调
    @app.callback(
        Output('root-url', 'pathname', allow_duplicate=True),
        Input('dashboard-menu-item-health', 'nClicks'),
        State('root-url', 'pathname'),
        State('root-url', 'search'),
        prevent_initial_call=True
    )
    def handle_health_menu_click(nClicks, current_pathname, current_search):
        if nClicks is None:
            return no_update
        
        # 防抖逻辑：300ms内只允许一次跳转
        current_time = time.time()
        callback_id = 'health_menu_click'
        
        if callback_id in last_menu_click_time:
            if current_time - last_menu_click_time[callback_id] < 0.3:
                print(f"[handle_health_menu_click] 防抖：跳过跳转")
                return no_update
        
        last_menu_click_time[callback_id] = current_time
        print(f"[handle_health_menu_click] 防抖：允许跳转")
        
        target_path = f'/{prefix}/health'
        if current_pathname != target_path:
            # 过滤并保持相关参数
            filtered_params = filter_params_for_page('health', current_search)
            search_string = build_search_string(filtered_params)
            return target_path + search_string
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