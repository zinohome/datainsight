import dash
from flask import request, redirect, send_from_directory
from user_agents import parse
from dash_offline_detect_plugin import setup_offline_detect_plugin
import logging
import os
import mimetypes
# 防止系统缺失注册
mimetypes.add_type('image/svg+xml', '.svg')
# 应用基础参数
from configs import BaseConfig

if BaseConfig.setup_offline_detect:
    setup_offline_detect_plugin()

# 开启peewee日志调试
if BaseConfig.app_peewee_debug_log:
    logging.basicConfig()
    logging.getLogger('peewee').setLevel(logging.DEBUG)

prefix = BaseConfig.project_prefix

app = dash.Dash(
    __name__,
    title=BaseConfig.app_title,
    suppress_callback_exceptions=True,
    compress=True,  # 隐式依赖flask-compress
    update_title=None,
    requests_pathname_prefix=f'/{prefix}/',  # 末尾一定要有 /
    routes_pathname_prefix=f'/{prefix}/',
    assets_url_path=f'{prefix}/assets',
    assets_folder='assets',                     # ← 你的硬盘目录（默认就是 assets）
    serve_locally=True,                         # ← 关键2：必须本地服务
)

server = app.server

# 添加根路径和根路径（无末尾/）的重定向规则
@app.server.route('/')
def redirect_root():
    """将根路径重定向到应用首页"""
    return redirect(f'/{prefix}/', code=301)

@app.server.route('/assets/<path:filename>')
def redirect_old_assets(filename):
    return redirect(f'/{prefix}/assets/{filename}', code=301)

# ② 把 /{prefix}/assets 真正挂到硬盘 assets/
@app.server.route(f'/{prefix}/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(
        os.path.join(app.server.root_path, 'assets'),
        filename,
        mimetype='image/svg+xml' if filename.lower().endswith('.svg') else None
    )

@app.server.before_request
def check_browser():
    """检查浏览器版本是否符合最低要求"""

    # 提取当前请求对应的浏览器信息
    user_agent = parse(str(request.user_agent))

    # 若浏览器版本信息有效
    if user_agent.browser.version != ():
        # IE相关浏览器直接拦截
        if user_agent.browser.family == "IE":
            return (
                "<div style='font-size: 16px; color: red; position: fixed; top: 40%; left: 50%; transform: translateX(-50%);'>"
                "请不要使用IE浏览器，或开启了IE内核兼容模式的其他浏览器访问本应用</div>"
            )
        # 基于BaseConfig.min_browser_versions配置，对相关浏览器最低版本进行检查
        for rule in BaseConfig.min_browser_versions:
            # 若当前请求对应的浏览器版本，低于声明的最低支持版本
            if (
                user_agent.browser.family == rule["browser"]
                and user_agent.browser.version[0] < rule["version"]
            ):
                return (
                    "<div style='font-size: 16px; color: red; position: fixed; top: 40%; left: 50%; transform: translateX(-50%);'>"
                    "您的{}浏览器版本低于本应用最低支持版本（{}），请升级浏览器后再访问</div>"
                ).format(rule["browser"], rule["version"])

        # 若开启了严格的浏览器类型限制
        if BaseConfig.strict_browser_type_check:
            # 若当前浏览器不在声明的浏览器范围内
            if user_agent.browser.family not in [
                rule["browser"] for rule in BaseConfig.min_browser_versions
            ]:
                return (
                    "<div style='font-size: 16px; color: red; position: fixed; top: 40%; left: 50%; transform: translateX(-50%);'>"
                    "当前浏览器类型不在支持的范围内，支持的浏览器类型有：{}</div>"
                ).format(
                    "、".join(
                        [rule["browser"] for rule in BaseConfig.min_browser_versions]
                    )
                )
