#!/usr/bin/env python3
"""
测试 4kvm.tv 源
快速验证所有功能是否正常工作
"""

import requests
import json

BASE = "http://127.0.0.1:5000"

print("="*70)
print("4kvm.tv 源功能测试")
print("="*70)

# 测试1：主页
print("\n[1] 测试主页...")
try:
    r = requests.get(f"{BASE}/api.php/provide/vod/", timeout=10)
    data = r.json()
    print(f"    ✓ 成功，获取到 {len(data.get('list', []))} 个结果")
    if data.get('list'):
        first = data['list'][0]
        print(f"    示例: {first.get('vod_name', 'N/A')}")
except Exception as e:
    print(f"    ✗ 失败: {e}")

# 测试2：分类
print("\n[2] 测试电影分类...")
try:
    r = requests.get(f"{BASE}/api.php/provide/vod/?ac=list&t=1", timeout=10)
    data = r.json()
    print(f"    ✓ 成功，获取到 {len(data.get('list', []))} 个结果")
except Exception as e:
    print(f"    ✗ 失败: {e}")

# 测试3：搜索
print("\n[3] 测试搜索功能...")
try:
    r = requests.get(f"{BASE}/api.php/provide/vod/?wd=飞驰", timeout=10)
    data = r.json()
    print(f"    ✓ 成功，找到 {len(data.get('list', []))} 个结果")
    if data.get('list'):
        first = data['list'][0]
        print(f"    示例: {first.get('vod_name', 'N/A')}")
except Exception as e:
    print(f"    ✗ 失败: {e}")

# 测试4：config
print("\n[4] 测试配置文件...")
try:
    r = requests.get(f"{BASE}/config.js", timeout=10)
    if r.status_code == 200:
        print("    ✓ 成功")
except Exception as e:
    print(f"    ✗ 失败: {e}")

print("\n" + "="*70)
print("测试完成")
print("="*70)
print("\n💡 提示:")
print("  为了测试播放功能，请先确保:")
print("  1. 已安装 Playwright: pip install playwright")
print("  2. 已下载浏览器: playwright install chromium")
print("  3. 服务正在运行: python tvbox_complete.py")
