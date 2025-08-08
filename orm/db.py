from playhouse.pool import PooledPostgresqlExtDatabase
from configs.base_config import BaseConfig

# 初始化数据库连接池
db = PooledPostgresqlExtDatabase(
    database=BaseConfig.db_dbname,
    user=BaseConfig.db_user,
    password=BaseConfig.db_password,
    host=BaseConfig.db_host,
    port=int(BaseConfig.db_port),
    max_connections=BaseConfig.db_maxconn,
    stale_timeout=BaseConfig.db_stale_timeout,  # 5分钟闲置连接超时回收
    timeout=BaseConfig.db_timeout,
)


def initialize_db():
    """初始化数据库连接"""
    if db.is_closed():
        db.connect()


def close_db():
    """关闭数据库连接"""
    if not db.is_closed():
        db.close()