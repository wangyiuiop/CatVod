#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决视频只有声音没有画面的问题
通过获取完整的m3u8播放列表并尝试修复
"""
import requests
import re
import json
import time
import random
import urllib.parse
from datetime import datetime

BASE_URL = "https://www.lmm85.com"
API_URL = "https://yun.92cj.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': BASE_URL,
    'Accept': '*/*',
}

def get(url, headers=None):
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.3, 0.8))
    return requests.get(url, headers=req_headers, timeout=15)

def analyze_m3u8(m3u8_url, referer):
    """
    分析m3u8播放列表，找出只有音频的原因
    """
    print("="*70)
    print("分析M3U8播放列表")
    print("="*70)
    
    print(f"\n📄 M3U8地址: {m3u8_url}")
    print(f"🔗 Referer: {referer}")
    
    # 尝试获取m3u8内容
    print(f"\n1️⃣ 获取M3U8文件...")
    try:
        response = get(m3u8_url, headers={'Referer': referer})
        print(f"   状态码: {response.status_code}")
        m3u8_content = response.text
        print(f"   内容长度: {len(m3u8_content)} 字符")
    except Exception as e:
        print(f"   ❌ 获取失败: {e}")
        return None
    
    # 分析m3u8内容
    print(f"\n2️⃣ 分析M3U8内容...")
    
    lines = m3u8_content.split('\n')
    
    # 提取所有.ts片段
    segments = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            segments.append(line)
    
    print(f"   找到 {len(segments)} 个视频片段")
    
    # 分析前几个片段
    if segments:
        print(f"\n3️⃣ 检查视频片段...")
        
        # 获取base URL
        base_url = m3u8_url.rsplit('/', 1)[0] + '/'
        
        # 检查前5个片段的可访问性
        accessible = 0
        inaccessible = 0
        
        for i, segment in enumerate(segments[:10]):
            # 构建完整URL
            if segment.startswith('http'):
                segment_url = segment
            else:
                segment_url = base_url + segment
            
            try:
                response = get(segment_url, headers={'Referer': referer})
                if response.status_code == 200:
                    accessible += 1
                    print(f"   片段{i+1}: ✅ 可访问 ({len(response.content)} 字节)")
                else:
                    inaccessible += 1
                    print(f"   片段{i+1}: ❌ 状态码 {response.status_code}")
            except Exception as e:
                inaccessible += 1
                print(f"   片段{i+1}: ❌ {e}")
        
        print(f"\n统计:")
        print(f"   可访问: {accessible}/10")
        print(f"   不可访问: {inaccessible}/10")
        
        # 保存m3u8内容
        with open('debug_m3u8.m3u8', 'w', encoding='utf-8') as f:
            f.write(m3u8_content)
        print(f"\n📝 已保存M3U8到 debug_m3u8.m3u8")
        
        return {
            'm3u8_url': m3u8_url,
            'segments': segments,
            'accessible': accessible,
            'inaccessible': inaccessible
        }
    
    return None

def get_video_directly():
    """
    直接尝试获取完整的视频地址
    """
    print("\n" + "="*70)
    print("直接获取视频地址")
    print("="*70)
    
    # 1. 获取播放页面
    play_path = "/play/5823_1_1.html"
    full_play_url = f"{BASE_URL}{play_path}"
    
    print(f"\n1️⃣ 获取播放页面...")
    response = get(full_play_url, headers={'Referer': BASE_URL})
    html = response.text
    
    # 提取player数据
    player_match = re.search(r'player_\w+\s*=\s*(\{[^}]+\})', html)
    if not player_match:
        print("❌ 无法提取player数据")
        return
    
    player_data = json.loads(player_match.group(1))
    print(f"   ✅ 提取到player数据")
    print(f"   url: {player_data.get('url', '')[:50]}...")
    print(f"   from: {player_data.get('from')}")
    
    # 2. 获取API页面
    vid = player_data.get('url', '')
    api_page_url = f"{API_URL}/acfun58.php?id={urllib.parse.quote(vid)}&referer={urllib.parse.quote(full_play_url)}"
    
    print(f"\n2️⃣ 访问API页面...")
    api_response = get(api_page_url, headers={'Referer': full_play_url})
    api_html = api_response.text
    
    # 3. 提取POST参数
    print(f"\n3️⃣ 提取POST参数...")
    
    post_params = {}
    patterns = [
        ('vid', r'"vid":\s*"([^"]+)"'),
        ('type', r'"type":\s*"([^"]+)"'),
        ('sing', r'"sing":\s*"([^"]+)"'),
        ('token', r'"token":\s*"([^"]+)"'),
        ('t', r'"t":\s*"([^"]+)"'),
        ('ti', r'"ti":\s*(\d+)'),
    ]
    
    for key, pattern in patterns:
        match = re.search(pattern, api_html)
        if match:
            if key == 'ti':
                post_params[key] = match.group(1)
            else:
                post_params[key] = match.group(1).replace(' ', '+')
    
    print(f"   提取到 {len(post_params)} 个参数")
    
    # 4. 发送POST请求
    print(f"\n4️⃣ 发送POST请求...")
    
    try:
        post_response = requests.post(
            f"{API_URL}/acfun58.php",
            data=post_params,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': api_page_url,
                'User-Agent': HEADERS['User-Agent'],
                'X-Requested-With': 'XMLHttpRequest'
            },
            timeout=15
        )
        
        print(f"   状态码: {post_response.status_code}")
        
        try:
            result = post_response.json()
            print(f"\n5️⃣ 解析响应...")
            print(f"   msg: {result.get('msg')}")
            print(f"   ext: {result.get('ext')}")
            print(f"   url: {result.get('url', '')[:100]}...")
            
            if result.get('msg') == 200:
                video_url = result.get('url', '')
                ext = result.get('ext', '')
                
                # 解码URL
                if ext in ['hls', 'hls_list']:
                    video_url = urllib.parse.unquote(video_url)
                
                print(f"\n🎉 成功获取视频地址!")
                print(f"   类型: {ext}")
                print(f"   地址: {video_url}")
                
                # 分析m3u8
                if '.m3u8' in video_url:
                    analyze_m3u8(video_url, api_page_url)
                
                return result
            else:
                print(f"\n❌ 获取失败: {result}")
                
        except Exception as e:
            print(f"   ❌ JSON解析失败: {e}")
            print(f"   响应: {post_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ POST请求失败: {e}")

def create_player_config():
    """
    创建播放器配置，解决Referer问题
    """
    print("\n" + "="*70)
    print("播放器配置建议")
    print("="*70)
    
    print(f"""
🎯 针对"只有声音没有画面"的问题，解决方案：

1️⃣ 使用VLC播放器
   - VLC可以自定义Referer
   - 设置方法：
     * 媒体 → 打开网络串流
     * 输入URL后，点击"播放选项"
     * 添加: :http-referrer={BASE_URL}

2️⃣ 使用PotPlayer
   - 右键 → 打开 → 打开链接
   - 在弹出窗口中设置Referer

3️⃣ 使用ffplay播放
   ffmpeg -i "m3u8_url" -fflags nobuffer -i "m3u8_url" -http_host p3-dcd-sign.byteimg.com -headers "Referer: {BASE_URL}/" output.mp4

4️⃣ 下载后播放
   ffmpeg -i "m3u8_url" -headers "Referer: {BASE_URL}/" output.mp4

5️⃣ 使用浏览器开发者工具
   - F12 → Network
   - 找到m3u8文件，右键 → Copy → Copy link address
   - 在新标签页打开，浏览器会自动处理Referer
""")

def main():
    print("="*70)
    print("解决视频只有声音没有画面的问题")
    print("="*70)
    
    # 直接获取视频地址
    result = get_video_directly()
    
    # 创建播放器配置建议
    create_player_config()
    
    print("\n" + "="*70)
    print("完成")
    print("="*70)

if __name__ == "__main__":
    main()
