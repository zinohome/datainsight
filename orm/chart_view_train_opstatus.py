from peewee import Model, CharField, IntegerField, DateTimeField, FloatField
from orm.db import db, initialize_db, close_db


class ChartViewTrainOpstatus(Model):
    """chart_view_train_opstatus视图的ORM模型
    该视图通过UNION ALL组合了dev_view_train_opstatus和pro_view_train_opstatus两个表的运行状态数据
    """
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    latest_op_condition = CharField(max_length=100, verbose_name='最新运行状态')
    latest_time = DateTimeField(verbose_name='最新时间')
    立即维修 = IntegerField(verbose_name='立即维修')
    加强跟踪 = IntegerField(verbose_name='加强跟踪')
    计划维修 = IntegerField(verbose_name='计划维修')
    正常运营 = IntegerField(verbose_name='正常运营')

    class Meta:
        database = db
        table_name = 'chart_view_train_opstatus'
        primary_key = False
        schema = 'public'
        ordering = ['dvc_train_no']
        indexes = (
            (('dvc_train_no',), False),
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
        query = ChartViewTrainOpstatus.select().order_by(
            ChartViewTrainOpstatus.dvc_train_no
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartViewTrainOpstatus.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"最新运行状态: {record.latest_op_condition}")
            logger.info(f"最新时间: {record.latest_time}")
            logger.info(f"立即维修: {record.立即维修}")
            logger.info(f"加强跟踪: {record.加强跟踪}")
            logger.info(f"计划维修: {record.计划维修}")
            logger.info(f"正常运营: {record.正常运营}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")