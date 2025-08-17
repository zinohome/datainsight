from peewee import Model, DateTimeField, IntegerField, TextField, FloatField
from orm.db import db, initialize_db, close_db


class DChartHealthClean(Model):
    """d_chart_health_clean表的ORM模型
    该表存储设备健康清洁相关数据
    """
    clean_time = DateTimeField(verbose_name='清洁时间', primary_key=True)
    车号 = IntegerField(verbose_name='车号')
    车厢号 = IntegerField(verbose_name='车厢号')
    部件 = TextField(verbose_name='部件')
    已耗 = FloatField(verbose_name='已耗')

    class Meta:
        database = db
        table_name = 'd_chart_health_clean'
        schema = 'public'
        ordering = ['clean_time']
        indexes = (
            (('车号', '车厢号'), False),
            (('部件',), False),
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
        query = DChartHealthClean.select().order_by(
            DChartHealthClean.clean_time.desc()
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(DChartHealthClean.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"清洁时间: {record.clean_time}")
            logger.info(f"车号: {record.车号}")
            logger.info(f"车厢号: {record.车厢号}")
            logger.info(f"部件: {record.部件}")
            logger.info(f"已耗: {record.已耗}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")