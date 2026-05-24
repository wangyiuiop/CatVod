#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从已保存的HTML直接分析完整算法
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get(url, headers=None):
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1.5))
    return requests.get(url, headers=req_headers, timeout=15)

def analyze_from_saved():
    """
    从已保存的HTML开始完整分析
    """
    print("="*70)
    print("算法分析 - 从已保存数据开始")
    print("="*70)
    
    # 步骤1: 从保存的HTML提取player数据
    print(f"\n📄 1. 从 debug_full_play_page.html 提取 player_data")
    
    with open('debug_full_play_page.html', 'r', encoding='utf-8') as f:
        html1 = f.read()
    
    # 直接提取我们已经找到的那一行
    player_line = re.search(r'player_aaaa=(\{[^\}]+\})', html1)
    if player_line:
        data_str = player_line.group(1)
        player_data = json.loads(data_str)
        print(f"\n✅ 成功提取 player_data:")
        print(f"   {json.dumps(player_data, ensure_ascii=False, indent=4)}")
    else:
        print(f"\n❌ 提取失败")
        return
    
    # 步骤2: 获取player JS
    from_name = player_data.get('from', '')
    player_js_url = f"{BASE_URL}/static/player/{from_name}.js"
    
    print(f"\n📄 2. 获取 Player JS")
    print(f"   URL: {player_js_url}")
    
    play_path = "/play/5823_1_1.html"
    full_play_url = f"{BASE_URL}{play_path}"
    
    response2 = get(player_js_url, headers={'Referer': full_play_url})
    js_content = response2.text
    print(f"   JS 长度: {len(js_content)}")
    
    # 提取API地址
    print(f"\n🔍 3. 从JS提取API地址")
    src_match = re.search(r'\.src\s*=\s*([^;]+?);', js_content)
    if src_match:
        print(f"   .src = {src_match.group(1)}")
    
    # 步骤3: 访问API页面
    vid = player_data.get('url', '')
    api_page_url = f"{API_URL}/acfun58.php?id={urllib.parse.quote(vid)}&referer={urllib.parse.quote(full_play_url)}"
    
    print(f"\n📄 4. 访问 API 页面")
    print(f"   URL: {api_page_url}")
    
    response3 = get(api_page_url, headers={'Referer': full_play_url})
    html3 = response3.text
    
    with open('algorithm_debug.html', 'w', encoding='utf-8') as f:
        f.write(html3)
    print(f"✅ 已保存到 algorithm_debug.html")
    
    # 提取POST参数
    print(f"\n🔍 5. 提取 POST 参数")
    
    post_match = re.search(r'\$\.post\(""\s*,\s*(\{[^{]*(?:\{[^{]*\}[^{]*)*\})\s*,\s*function', html3, re.S)
    
    if post_match:
        post_data_str = post_match.group(1)
        print(f"\n   POST 数据 (原始):")
        print(f"   {post_data_str[:200]}...")
        
        # 提取各个字段
        fields = ['vid', 'type', 'sing', 'token', 'token1', 'token2', 'token3', 't', 'ti']
        post_params = {}
        for field in fields:
            pattern = rf'"{field}":\s*"([^"]+)"'
            match = re.search(pattern, post_data_str)
            if match:
                value = match.group(1)
                if field == 'vid':
                    value = value.replace(' ', '+')
                post_params[field] = value
        
        print(f"\n   提取后:")
        for k, v in post_params.items():
            print(f"   {k}: {v}")
        
        # 步骤4: 发送POST请求
        print(f"\n🚀 6. 发送 POST 请求获取真实地址")
        
        post_headers = HEADERS.copy()
        post_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        post_headers['X-Requested-With'] = 'XMLHttpRequest'
        post_headers['Referer'] = api_page_url
        
        try:
            final_response = requests.post(
                f"{API_URL}/acfun58.php",
                data=post_params,
                headers=post_headers,
                timeout=15
            )
            
            print(f"\n   状态码: {final_response.status_code}")
            print(f"\n   响应内容:")
            
            try:
                result_data = final_response.json()
                print(json.dumps(result_data, ensure_ascii=False, indent=4))
                
                if result_data.get('msg') == 200:
                    video_url = result_data.get('url', '')
                    ext = result_data.get('ext', '')
                    
                    if ext in ['hls', 'hls_list']:
                        video_url = urllib.parse.unquote(video_url)
                    
                    print(f"\n🎉 成功提取真实视频地址!")
                    print(f"   类型: {ext}")
                    print(f"   地址: {video_url}")
                    
                    print(f"\n📦 保存成功信息到 result.txt")
                    with open('result.txt', 'w', encoding='utf-8') as f:
                        f.write("播放参数:\n")
                        f.write(json.dumps(player_data, ensure_ascii=False, indent=4))
                        f.write("\n\nPOST参数:\n")
                        f.write(json.dumps(post_params, ensure_ascii=False, indent=4))
                        f.write("\n\n视频地址:\n")
                        f.write(f"类型: {ext}\n")
                        f.write(f"地址: {video_url}")
                    
                else:
                    print(f"\n❌ 响应错误: {result_data}")
                    
            except Exception as e:
                print(f"   响应: {final_response.text}")
                print(f"   JSON 解析失败: {e}")
                
        except Exception as e:
            print(f"   POST 请求失败: {e}")
    
    print("\n" + "="*70)
    print("分析完成！")
    print("="*70)

if __name__ == "__main__":
    analyze_from_saved()
