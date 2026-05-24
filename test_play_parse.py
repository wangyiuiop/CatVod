#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 路漫漫动漫播放解析测试
"""
import requests
import re
import json
import base64
import urllib.parse
import time
import random

BASE_URL = "https://www.lmm85.com"

# 模拟浏览器请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': BASE_URL,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get(url, headers=None):
    """发送GET请求"""
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(0.5, 1.5))
    return requests.get(url, headers=req_headers, timeout=15)

def search(keyword):
    """搜索视频"""
    print(f"\n🔍 搜索: {keyword}")
    url = f"{BASE_URL}/vod/search/page/1/wd/{urllib.parse.quote(keyword)}.html"
    response = get(url)
    
    print(f"状态码: {response.status_code}")
    
    results = []
    pattern = r'<div class="video-img-box.*?>(.*?)<h6 class="title">(.*?)</h6>'
    matches = re.findall(pattern, response.text, re.S)
    
    for c, t in matches:
        try:
            vid_match = re.search(r'href="/detail/(\d+).html"', c)
            if not vid_match:
                continue
            vid = vid_match.group(1)
            title_match = re.search(r'<a.*?>(.*?)</a>', t)
            title = title_match.group(1) if title_match else ""
            img_match = re.search(r'data-src="(.*?)"', c) or re.search(r'src="(.*?)"', c)
            img = img_match.group(1) if img_match else ""
            rem_match = re.search(r'class="label">(.*?)</span>', c)
            rem = rem_match.group(1) if rem_match else ""
            
            results.append({
                'id': vid,
                'title': title,
                'img': img,
                'remark': rem
            })
        except Exception as e:
            print(f"解析错误: {e}")
    
    print(f"找到 {len(results)} 个结果")
    return results

def get_detail(vid):
    """获取详情页信息"""
    print(f"\n📄 获取详情页: vid={vid}")
    url = f"{BASE_URL}/detail/{vid}.html"
    response = get(url)
    print(f"状态码: {response.status_code}")
    
    # 提取播放链接
    play_urls = []
    for b in response.text.split('class="module-list')[1:]:
        if 'module-blocklist' not in b:
            continue
        es = re.findall(r'<a href="(/play/.*?.html)".*?<span>(.*?)</span>', b)
        for u, n in es:
            play_urls.append({
                'name': n,
                'url': u
            })
    
    print(f"找到 {len(play_urls)} 个播放链接")
    return play_urls, response.text

def get_play_page(play_url):
    """获取播放页信息"""
    print(f"\n🎬 访问播放页: {play_url}")
    url = f"{BASE_URL}{play_url}" if play_url.startswith('/') else play_url
    response = get(url, headers={'Referer': f"{BASE_URL}/"})
    print(f"状态码: {response.status_code}")
    return response.text

def extract_player_data(html):
    """提取player数据"""
    print("\n🔎 提取player数据...")
    
    patterns = [
        r'var\s+player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
        r'player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
        r'<script[^>]*>\s*var\s+player[^=]*=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;?\s*<\/script>',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.S)
        if matches:
            print(f"找到 {len(matches)} 个匹配")
            for i, data_str in enumerate(matches):
                try:
                    data = json.loads(data_str)
                    print(f"\n✅ Player数据{i+1}:")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSON解析失败{i+1}: {e}")
    
    # 保存HTML用于调试
    with open('debug_play_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\n⚠️ 未找到player数据，已保存到debug_play_page.html")
    
    return None

def test_play_parse(vid="5823"):
    """测试播放解析"""
    print("="*70)
    print("路漫漫动漫 - 播放解析测试")
    print("="*70)
    
    # 1. 搜索"斗罗大陆"
    search_results = search("斗罗大陆")
    
    if not search_results:
        print("\n搜索失败，使用默认视频ID")
    else:
        vid = search_results[0]['id']
        print(f"\n选择视频: {search_results[0]['title']} ({vid})")
    
    # 2. 获取详情页
    play_urls, _ = get_detail(vid)
    
    if not play_urls:
        print("\n未找到播放链接")
        return
    
    # 3. 访问第一个播放页面
    first_play_url = play_urls[0]['url']
    html = get_play_page(first_play_url)
    
    # 4. 提取player数据
    player_data = extract_player_data(html)
    
    if not player_data:
        return
    
    # 5. 分析数据
    url = player_data.get('url', '')
    from_name = player_data.get('from', '')
    encrypt = player_data.get('encrypt', 0)
    
    print(f"\n📊 分析结果:")
    print(f"  URL: {url}")
    print(f"  from: {from_name}")
    print(f"  encrypt: {encrypt}")
    
    # 6. 尝试解密/解码
    decrypted_url = url
    if encrypt == 1:
        decrypted_url = urllib.parse.unquote(url)
        print(f"  unescape解码: {decrypted_url}")
    elif encrypt == 2:
        try:
            decoded = base64.b64decode(url).decode('utf-8')
            decrypted_url = urllib.parse.unquote(decoded)
            print(f"  base64+unescape解码: {decrypted_url}")
        except Exception as e:
            print(f"  base64解码失败: {e}")
    
    # 7. 判断是否为直接视频
    is_direct = any(ext in decrypted_url.lower() for ext in ['.mp4', '.m3u8', '.flv', '.ts', '.mkv'])
    print(f"\n🎥 是否为直接视频: {'✅' if is_direct else '❌'}")
    
    if is_direct:
        print(f"\n✅ 成功获取真实播放地址:")
        print(f"   {decrypted_url}")
    else:
        print(f"\n⚠️ 需要进一步解析，尝试获取player JS...")
        
        # 获取player JS
        if from_name:
            player_js_url = f"{BASE_URL}/static/player/{from_name}.js"
            print(f"\n📄 获取player JS: {player_js_url}")
            try:
                response = get(player_js_url, headers={'Referer': f"{BASE_URL}{first_play_url}"})
                print(f"状态码: {response.status_code}")
                
                # 保存JS用于分析
                with open(f'debug_player_{from_name}.js', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"已保存到: debug_player_{from_name}.js")
                
                # 简单分析JS
                if '.src' in response.text:
                    src_matches = re.findall(r'\.src\s*=\s*([^;]+?);', response.text)
                    print(f"\n🔗 找到 {len(src_matches)} 个 .src")
                    for i, match in enumerate(src_matches[:3]):
                        print(f"{i+1}. {match}")
                
            except Exception as e:
                print(f"获取JS失败: {e}")
    
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)

if __name__ == "__main__":
    test_play_parse()
