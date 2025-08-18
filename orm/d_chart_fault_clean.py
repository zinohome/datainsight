from peewee import Model, DateTimeField, IntegerField, TextField
from orm.db import db, initialize_db, close_db


class DChartFaultClean(Model):
    """d_chart_fault_clean表的ORM模型
    该表存储设备故障清洁相关数据
    """
    clean_time = DateTimeField(verbose_name='清洁时间', primary_key=True)
    dvc_train_no = IntegerField(verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    param_name = TextField(verbose_name='参数名称')
    start_time = DateTimeField(verbose_name='开始时间', null=True)
    fault_level = IntegerField(verbose_name='故障等级', null=True)
    fault_type = TextField(verbose_name='故障类型')

    class Meta:
        database = db
        table_name = 'd_chart_fault_clean'
        schema = 'public'
        ordering = ['clean_time']
        indexes = (
            (('dvc_train_no', 'dvc_carriage_no'), False),
            (('param_name',), False),
            (('fault_type',), False),
        )

    @classmethod
    def get_all_verbose_names(cls):
        # 获取所有字段的verbose_name字典
        return {
            field_name: field.verbose_name 
            for field_name, field in cls._meta.fields.items()
            if hasattr(field, 'verbose_name')
        }

    @classmethod
    def print_verbose_names(cls):
        # 打印所有字段的verbose_name
        print("表字段中文名称列表：")
        for idx, (field_name, verbose_name) in enumerate(cls.get_all_verbose_names().items(), 1):
            print(f"  {idx}. {verbose_name} ({field_name}) ")


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        initialize_db()
        logger.info("数据库连接成功")

        # 测试查询最近10条记录
        query = DChartFaultClean.select().order_by(
            DChartFaultClean.clean_time.desc()
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(DChartFaultClean.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"清洁时间: {record.clean_time}")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"车厢号: {record.dvc_carriage_no}")
            logger.info(f"参数名称: {record.param_name}")
            logger.info(f"开始时间: {record.start_time}")
            logger.info(f"故障等级: {record.fault_level}")
            logger.info(f"故障类型: {record.fault_type}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")