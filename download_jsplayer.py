#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载并分析 /jsplayer/ 下的核心JS
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

def download_and_analyze():
    print("="*70)
    print("下载核心JS并分析")
    print("="*70)
    
    js_files = [
        f"{API_URL}/jsplayer/a.js",
        f"{API_URL}/jsplayer/b.js",
    ]
    
    for i, url in enumerate(js_files):
        print(f"\n📄 {i+1}. 下载 {url}")
        
        try:
            response = get(url, headers={'Referer': API_URL})
            print(f"   状态码: {response.status_code}, 长度: {len(response.text)}")
            
            filename = f'jsplayer_{i}.js'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"   已保存到: {filename}")
            
            print(f"\n🔍 分析内容:")
            
            # 查找关键函数
            if 'md5' in response.text.lower():
                print("   ✅ 包含 md5")
            
            for keyword in ['encrypt', 'decrypt', 'token', 'sing', 'base64']:
                if keyword in response.text:
                    print(f"   ✅ 包含 {keyword}")
            
            # 查找eval混淆
            if 'eval(' in response.text:
                print(f"\n⚠️ 发现 eval 混淆!")
                
                # 尝试简单解混淆
                eval_pattern = r'eval\s*\(\s*(.*?)\s*\);'
                matches = re.findall(eval_pattern, response.text, re.S)
                if matches:
                    print(f"   找到 {len(matches)} 个 eval")
                    
                    for j, match in enumerate(matches):
                        with open(f'jsplayer_{i}_eval_{j}.txt', 'w', encoding='utf-8') as f:
                            f.write(match)
                        print(f"   已保存 eval {j}")
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*70)
    print("下载完成！")
    print("="*70)

if __name__ == "__main__":
    download_and_analyze()
