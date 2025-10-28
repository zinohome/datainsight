from peewee import Model, CharField, IntegerField
from orm.db import db, initialize_db, close_db


class ChartLineFaultParamType(Model):
    """chart_line_fault_param_type视图的ORM模型
    """
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    故障部件 = CharField(max_length=100, verbose_name='故障部件')
    故障数量 = IntegerField(verbose_name='故障数量')

    class Meta:
        database = db
        table_name = 'chart_line_fault_param_type'
        primary_key = False
        schema = 'public'
        ordering = ['dvc_train_no', '故障数量']
        indexes = (
            (('dvc_train_no'), False),
        )

    @classmethod
    def get_all_verbose_names(cls):
        #获取所有字段的verbose_name字典
        return {
            field_name: field.verbose_name 
            for field_name, field in cls._meta.fields.items()
            if hasattr(field, 'verbose_name')
        }

    @classmethod
    def print_verbose_names(cls):
        #打印所有字段的verbose_name
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
        query = ChartLineFaultParamType.select().order_by(
            ChartLineFaultParamType.故障部件, ChartLineFaultParamType.dvc_train_no
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartLineFaultParamType.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"故障类型: {record.故障部件}")
            logger.info(f"故障数量: {record.故障数量}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")