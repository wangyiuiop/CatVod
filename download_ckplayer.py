#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载并分析 /jsplayer/ckplayer.js
"""
import requests
import re
import json
import time
import random

BASE_URL = "https://www.lmm85.com"
API_URL = "https://yun.92cj.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': API_URL,
    'Accept': '*/*',
}

def get(url, headers=None):
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1))
    return requests.get(url, headers=req_headers, timeout=15)

def download_ckplayer():
    print("="*70)
    print("下载 ckplayer.js")
    print("="*70)
    
    url = f"{API_URL}/jsplayer/ckplayer.js"
    
    print(f"\n📄 下载: {url}")
    
    try:
        response = get(url, headers={'Referer': API_URL})
        print(f"   状态码: {response.status_code}, 长度: {len(response.text)}")
        
        filename = 'ckplayer.js'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"\n✅ 已保存到: {filename}")
        
        print(f"\n🔍 关键搜索:")
        
        keywords = ['sing', 'token', 'md5', 'encrypt', 'hdMd5']
        for k in keywords:
            if k in response.text:
                print(f"   ✅ 包含 {k}")
                
                # 找到周围的代码
                idx = response.text.find(k)
                start = max(0, idx - 100)
                end = min(len(response.text), idx + 200)
                print(f"\n   ...{response.text[start:end]}...")
                
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    download_ckplayer()
