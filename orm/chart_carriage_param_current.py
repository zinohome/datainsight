from peewee import Model, CharField, IntegerField, FloatField
from orm.db import db, initialize_db, close_db


class ChartCarriageParamCurrent(Model):
    """chart_carriage_param_current视图的ORM模型
    该视图通过UNION ALL组合了dev_param_transposed和pro_param_transposed两个表的参数数据
    并筛选了最新的通风机、压缩机和冷凝风机电流数据
    """
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    param_name = CharField(max_length=100, verbose_name='参数名称')
    param_value = FloatField(verbose_name='参数值')

    class Meta:
        database = db
        table_name = 'c_chart_carriage_param_current'
        primary_key = False
        schema = 'public'
        ordering = ['dvc_train_no', 'param_name', '-msg_time']
        indexes = (
            (('dvc_train_no', 'param_name'), False),
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
        query = ChartCarriageParamCurrent.select().order_by(
            ChartCarriageParamCurrent.dvc_train_no,
            ChartCarriageParamCurrent.param_name
        ).limit(10)
        
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartCarriageParamCurrent.get_all_verbose_names().values()))

        if query.count() > 0:
            # 打印所有记录的信息
            logger.info("\n查询结果记录:")
            for i, record in enumerate(query, 1):
                logger.info(f"记录 {i}:")
                logger.info(f"车号: {record.dvc_train_no}")
                logger.info(f"车厢号: {record.dvc_carriage_no}")
                logger.info(f"参数名称: {record.param_name}")
                logger.info(f"参数值: {record.param_value:.2f}")
                logger.info("---")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")