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
    stale_timeout=BaseConfig.db_stale_timeout,
    timeout=BaseConfig.db_timeout,
    autocommit=True,  # 添加自动提交
)


def initialize_db():
    """初始化数据库连接"""
    if db.is_closed():
        db.connect()


def close_db():
    """关闭数据库连接"""
    if not db.is_closed():
        db.close()


'''
from contextlib import contextmanager
import time
import logging

logger = logging.getLogger(__name__)

@contextmanager
def monitored_connection():
    """带监控的数据库连接上下文管理器"""
    start_time = time.time()
    conn = db.connection()
    try:
        yield conn
    finally:
        # 记录连接使用时长
        duration = time.time() - start_time
        if duration > 5:  # 记录慢查询
            logger.warning(f"数据库连接使用超时: {duration:.2f}秒")
        # 归还连接前检查状态
        if not db.is_closed():
            db.close()
'''