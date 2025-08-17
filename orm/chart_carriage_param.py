from peewee import Model, CharField, IntegerField, FloatField
from orm.db import db, initialize_db, close_db


class ChartCarriageParam(Model):
    """chart_carriage_param_current视图的ORM模型
    该视图通过UNION ALL组合了dev_param_transposed和pro_param_transposed两个表的参数数据
    并筛选了最新的空调运行参数数据
    """
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    吸气压力_u11 = FloatField(verbose_name='吸气压力-U11')
    吸气压力_u12 = FloatField(verbose_name='吸气压力-U12')
    吸气压力_u21 = FloatField(verbose_name='吸气压力-U21')
    吸气压力_u22 = FloatField(verbose_name='吸气压力-U22')
    高压压力_u11 = FloatField(verbose_name='高压压力-U11')
    高压压力_u12 = FloatField(verbose_name='高压压力-U12')
    高压压力_u21 = FloatField(verbose_name='高压压力-U21')
    高压压力_u22 = FloatField(verbose_name='高压压力-U22')
    新风温度_u1 = FloatField(verbose_name='新风温度-U1')
    新风温度_u2 = FloatField(verbose_name='新风温度-U2')
    回风温度_u1 = FloatField(verbose_name='回风温度-U1')
    回风温度_u2 = FloatField(verbose_name='回风温度-U2')
    送风温度_u11 = FloatField(verbose_name='送风温度-U11')
    送风温度_u12 = FloatField(verbose_name='送风温度-U12')
    送风温度_u21 = FloatField(verbose_name='送风温度-U21')
    送风温度_u22 = FloatField(verbose_name='送风温度-U22')
    送风温度_u1 = FloatField(verbose_name='送风温度-U1')
    送风温度_u2 = FloatField(verbose_name='送风温度-U2')
    co2_u1 = FloatField(verbose_name='空气质量-CO2-U1')
    co2_u2 = FloatField(verbose_name='空气质量-CO2-U2')
    湿度_u1 = FloatField(verbose_name='空气质量-湿度-U1')
    湿度_u2 = FloatField(verbose_name='空气质量-湿度-U2')
    车厢温度_1 = FloatField(verbose_name='车厢温度-1')
    车厢温度_2 = FloatField(verbose_name='车厢温度-2')
    车厢湿度_1 = FloatField(verbose_name='车厢湿度-1')
    车厢湿度_2 = FloatField(verbose_name='车厢湿度-2')

    class Meta:
        database = db
        table_name = 'chart_carriage_param'
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
        query = ChartCarriageParam.select().order_by(
            ChartCarriageParam.dvc_train_no,
            ChartCarriageParam.dvc_carriage_no
        ).limit(10)

        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(ChartCarriageParam.get_all_verbose_names().values()))

        if query.count() > 0:
            # 打印第一条记录的信息
            record = query[0]
            logger.info("第一条记录:")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"车厢号: {record.dvc_carriage_no}")
            logger.info(f"吸气压力-U11: {record.吸气压力_u11:.2f}")
            logger.info(f"吸气压力-U12: {record.吸气压力_u12:.2f}")
            logger.info(f"吸气压力-U21: {record.吸气压力_u21:.2f}")
            logger.info(f"吸气压力-U22: {record.吸气压力_u22:.2f}")
            logger.info(f"高压压力-U11: {record.高压压力_u11:.2f}")
            logger.info(f"高压压力-U12: {record.高压压力_u12:.2f}")
            logger.info(f"高压压力-U21: {record.高压压力_u21:.2f}")
            logger.info(f"高压压力-U22: {record.高压压力_u22:.2f}")
            logger.info(f"新风温度-U1: {record.新风温度_u1:.1f}°C")
            logger.info(f"新风温度-U2: {record.新风温度_u2:.1f}°C")
            logger.info(f"回风温度-U1: {record.回风温度_u1:.1f}°C")
            logger.info(f"回风温度-U2: {record.回风温度_u2:.1f}°C")
            logger.info(f"送风温度-U11: {record.送风温度_u11:.1f}°C")
            logger.info(f"送风温度-U12: {record.送风温度_u12:.1f}°C")
            logger.info(f"送风温度-U21: {record.送风温度_u21:.1f}°C")
            logger.info(f"送风温度-U22: {record.送风温度_u22:.1f}°C")
            logger.info(f"送风温度-U1: {record.送风温度_u1:.1f}°C")
            logger.info(f"送风温度-U2: {record.送风温度_u2:.1f}°C")
            logger.info(f"空气质量-CO2-U1: {record.co2_u1:.1f}")
            logger.info(f"空气质量-CO2-U2: {record.co2_u2:.1f}")
            logger.info(f"空气质量-湿度-U1: {record.湿度_u1:.1f}%")
            logger.info(f"空气质量-湿度-U2: {record.湿度_u2:.1f}%")
            logger.info(f"车厢温度-1: {record.车厢温度_1:.1f}°C")
            logger.info(f"车厢温度-2: {record.车厢温度_2:.1f}°C")
            logger.info(f"车厢湿度-1: {record.车厢湿度_1:.1f}%")
            logger.info(f"车厢湿度-2: {record.车厢湿度_2:.1f}%")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")