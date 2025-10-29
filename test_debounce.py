#!/usr/bin/env python3
"""
测试防抖功能的脚本
"""

import time
import requests
from urllib.parse import urljoin

def test_menu_debounce():
    """测试菜单防抖功能"""
    base_url = "http://192.168.32.228:8050/sz16phmHVAC2"
    
    print("=== 测试菜单防抖功能 ===")
    
    # 测试场景1：快速双击线路菜单
    print("\n1. 测试快速双击线路菜单...")
    start_time = time.time()
    
    # 模拟快速双击
    for i in range(2):
        response = requests.get(f"{base_url}/line")
        print(f"   第{i+1}次请求: {response.status_code}")
        time.sleep(0.1)  # 100ms间隔，小于防抖时间300ms
    
    end_time = time.time()
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    
    # 测试场景2：快速双击参数菜单
    print("\n2. 测试快速双击参数菜单...")
    start_time = time.time()
    
    for i in range(2):
        response = requests.get(f"{base_url}/param?train_no=12101&carriage_no=6")
        print(f"   第{i+1}次请求: {response.status_code}")
        time.sleep(0.1)
    
    end_time = time.time()
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    
    # 测试场景3：正常间隔点击
    print("\n3. 测试正常间隔点击...")
    start_time = time.time()
    
    for i in range(2):
        response = requests.get(f"{base_url}/train")
        print(f"   第{i+1}次请求: {response.status_code}")
        time.sleep(0.5)  # 500ms间隔，大于防抖时间300ms
    
    end_time = time.time()
    print(f"   总耗时: {end_time - start_time:.2f}秒")

def test_url_params_persistence():
    """测试URL参数保持功能"""
    base_url = "http://192.168.32.228:8050/sz16phmHVAC2"
    
    print("\n=== 测试URL参数保持功能 ===")
    
    # 测试场景：带参数的页面跳转
    test_params = [
        ("/param", "?train_no=12101&carriage_no=6"),
        ("/fault", "?train_no=12101&carriage_no=6&fault_type=预警"),
        ("/health", "?train_no=12101&carriage_no=6&component_type=空调"),
    ]
    
    for path, params in test_params:
        url = f"{base_url}{path}{params}"
        print(f"\n测试URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   状态码: {response.status_code}")
            print(f"   页面标题: {extract_title(response.text)}")
        except requests.exceptions.RequestException as e:
            print(f"   请求失败: {e}")

def extract_title(html_content):
    """从HTML内容中提取标题"""
    import re
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if title_match:
        return title_match.group(1)
    return "未找到标题"

if __name__ == "__main__":
    print("开始测试防抖功能...")
    
    try:
        test_menu_debounce()
        test_url_params_persistence()
        print("\n=== 测试完成 ===")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
