"""
动态ORM模型工具模块
根据配置动态创建ORM模型，支持车厢/车厢号字段的切换
"""

from peewee import Model, CharField, IntegerField, FloatField, DateTimeField, TextField
from orm.db import db
from configs import BaseConfig


def get_dynamic_health_model():
    """
    根据配置动态创建健康设备ORM模型
    :return: 动态创建的ORM模型类
    """
    if BaseConfig.use_carriage_field:
        # 使用车厢字段的模型（当数据库中存在车厢字段时）
        class DynamicChartHealthEquipment(Model):
            """动态健康设备模型 - 使用车厢字段"""
            车厢 = CharField(max_length=50, verbose_name='车厢')
            车号 = CharField(max_length=50, verbose_name='车号')
            部件 = CharField(max_length=200, verbose_name='部件')
            耗用率 = FloatField(verbose_name='耗用率')
            额定寿命 = FloatField(verbose_name='额定寿命')
            已耗 = FloatField(verbose_name='已耗')

            class Meta:
                database = db
                table_name = 'c_chart_health_equipment'
                primary_key = False
                schema = 'public'
                ordering = ['-耗用率']
    else:
        # 使用车厢号字段的模型（当数据库中存在车厢号字段时）
        class DynamicChartHealthEquipment(Model):
            """动态健康设备模型 - 使用车厢号字段"""
            车号 = CharField(max_length=50, verbose_name='车号')
            车厢号 = IntegerField(verbose_name='车厢号')
            部件 = CharField(max_length=200, verbose_name='部件')
            耗用率 = FloatField(verbose_name='耗用率')
            额定寿命 = FloatField(verbose_name='额定寿命')
            已耗 = FloatField(verbose_name='已耗')

            class Meta:
                database = db
                table_name = 'c_chart_health_equipment'
                primary_key = False
                schema = 'public'
                ordering = ['-耗用率']
    
    return DynamicChartHealthEquipment


def get_dynamic_fault_model():
    """
    根据配置动态创建故障视图ORM模型
    :return: 动态创建的ORM模型类
    """
    if BaseConfig.use_carriage_field:
        # 使用车厢字段的模型
        class DynamicChartViewFaultTimed(Model):
            """动态故障视图模型 - 使用车厢字段"""
            msg_calc_dvc_no = CharField(max_length=50, verbose_name='车厢')
            dvc_train_no = CharField(max_length=50, verbose_name='车号')
            fault_name = CharField(max_length=200, verbose_name='故障名称')
            start_time = DateTimeField(verbose_name='开始时间')
            end_time = DateTimeField(verbose_name='结束时间')
            update_time = DateTimeField(verbose_name='更新时间')
            status = CharField(max_length=20, verbose_name='状态')
            fault_level = IntegerField(verbose_name='故障等级')
            fault_type = CharField(max_length=50, verbose_name='类型')
            repair_suggestion = TextField(verbose_name='维修建议')

            class Meta:
                database = db
                table_name = 'c_chart_view_fault_timed'
                primary_key = False
                schema = 'public'
                ordering = ['-start_time']
    else:
        # 使用车厢号字段的模型
        class DynamicChartViewFaultTimed(Model):
            """动态故障视图模型 - 使用车厢号字段"""
            dvc_train_no = CharField(max_length=50, verbose_name='车号')
            dvc_carriage_no = IntegerField(verbose_name='车厢号')
            fault_name = CharField(max_length=200, verbose_name='故障名称')
            start_time = DateTimeField(verbose_name='开始时间')
            end_time = DateTimeField(verbose_name='结束时间')
            update_time = DateTimeField(verbose_name='更新时间')
            status = CharField(max_length=20, verbose_name='状态')
            fault_level = IntegerField(verbose_name='故障等级')
            fault_type = CharField(max_length=50, verbose_name='类型')
            repair_suggestion = TextField(verbose_name='维修建议')

            class Meta:
                database = db
                table_name = 'c_chart_view_fault_timed'
                primary_key = False
                schema = 'public'
                ordering = ['-start_time']
    
    return DynamicChartViewFaultTimed
