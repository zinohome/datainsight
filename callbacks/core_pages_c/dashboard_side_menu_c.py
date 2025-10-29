from dash import callback, Output, Input, State, no_update
from configs import BaseConfig
from utils.log import log
import time

prefix = BaseConfig.project_prefix

# 全局变量存储上次回调时间，用于防抖
last_callback_time = {}

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

def register_dashboard_side_menu_callbacks(app):
    """注册dashboard侧边菜单的回调函数"""
    
    @app.callback(
        Output('menu-url-params-store', 'data'),
        Input('url', 'search'),
        prevent_initial_call=False
    )
    def update_menu_url_params(search):
        """更新菜单URL参数存储"""
        log.debug(f"[update_menu_url_params] 更新菜单URL参数: {search}")
        return search or ''
    
    @app.callback(
        Output('dashboard-side-menu', 'menuItems'),
        Input('menu-url-params-store', 'data'),
        prevent_initial_call=False
    )
    def update_menu_items_with_params(search_params):
        """根据URL参数更新菜单项的href属性"""
        log.debug(f"[update_menu_items_with_params] 更新菜单项: {search_params}")
        
        # 防抖逻辑：300ms内只允许一次更新
        current_time = time.time()
        callback_id = 'menu_items_update'
        
        if callback_id in last_callback_time:
            if current_time - last_callback_time[callback_id] < 0.3:
                log.debug(f"[update_menu_items_with_params] 防抖：跳过更新")
                return no_update
        
        last_callback_time[callback_id] = current_time
        log.debug(f"[update_menu_items_with_params] 防抖：允许更新")
        
        # 如果search_params为空，尝试保持之前的参数
        if not search_params and hasattr(update_menu_items_with_params, 'last_params'):
            search_params = update_menu_items_with_params.last_params
            log.debug(f"[update_menu_items_with_params] 使用上次参数: {search_params}")
        
        # 保存当前参数
        update_menu_items_with_params.last_params = search_params
        
        dash_menuItem_style = {
            "padding": "16px 0",
            "fontSize": "0",
            "justifyContent": "center",
            "margin": "0 auto",
            "minWidth": "40px",
            "background": "transparent",
            "borderBottom": "1px solid #e8e8e8"
        }
        
        # 动态生成菜单项
        menu_items = []
        
        # 线路菜单项
        line_params = filter_params_for_page('line', search_params)
        line_search = build_search_string(line_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "线路",
                "key": f"/{prefix}/line",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-line",
                "href": f"/{prefix}/line" + line_search,
            }
        })
        
        # 列车菜单项
        train_params = filter_params_for_page('train', search_params)
        train_search = build_search_string(train_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "列车",
                "key": f"/{prefix}/train",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-train",
                "href": f"/{prefix}/train" + train_search,
            }
        })
        
        # 车厢菜单项
        carriage_params = filter_params_for_page('carriage', search_params)
        carriage_search = build_search_string(carriage_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "车厢",
                "key": f"/{prefix}/carriage",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-carriage",
                "href": f"/{prefix}/carriage" + carriage_search,
            }
        })
        
        # 参数菜单项
        param_params = filter_params_for_page('param', search_params)
        param_search = build_search_string(param_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "参数",
                "key": f"/{prefix}/param",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-param",
                "href": f"/{prefix}/param" + param_search,
            }
        })
        
        # 故障菜单项
        fault_params = filter_params_for_page('fault', search_params)
        fault_search = build_search_string(fault_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "故障",
                "key": f"/{prefix}/fault",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-fault",
                "href": f"/{prefix}/fault" + fault_search,
            }
        })
        
        # 寿命菜单项
        health_params = filter_params_for_page('health', search_params)
        health_search = build_search_string(health_params)
        menu_items.append({
            "component": "Item",
            "props": {
                "title": "寿命",
                "key": f"/{prefix}/health",
                "style": dash_menuItem_style,
                "id": "dashboard-menu-item-health",
                "href": f"/{prefix}/health" + health_search,
            }
        })
        
        log.debug(f"[update_menu_items_with_params] 生成的菜单项数量: {len(menu_items)}")
        return menu_items
