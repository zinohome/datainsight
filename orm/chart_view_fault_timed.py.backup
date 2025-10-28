from peewee import Model, CharField, DateTimeField, IntegerField, TextField
from pytz import timezone
from orm.db import db, initialize_db, close_db  # 导入db模块

class Chart_view_fault_timed(Model):
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    param_name = CharField(max_length=200, verbose_name='故障名称')
    start_time = DateTimeField(verbose_name='开始时间')
    end_time = DateTimeField(verbose_name='结束时间')
    status = CharField(max_length=20, verbose_name='状态')
    fault_level = IntegerField(verbose_name='故障等级')
    fault_type = CharField(max_length=50, verbose_name='类型')
    repair_suggestion = TextField(verbose_name='维修建议')

    def formatted_start_time(self):
        """返回上海时区格式化的开始时间字符串"""
        if not self.start_time:
            return
        shanghai_tz = timezone('Asia/Shanghai')
        return self.start_time.astimezone(shanghai_tz).strftime('%Y-%m-%d %H:%M:%S')

    def formatted_end_time(self):
        """返回上海时区格式化的结束时间字符串"""
        if not self.end_time:
            return "N/A"
        shanghai_tz = timezone('Asia/Shanghai')
        return self.end_time.astimezone(shanghai_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        database = db  # 使用db.py中的数据库连接
        table_name = 'c_chart_view_fault_timed'
        primary_key = False
        schema = 'public'
        indexes = (
            (('dvc_train_no', 'start_time'), False),
            (('status', 'fault_level'), False),
        )

    @classmethod
    def get_all_verbose_names(cls):
        """获取所有字段的verbose_name字典"""
        return {
            field_name: field.verbose_name 
            for field_name, field in cls._meta.fields.items()
            if hasattr(field, 'verbose_name')
        }

    @classmethod
    def print_verbose_names(cls):
        """打印所有字段的verbose_name（带格式化输出）"""
        print("表字段中文名称列表：")
        for idx, (field_name, verbose_name) in enumerate(cls.get_all_verbose_names().items(), 1):
            print(f"  {idx}. {verbose_name} ({field_name})")

if __name__ == '__main__':
    import logging
    # 配置日志输出
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # 初始化数据库连接
        initialize_db()  # 使用db.py中的初始化函数
        logger.info("数据库连接成功")

        # 测试查询（使用server-side cursor模式）
        logger.info("开始测试查询...")
        query = Chart_view_fault_timed.select().limit(10).order_by(Chart_view_fault_timed.start_time.desc())

        # 打印查询结果
        logger.info(Chart_view_fault_timed.get_all_verbose_names().values())
        logger.info(Chart_view_fault_timed._meta.fields.keys())
        logger.info(f"共查询到 {query.count()} 条记录")
        for i, fault in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"车号: {fault.dvc_train_no}")
            logger.info(f"车厢号: {fault.dvc_carriage_no}")
            logger.info(f"故障名称: {fault.param_name}")
            logger.info(f"开始时间: {fault.formatted_start_time()}")
            logger.info(f"结束时间: {fault.formatted_end_time()}")
            logger.info(f"状态: {fault.status}")
            logger.info(f"故障等级: {fault.fault_level}")
            logger.info(f"类型: {fault.fault_type}")
            logger.info(f"维修建议: {fault.repair_suggestion}...")  # 只显示前50个字符

    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
    finally:
        # 确保连接关闭
        close_db()  # 使用db.py中的关闭函数
        logger.info("数据库连接已关闭")