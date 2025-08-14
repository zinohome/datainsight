import random

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from configs.base_config import BaseConfig
from utils.log import log as log

class DBQuery:
    def __init__(self):
        """
        初始化数据库连接池
        """
        self.logger = log
        self.connection_pool = None
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=BaseConfig.db_minconn,
                maxconn=BaseConfig.db_maxconn,
                dbname=BaseConfig.db_dbname,
                user=BaseConfig.db_user,
                password=BaseConfig.db_password,
                host=BaseConfig.db_host,
                port=BaseConfig.db_port
            )
            if self.connection_pool:
                self.logger.debug(f"成功创建DB连接池，最小连接数: {BaseConfig.db_minconn}, 最大连接数: {BaseConfig.db_maxconn}")
        except Exception as e:
            self.logger.error(f"创建连接池失败: {str(e)}", exc_info=True)
            raise

    def get_connection(self):
        """从连接池获取连接"""
        if not self.connection_pool:
            raise Exception("连接池未初始化")
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        """将连接释放回连接池"""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)

    def execute_query(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        use_server_side_cursor: bool = False,
        cursor_name: str = 'server_side_cursor'
    ) -> List[Dict[str, Any]]:
        """
        执行SQL查询
        :param sql: SQL语句
        :param params: SQL参数 (字典形式，用于参数化查询)
        :param use_server_side_cursor: 是否使用服务器端游标（处理大量数据时推荐）
        :param cursor_name: 服务器端游标名称
        :return: 查询结果列表
        """
        conn = None
        cursor = None
        results = []
        try:
            conn = self.get_connection()
            conn.autocommit = True  # 自动提交，适用于查询操作

            # 根据是否使用服务器端游标选择不同的cursor类型
            if use_server_side_cursor:
                cursor = conn.cursor(name=cursor_name, cursor_factory=RealDictCursor)
            else:
                cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 执行查询，使用参数化查询防止SQL注入
            cursor.execute(sql, params or {})

            # 如果是SELECT类查询，获取结果
            if cursor.description:
                results = cursor.fetchall()
                self.logger.debug(f"查询成功，返回 {len(results)} 条记录")
            else:
                self.logger.debug(f"执行成功，影响行数: {cursor.rowcount}")

            return results

        except Exception as e:
            self.logger.error(f"执行SQL失败: {str(e)}", exc_info=True)
            raise
        finally:
            # 确保游标和连接被正确关闭和释放
            if cursor:
                cursor.close()
            if conn:
                self.release_connection(conn)

    def close_all_connections(self):
        """关闭连接池中的所有连接"""
        if self.connection_pool:
            self.connection_pool.closeall()
            self.logger.info("已关闭连接池中的所有连接")

# 使用示例
if __name__ == '__main__':
    # 初始化查询类
    db_query = DBQuery()
    # 执行查询
    try:
        # 普通查询
        #sql = "SELECT  dvc_train_no as 车号,  dvc_carriage_no as 车厢号,  param_name as 故障名称,  start_time as 开始时间, status as 状态,  end_time as 结束时间,  fault_level as 故障等级,  fault_type as 类型,  repair_suggestion as 维修建议  FROM public.chart_view_fault_timed"
        sql = "SELECT field_name FROM public.sys_fields where field_category='Param'"
        #params = {'age': 18}
        results = db_query.execute_query(sql)
        log.debug(f"普通查询结果: {results}")
        # 提取field_name值到数组
        field_names = [item['field_name'] for item in results]
        log.debug(f"field_name数组: {field_names}")

        data = [
            {
                'carriage': f'12101-{i}',
                'ratio': random.randint(0, 100),
                'param': f'item{j}',
            }
            for i in range(1, 7)
            for j in range(1, 4)
        ],
        log.debug(f"数据: {data}")
        '''
        # 大量数据查询（使用服务器端游标）
        large_sql = "SELECT * FROM large_table"
        large_results = db_query.execute_query(large_sql, use_server_side_cursor=False)
        # 建议迭代处理大量结果
        for row in large_results:
            print(f"处理记录: {row['id']}")
        '''

    finally:
        # 程序退出时关闭所有连接
        db_query.close_all_connections()