#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法分析：完整流程测试
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

def analyze_algorithm():
    """
    完整流程分析
    """
    print("="*70)
    print("算法分析 - 完整流程")
    print("="*70)
    
    # 步骤1: 获取播放页面
    play_path = "/play/5823_1_1.html"
    full_play_url = f"{BASE_URL}{play_path}"
    
    print(f"\n📄 1. 获取播放页面")
    print(f"   URL: {full_play_url}")
    
    response1 = get(full_play_url, headers={'Referer': BASE_URL})
    html1 = response1.text
    
    # 提取player数据
    player_data = None
    
    # 更全面的提取方式
    # 首先找到<script>标签里的内容
    script_pattern = r'<script[^>]*>([\s\S]*?)</script>'
    scripts = re.findall(script_pattern, html1)
    
    print(f"\n找到 {len(scripts)} 个script标签")
    
    for i, script in enumerate(scripts):
        if 'player_' in script:
            print(f"\nScript {i} 包含 player_")
            
            # 在这个script里找 - 更宽松的模式
            player_patterns = [
                r'player_[\w]+\s*=\s*(\{[\s\S]*?\});?\s*<',
                r'player_[\w]+\s*=\s*(\{[\s\S]*?\});?',
                r'var\s+player_[\w]+\s*=\s*(\{[\s\S]*?\});?',
            ]
            
            for pattern in player_patterns:
                for match in re.finditer(pattern, script):
                    try:
                        data_str = match.group(1)
                        print(f"\n   找到可能的数据: {data_str[:100]}...")
                        
                        # 先简单清理一下，移除可能的注释
                        data_str = re.sub(r'//.*$', '', data_str, flags=re.MULTILINE)
                        data_str = data_str.strip()
                        
                        player_data = json.loads(data_str)
                        print(f"\n✅ 成功提取 player_data:")
                        print(f"   {json.dumps(player_data, ensure_ascii=False, indent=4)}")
                        break
                    except Exception as e:
                        # 如果失败，保存看看
                        print(f"   解析失败: {e}")
                        with open(f'debug_player_data_{i}.txt', 'w', encoding='utf-8') as f:
                            f.write(data_str)
                        print(f"   已保存到 debug_player_data_{i}.txt")
                if player_data:
                    break
        if player_data:
            break
    
    if not player_data:
        print(f"\n❌ 无法提取 player_data")
        # 保存整个HTML用于分析
        with open('debug_full_play_page.html', 'w', encoding='utf-8') as f:
            f.write(html1)
        print(f"   已保存完整页面到 debug_full_play_page.html")
        return
    
    # 步骤2: 获取player JS
    from_name = player_data.get('from', '')
    player_js_url = f"{BASE_URL}/static/player/{from_name}.js"
    
    print(f"\n📄 2. 获取 Player JS")
    print(f"   URL: {player_js_url}")
    
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
    
    # 保存用于分析
    with open('algorithm_debug.html', 'w', encoding='utf-8') as f:
        f.write(html3)
    print(f"✅ 已保存到 algorithm_debug.html")
    
    # 提取POST参数
    print(f"\n🔍 5. 提取 POST 参数")
    
    post_match = re.search(r'\$\.post\(""\s*,\s*(\{[^{]*(?:\{[^{]*\}[^{]*)*\})\s*,\s*function', html3, re.S)
    
    if post_match:
        post_data_str = post_match.group(1)
        print(f"\n   POST 数据 (原始):")
        print(f"   {post_data_str}")
        
        # 提取各个字段
        fields = ['vid', 'type', 'sing', 'token', 'token1', 'token2', 'token3', 't', 'ti']
        post_params = {}
        for field in fields:
            pattern = rf'"{field}":\s*"([^"]+)"'
            match = re.search(pattern, post_data_str)
            if match:
                value = match.group(1)
                # 修复空格变+的问题
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
    analyze_algorithm()
