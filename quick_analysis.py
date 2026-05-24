#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速直链分析 - 尝试找到不需要完整解密的方法
"""
import requests
import re
import json
import base64
import urllib.parse
import time
import random

BASE_URL = "https://www.lmm85.com"
API_URL = "https://yun.92cj.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': BASE_URL,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get(url, headers=None):
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1))
    return requests.get(url, headers=req_headers, timeout=15)

def post(url, data, headers=None):
    req_headers = HEADERS.copy()
    req_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1))
    return requests.post(url, data=data, headers=req_headers, timeout=15)

def analyze_vid():
    """
    分析vid参数，看看能否直接使用
    """
    print("="*70)
    print("分析 vid 参数")
    print("="*70)
    
    # 播放页面的vid
    vid = "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14="
    print(f"\n原始vid: {vid}")
    
    # 尝试base64解码
    print(f"\n尝试Base64解码:")
    try:
        decoded = base64.b64decode(vid)
        print(f"  解码后: {decoded}")
        print(f"  十六进制: {decoded.hex()}")
        print(f"  长度: {len(decoded)} 字节")
        
        # 尝试不同的解码
        print(f"\n尝试修正+号:")
        vid_fixed = vid.replace('+', '-').replace('/', '_')
        print(f"  URL-safe Base64: {vid_fixed}")
        
        decoded_fixed = base64.b64decode(vid_fixed + '==')
        print(f"  解码后: {decoded_fixed}")
        
    except Exception as e:
        print(f"  ❌ 解码失败: {e}")
    
    return vid

def test_direct_post():
    """
    测试直接POST不同的参数组合
    """
    print("\n" + "="*70)
    print("测试不同的POST参数组合")
    print("="*70)
    
    play_path = "/play/5823_1_1.html"
    full_play_url = f"{BASE_URL}{play_path}"
    
    # 1. 获取API页面
    vid = "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14="
    api_page_url = f"{API_URL}/acfun58.php?id={urllib.parse.quote(vid)}&referer={urllib.parse.quote(full_play_url)}"
    
    print(f"\n1️⃣ 获取API页面...")
    response = get(api_page_url, headers={'Referer': full_play_url})
    
    # 提取POST参数
    print(f"\n2️⃣ 提取POST参数...")
    
    post_params = {}
    
    patterns = {
        'vid': r'"vid":\s*"([^"]+)"',
        'type': r'"type":\s*"([^"]+)"',
        'sing': r'"sing":\s*"([^"]+)"',
        'token': r'"token":\s*"([^"]+)"',
        'token1': r'"token1":\s*"([^"]+)"',
        'token2': r'"token2":\s*"([^"]+)"',
        'token3': r'"token3":\s*"([^"]+)"',
        't': r'"t":\s*"([^"]+)"',
        'ti': r'"ti":\s*(\d+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, response.text)
        if match:
            if key == 'ti':
                post_params[key] = match.group(1)
            else:
                post_params[key] = match.group(1).replace(' ', '+')
            print(f"  {key}: {post_params[key]}")
    
    # 3. 尝试不同的POST组合
    print(f"\n3️⃣ 测试不同的POST组合...")
    
    test_combinations = [
        ("完整参数", post_params),
        ("仅token", {'token': post_params.get('token', '')}),
        ("无token", {k: v for k, v in post_params.items() if k != 'token'}),
        ("vid+type", {'vid': post_params.get('vid', ''), 'type': post_params.get('type', '')}),
    ]
    
    for name, params in test_combinations:
        print(f"\n测试: {name}")
        print(f"  参数: {params}")
        
        try:
            resp = post(f"{API_URL}/acfun58.php", params, headers={'Referer': api_page_url})
            print(f"  状态码: {resp.status_code}")
            
            try:
                data = resp.json()
                print(f"  响应: {json.dumps(data, ensure_ascii=False)}")
                
                if data.get('msg') == 200:
                    print(f"\n  🎉 成功!")
                    return data
            except:
                print(f"  响应: {resp.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    return None

def test_different_encrypt():
    """
    测试不同的加密参数
    """
    print("\n" + "="*70)
    print("测试不同的加密参数")
    print("="*70)
    
    # 获取新的播放页面，看看是否需要encrypt参数
    play_path = "/play/5823_1_1.html"
    full_play_url = f"{BASE_URL}{play_path}"
    
    print(f"\n获取播放页面...")
    response = get(full_play_url)
    
    # 查找所有player配置
    players = re.findall(r'player_\w+\s*=\s*(\{[^}]+\})', response.text)
    print(f"找到 {len(players)} 个player配置")
    
    for i, player in enumerate(players):
        print(f"\nPlayer {i+1}:")
        try:
            data = json.loads(player)
            print(f"  encrypt: {data.get('encrypt')}")
            print(f"  url: {data.get('url', '')[:50]}...")
            print(f"  from: {data.get('from')}")
        except:
            print(f"  解析失败: {player[:100]}")

def main():
    print("="*70)
    print("路漫漫动漫 - 快速直链分析")
    print("="*70)
    
    # 1. 分析vid
    vid = analyze_vid()
    
    # 2. 测试不同POST组合
    result = test_direct_post()
    
    # 3. 测试不同加密
    test_different_encrypt()
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
    print("\n结论:")
    print("1. vid参数本身可能是编码的视频ID")
    print("2. POST需要多个参数配合")
    print("3. 核心算法在混淆的JS中")
    print("\n建议:")
    print("- 使用Playwright是当前最可靠的方案")
    print("- 或者继续逆向JS代码")

if __name__ == "__main__":
    main()
