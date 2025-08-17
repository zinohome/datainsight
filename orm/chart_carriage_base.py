from peewee import Model, CharField, IntegerField, FloatField, TextField
from orm.db import db, initialize_db, close_db


class ChartCarriageBase(Model):
    """chart_carriage_base视图的ORM模型
    该视图通过UNION ALL组合了dev_param_transposed和pro_param_transposed两个表的参数数据
    并筛选了最新的空调运行模式、目标温度、新风温度和回风温度数据
    """
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    运行模式 = IntegerField(verbose_name='运行模式')
    目标温度 = FloatField(verbose_name='目标温度')
    新风温度 = FloatField(verbose_name='新风温度')
    回风温度 = FloatField(verbose_name='回风温度')

    class Meta:
        database = db
        table_name = 'c_chart_carriage_base'
        primary_key = False
        schema = 'public'
        ordering = ['dvc_train_no', 'dvc_carriage_no']
        indexes = (
            (('dvc_train_no', 'dvc_carriage_no'), False),
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
        query = ChartCarriageBase.select().order_by(
            ChartCarriageBase.dvc_train_no,
            ChartCarriageBase.dvc_carriage_no
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartCarriageBase.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"车厢号: {record.dvc_carriage_no}")
            logger.info(f"运行模式: {record.运行模式}")
            logger.info(f"目标温度: {record.目标温度:.1f}°C")
            logger.info(f"新风温度: {record.新风温度:.1f}°C")
            logger.info(f"回风温度: {record.回风温度:.1f}°C")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")