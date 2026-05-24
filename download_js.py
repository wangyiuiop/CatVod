#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载并分析核心JS文件
"""
import requests
import re
import json
import time
import random

BASE_URL = "https://www.lmm85.com"
API_URL = "https://yun.92cj.com"

# 模拟浏览器请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': API_URL,
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get(url, headers=None):
    """发送GET请求"""
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1))
    return requests.get(url, headers=req_headers, timeout=15)

def download_js_files():
    """下载核心JS文件"""
    print("="*70)
    print("下载核心JS文件...")
    print("="*70)
    
    js_files = [
        f"{API_URL}/jsplayer/a.js",
        f"{API_URL}/jsplayer/b.js",
    ]
    
    for i, url in enumerate(js_files):
        print(f"\n📄 下载 ({i+1}/{len(js_files)}): {url}")
        try:
            response = get(url, headers={'Referer': API_URL})
            print(f"✅ 状态码: {response.status_code}, 长度: {len(response.text)}")
            
            filename = f'debug_core_{i+1}.js'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"📝 已保存到: {filename}")
            
            # 简单分析
            print(f"\n🔍 简单分析 ({filename}):")
            
            # 查找token相关函数
            if 'token' in response.text.lower():
                print("   包含 'token' 相关内容")
                
            # 查找md5相关
            if 'md5' in response.text.lower():
                print("   包含 'md5' 相关内容")
                
            # 查找encrypt/encode相关
            if 'encrypt' in response.text.lower() or 'encode' in response.text.lower():
                print("   包含加密/编码相关内容")
                
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    print("\n" + "="*70)
    print("下载完成！")
    print("="*70)

if __name__ == "__main__":
    download_js_files()
