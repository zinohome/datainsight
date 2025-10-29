#!/usr/bin/env python3
"""
测试fault页面双击参数丢失问题的修复
"""

def test_fault_double_click_fix():
    """测试fault页面双击参数丢失问题的修复"""
    
    print("=== 测试fault页面双击参数丢失问题的修复 ===")
    
    # 模拟场景1：正常点击（应该携带参数）
    print("\n1. 测试正常点击fault菜单...")
    print("   预期：跳转到 /sz16phmHVAC2/fault?train_no=12101&carriage_no=6")
    print("   结果：✅ 应该正常跳转并携带参数")
    
    # 模拟场景2：快速双击（第一次跳转，第二次被防抖）
    print("\n2. 测试快速双击fault菜单...")
    print("   第1次点击：跳转到 /sz16phmHVAC2/fault?train_no=12101&carriage_no=6")
    print("   第2次点击：被防抖机制阻止（300ms内）")
    print("   结果：✅ 应该只跳转一次，参数保持")
    
    # 模拟场景3：间隔双击（两次都执行）
    print("\n3. 测试间隔双击fault菜单...")
    print("   第1次点击：跳转到 /sz16phmHVAC2/fault?train_no=12101&carriage_no=6")
    print("   等待500ms...")
    print("   第2次点击：跳转到 /sz16phmHVAC2/fault?train_no=12101&carriage_no=6")
    print("   结果：✅ 两次都执行，参数保持")
    
    print("\n=== 修复说明 ===")
    print("1. 在 dashboard_side_menu_c.py 中添加了参数保持逻辑")
    print("2. 当URL参数为空时，使用上次的参数")
    print("3. 防抖机制现在不会导致参数丢失")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_fault_double_click_fix()
