from peewee import Model, CharField, DateTimeField, IntegerField, FloatField
from pytz import timezone
from orm.db import db, initialize_db, close_db

class Chart_view_param(Model):
    msg_calc_dvc_time = DateTimeField(verbose_name='时间')
    msg_calc_dvc_no = CharField(max_length=50, verbose_name='设备编号')
    msg_calc_train_no = CharField(max_length=50, verbose_name='列车编号')
    dvc_train_no = CharField(max_length=50, verbose_name='车号')
    dvc_carriage_no = IntegerField(verbose_name='车厢号')
    param_name = CharField(max_length=200, verbose_name='参数名称')
    param_value = FloatField(verbose_name='数值')

    def formatted_time_minute(self):
        """返回上海时区格式化的时间字符串"""
        if not self.msg_calc_dvc_time:
            return
        shanghai_tz = timezone('Asia/Shanghai')
        return self.msg_calc_dvc_time.astimezone(shanghai_tz).strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db
        table_name = 'pro_param_transposed'
        primary_key = False
        schema = 'public'
        indexes = (
            (('param_name', 'dvc_train_no', 'dvc_carriage_no', 'msg_calc_dvc_time'), False),
            (('msg_calc_dvc_time', 'dvc_train_no', 'param_name'), False),
            (('msg_calc_dvc_time'), False),
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
        """打印所有字段的verbose_name"""
        print("表字段中文名称列表：")
        for idx, (field_name, verbose_name) in enumerate(cls.get_all_verbose_names().items(), 1):
            print(f"  {idx}. {verbose_name} ({field_name})")

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        initialize_db()
        logger.info("数据库连接成功")

        # 测试查询最近10条记录
        query = Chart_view_param.select().order_by(Chart_view_param.msg_calc_dvc_time.desc()).limit(10)
        logger.info(f"查询到 {query.count()} 条记录")
        logger.info("字段名称: " + ", ".join(Chart_view_param.get_all_verbose_names().values()))

        for i, record in enumerate(query, 1):
            logger.info(f"\n记录 {i}:")
            logger.info(f"时间: {record.formatted_time_minute()}")
            logger.info(f"设备编号: {record.msg_calc_dvc_no}")
            logger.info(f"列车编号: {record.msg_calc_train_no}")
            logger.info(f"车号: {record.dvc_train_no}")
            logger.info(f"车厢号: {record.dvc_carriage_no}")
            logger.info(f"参数名称: {record.param_name}")
            logger.info(f"数值值: {record.param_value:.2f}")

    except Exception as e:
        logger.error(f"测试错误: {str(e)}", exc_info=True)
    finally:
        close_db()
        logger.info("数据库连接已关闭")