"""
ORM 模型测试
测试所有 ORM 模型的连接、查询和字段功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from orm.db import initialize_db, close_db
from orm.chart_health_equipment import ChartHealthEquipment
from orm.chart_view_fault_timed import Chart_view_fault_timed
from orm.chart_line_fault_param_type import ChartLineFaultParamType
from orm.chart_table_fault_timed import Chart_table_fault_timed
from orm.chart_view_param_test import Chart_view_param

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """测试数据库连接"""
    try:
        initialize_db()
        logger.info("✅ 数据库连接成功")
        return True
    except Exception as e:
        logger.error(f"❌ 数据库连接失败: {str(e)}")
        return False
    finally:
        close_db()

def test_chart_health_equipment():
    """测试健康设备模型"""
    try:
        initialize_db()
        
        # 测试查询
        query = ChartHealthEquipment.select().limit(5)
        count = query.count()
        logger.info(f"✅ ChartHealthEquipment 查询成功，共 {count} 条记录")
        
        # 测试字段
        if count > 0:
            first_record = query.first()
            logger.info(f"✅ 第一条记录字段: {list(first_record._meta.fields.keys())}")
            
            # 检查新字段是否存在
            if hasattr(first_record, '车厢'):
                logger.info("✅ 新字段 '车厢' 存在")
            else:
                logger.warning("⚠️ 新字段 '车厢' 不存在")
        
        return True
    except Exception as e:
        logger.error(f"❌ ChartHealthEquipment 测试失败: {str(e)}")
        return False
    finally:
        close_db()

def test_chart_view_fault_timed():
    """测试故障时间视图模型"""
    try:
        initialize_db()
        
        # 测试查询
        query = Chart_view_fault_timed.select().limit(5)
        count = query.count()
        logger.info(f"✅ Chart_view_fault_timed 查询成功，共 {count} 条记录")
        
        # 测试字段
        if count > 0:
            first_record = query.first()
            logger.info(f"✅ 第一条记录字段: {list(first_record._meta.fields.keys())}")
            
            # 检查新字段是否存在
            if hasattr(first_record, 'msg_calc_dvc_no'):
                logger.info("✅ 新字段 'msg_calc_dvc_no' 存在")
            else:
                logger.warning("⚠️ 新字段 'msg_calc_dvc_no' 不存在")
                
            if hasattr(first_record, 'fault_name'):
                logger.info("✅ 重命名字段 'fault_name' 存在")
            else:
                logger.warning("⚠️ 重命名字段 'fault_name' 不存在")
                
            if hasattr(first_record, 'update_time'):
                logger.info("✅ 新字段 'update_time' 存在")
            else:
                logger.warning("⚠️ 新字段 'update_time' 不存在")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chart_view_fault_timed 测试失败: {str(e)}")
        return False
    finally:
        close_db()

def test_chart_line_fault_param_type():
    """测试故障参数类型模型"""
    try:
        initialize_db()
        
        # 测试查询
        query = ChartLineFaultParamType.select().limit(5)
        count = query.count()
        logger.info(f"✅ ChartLineFaultParamType 查询成功，共 {count} 条记录")
        
        # 测试字段
        if count > 0:
            first_record = query.first()
            logger.info(f"✅ 第一条记录字段: {list(first_record._meta.fields.keys())}")
        
        return True
    except Exception as e:
        logger.error(f"❌ ChartLineFaultParamType 测试失败: {str(e)}")
        return False
    finally:
        close_db()

def test_chart_table_fault_timed():
    """测试故障记录表模型"""
    try:
        initialize_db()
        
        # 测试查询
        query = Chart_table_fault_timed.select().limit(5)
        count = query.count()
        logger.info(f"✅ Chart_table_fault_timed 查询成功，共 {count} 条记录")
        
        # 测试字段
        if count > 0:
            first_record = query.first()
            logger.info(f"✅ 第一条记录字段: {list(first_record._meta.fields.keys())}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chart_table_fault_timed 测试失败: {str(e)}")
        return False
    finally:
        close_db()

def test_chart_view_param():
    """测试参数视图模型"""
    try:
        initialize_db()
        
        # 测试查询
        count = Chart_view_param.select().count()
        logger.info(f"✅ Chart_view_param 查询成功，共 {count} 条记录")
        
        # 如果表为空，检查表结构
        if count == 0:
            logger.info("✅ 表为空，但表结构存在")
            return True
        
        # 测试字段
        query = Chart_view_param.select().limit(1)
        first_record = query.first()
        if first_record:
            logger.info(f"✅ 第一条记录字段: {list(first_record._meta.fields.keys())}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chart_view_param 测试失败: {str(e)}")
        return False
    finally:
        close_db()

def run_all_tests():
    """运行所有测试"""
    logger.info("🚀 开始 ORM 模型测试...")
    
    tests = [
        ("数据库连接", test_database_connection),
        ("健康设备模型", test_chart_health_equipment),
        ("故障时间视图模型", test_chart_view_fault_timed),
        ("故障参数类型模型", test_chart_line_fault_param_type),
        ("参数视图模型", test_chart_view_param),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n📋 测试: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # 输出测试结果
    logger.info("\n📊 测试结果汇总:")
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 测试完成: {passed}/{len(tests)} 通过")
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
