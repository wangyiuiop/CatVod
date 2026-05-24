#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实视频地址获取器 - 使用Playwright捕获网络请求
"""
import sys
import time
import json
import urllib.parse
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 需要安装Playwright")
    print("安装命令:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

BASE_URL = "https://www.lmm85.com"

def get_real_video_url(play_path):
    """
    获取真实的视频地址
    """
    print("="*70)
    print("获取真实视频地址")
    print("="*70)
    
    full_play_url = f"{BASE_URL}{play_path}"
    print(f"\n播放页面: {full_play_url}")
    
    video_urls = []
    all_requests = []
    
    with sync_playwright() as p:
        print("\n🚀 启动浏览器...")
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={'Referer': BASE_URL}
        )
        page = context.new_page()
        
        # 监听所有网络响应
        def handle_response(response):
            url = response.url
            status = response.status
            all_requests.append({
                'url': url,
                'status': status,
                'content_type': response.headers.get('Content-Type', '')
            })
            
            # 检查是否是视频资源
            is_video = any(ext in url.lower() for ext in [
                '.mp4', '.m3u8', '.flv', '.ts', '.webm', '.avi'
            ])
            
            content_type = response.headers.get('Content-Type', '').lower()
            is_video_content = any(v in content_type for v in [
                'video/', 'application/vnd.apple.mpegurl', 'application/x-mpegurl'
            ])
            
            if is_video or is_video_content:
                if 200 <= status < 300:
                    print(f"\n🎥 捕获视频: {url}")
                    if url not in video_urls:
                        video_urls.append(url)
        
        # 监听API响应，尝试找到JSON格式的视频信息
        def handle_api_response(response):
            if '/acfun58.php' in response.url and response.request.method == 'POST':
                print(f"\n📡 捕获API响应: {response.url}")
                try:
                    data = response.json()
                    print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=4)}")
                    
                    if data.get('msg') == 200 and 'url' in data:
                        url = data.get('url')
                        ext = data.get('ext')
                        
                        if ext in ['hls', 'hls_list']:
                            try:
                                url = urllib.parse.unquote(url)
                            except:
                                pass
                        
                        print(f"\n🎉 找到真实视频地址:")
                        print(f"  地址: {url}")
                        print(f"  类型: {ext}")
                        
                        if url not in video_urls:
                            video_urls.insert(0, url)
                            
                except Exception as e:
                    try:
                        print(f"  响应文本: {response.text()[:200]}")
                    except:
                        print(f"  无法解析API响应: {e}")
        
        page.on("response", handle_response)
        page.on("response", handle_api_response)
        
        print("\n📄 访问播放页面...")
        try:
            page.goto(full_play_url, wait_until="networkidle", timeout=30000)
        except:
            print("  ⚠️ 页面加载超时，继续等待...")
        
        print("\n⏳ 等待15秒让视频加载...")
        
        # 滚动页面，触发加载
        try:
            page.mouse.wheel(0, 1000)
            time.sleep(2)
            page.mouse.wheel(0, -1000)
        except:
            pass
        
        time.sleep(15)
        
        # 保存所有请求
        with open('debug_requests.json', 'w', encoding='utf-8') as f:
            json.dump(all_requests, f, ensure_ascii=False, indent=4)
        print(f"\n📝 已保存 {len(all_requests)} 个请求到 debug_requests.json")
        
        browser.close()
    
    print("\n" + "="*70)
    print("结果")
    print("="*70)
    
    if video_urls:
        print(f"\n✅ 找到 {len(video_urls)} 个视频地址:")
        for i, url in enumerate(video_urls):
            print(f"\n{i+1}. {url}")
        
        # 保存到文件
        with open('video_urls.txt', 'w', encoding='utf-8') as f:
            for url in video_urls:
                f.write(f"{url}\n")
        print(f"\n📝 已保存到 video_urls.txt")
        
        # 返回第一个视频地址
        return video_urls[0]
    else:
        print(f"\n❌ 未找到视频地址")
        print(f"\n💡 建议:")
        print(f"  1. 查看 debug_requests.json")
        print(f"  2. 尝试 headless=False 看看页面")
        print(f"  3. 手动在浏览器检查网络请求")
        return None

def main():
    print("="*70)
    print("路漫漫动漫 - 真实视频地址获取器")
    print("="*70)
    
    # 测试视频
    play_path = "/play/5823_1_1.html"
    
    # 获取真实地址
    video_url = get_real_video_url(play_path)
    
    if video_url:
        print(f"\n" + "="*70)
        print("测试视频播放")
        print("="*70)
        print(f"\n真实地址: {video_url}")
        
        print(f"\n📋 播放建议:")
        print(f"  1. 直接在浏览器打开链接")
        print(f"  2. 使用VLC/PotPlayer播放")
        print(f"  3. 确保播放时加上 Referer: {BASE_URL}/")
        
        if '.m3u8' in video_url:
            print(f"  4. 这是HLS流媒体，支持m3u8的播放器才能播放")

if __name__ == "__main__":
    main()
