from peewee import Model, CharField, IntegerField, FloatField
from orm.db import db, initialize_db, close_db


class ChartHealthEquipment(Model):
    """chart_health_equipment视图的ORM模型
    该视图通过UNION ALL组合了dev_view_health_equipment_mat和pro_view_health_equipment_mat两个表的健康状态数据
    """
    车号 = CharField(max_length=50, verbose_name='车号')
    车厢号 = IntegerField(verbose_name='车厢号')
    部件 = CharField(max_length=200, verbose_name='部件')
    耗用率 = FloatField(verbose_name='耗用率')
    额定寿命 = FloatField(verbose_name='额定寿命')
    已耗 = FloatField(verbose_name='已耗')

    class Meta:
        database = db
        table_name = 'chart_health_equipment'
        primary_key = False
        schema = 'public'
        ordering = ['车号', '车厢号', '-耗用率']
        indexes = (
            (('车号', '车厢号'), False),
            (('部件',), False),
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
        query = ChartHealthEquipment.select().order_by(
            ChartHealthEquipment.车号, 
            ChartHealthEquipment.车厢号, 
            ChartHealthEquipment.耗用率.desc()
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartHealthEquipment.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"车号: {record.车号}")
            logger.info(f"车厢号: {record.车厢号}")
            logger.info(f"部件: {record.部件}")
            logger.info(f"耗用率: {record.耗用率:.2%}")
            logger.info(f"额定寿命: {record.额定寿命}")
            logger.info(f"已耗: {record.已耗}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")