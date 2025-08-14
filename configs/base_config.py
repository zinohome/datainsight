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

    # setup_offline_detect
    setup_offline_detect: bool = False

    # 数据库连接配置参数
    db_dbname: str = 'postgres'
    db_user: str = 'postgres'
    db_password: str = 'passw0rd'
    db_host: str = '192.168.32.17'
    db_port: str = '5432'
    db_minconn: int = 5
    db_maxconn: int = 30
    db_stale_timeout: int = 300  # 10分钟连接超时
    db_timeout = 30  # 获取连接超时时间(秒)
    db_max_lifetime = 600  # 连接最大生命周期(秒)

    # 日志配置参数
    app_log_filename: str = 'app.log'
    app_log_level: str = 'DEBUG'
    app_peewee_debug_log: bool = True

    # 数据刷新时间配置
    line_update_data_interval: int = 5000
    fault_update_data_interval: int = 10000

    # 部件耗用率选择
    #health_bar_data_rnd = ['1633', '1634', '1635', '1636', '1637', '1638', '1639', '1640', '1641', '1642', '1643', '1644', '12101']
    health_bar_data_rnd: List[str] = ['12101']

    # 外部连接配置
    # 外部链接打开方式 ['_blank', '_self', '_parent', '_top']
    external_link_target: str = '_blank'
    # 首页-“一期空调状态跳转地址”
    external_main_status_url: str = 'https://www.baidu.com'
    # 首页-“一期故障跳转地址”
    external_main_fault_url: str = 'https://www.baidu.com'
    # 首页-“一期预警跳转地址”
    external_main_predict_url: str = 'https://www.baidu.com'
    # 首页-“一期寿命跳转地址”
    external_main_health_url: str = 'https://www.baidu.com'
    # 设备参数页面-“一期运行参数跳转地址”
    external_param_url: str = 'https://www.baidu.com'
    # 设备参数页面-“一期故障&预警跳转地址”
    external_fault_url: str = 'https://www.baidu.com'
