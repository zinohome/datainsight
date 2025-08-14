from playhouse.pool import PooledPostgresqlExtDatabase, PooledPostgresqlDatabase
from configs.base_config import BaseConfig
import threading
import time
from utils.log import log as log

# 初始化数据库连接池
db = PooledPostgresqlDatabase(
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

# 添加连接池监控方法
def get_pool_status():
    """
    获取连接池状态信息
    :return: 包含已使用连接数、空闲连接数和最大连接数的字典
    """
    try:
        with db._pool_lock:  # 确保线程安全
            return {
                'used': len(db._in_use),
                'idle': len(db._connections),
                'max': db._max_connections,
                'utilization': round(len(db._in_use) / db._max_connections * 100, 2) if db._max_connections else 0
            }
    except Exception as e:
        log.error(f"获取连接池状态失败: {str(e)}")
        return {'used': -1, 'idle': -1, 'max': db._max_connections if hasattr(db, '_max_connections') else -1, 'utilization': -1}

# 添加连接池状态日志输出方法
def log_pool_status():
    """记录连接池状态日志"""
    status = get_pool_status()
    if status['used'] != -1:
        log.debug(f"连接池状态: 已使用={status['used']}, 空闲={status['idle']}, 总数={status['max']}, 使用率={status['utilization']}%")
    return status


def start_pool_cleaner(interval=60):
    """
    启动连接池清理线程，定期关闭闲置连接
    :param interval: 清理间隔（秒）
    """

    def cleaner():
        while True:
            time.sleep(interval)
            try:
                with db._pool_lock:
                    # 关闭所有空闲连接（根据业务需求调整策略）
                    if len(db._connections) > 10:  # 空闲连接超过10个时清理
                        closed = len(db._connections)
                        db._connections = []  # 清空空闲连接堆
                        log.debug(f"清理连接池: 关闭{closed}个空闲连接")
            except Exception as e:
                log.error(f"连接池清理失败: {str(e)}")

    thread = threading.Thread(target=cleaner, daemon=True)
    thread.start()
    log.debug("连接池自动清理线程已启动")

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