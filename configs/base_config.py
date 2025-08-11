from typing import List


class BaseConfig:
    """应用基础配置参数"""

    # 应用基础标题
    app_title: str = "MACDA_Insight"

    # 应用版本
    app_version: str = "0.2.1"

    # 浏览器最低版本限制规则
    min_browser_versions: List[dict] = [
        {"browser": "Chrome", "version": 88},
        {"browser": "Firefox", "version": 78},
        {"browser": "Edge", "version": 100},
    ]

    # 是否基于min_browser_versions开启严格的浏览器类型限制
    # 不在min_browser_versions规则内的浏览器将被直接拦截
    strict_browser_type_check: bool = False

    # 数据库连接配置参数
    db_dbname = 'postgres'
    db_user = 'postgres'
    db_password = 'passw0rd'
    db_host = '192.168.32.17'
    db_port = '5432'
    db_minconn = 5
    db_maxconn = 30
    db_stale_timeout = 600  # 10分钟连接超时
    db_timeout = 30  # 获取连接超时时间(秒)
    db_max_lifetime = 600  # 连接最大生命周期(秒)

    # 日志配置参数
    app_log_filename = 'app.log'
    app_log_level = 'INFO'

    # 数据刷新时间配置
    fault_update_data_interval = 10000

    # 外部连接配置
    external_param_url = 'https://www.baidu.com'
    external_fault_url = 'https://www.baidu.com'
