#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Playwright提取真实视频直链
"""
import sys
import json
import time
import random
from urllib.parse import urljoin, quote

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 请先安装Playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

BASE_URL = "https://www.lmm85.com"

def extract_direct_url(play_url):
    """
    使用Playwright提取真实视频直链
    """
    print(f"\n🎬 开始提取直链...")
    print(f"📄 播放页面: {play_url}")
    
    video_urls = []
    all_requests = []
    
    with sync_playwright() as p:
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(headless=False)  # 设为False可以看到浏览器操作
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                'Referer': BASE_URL,
            }
        )
        
        page = context.new_page()
        
        # 监听所有网络请求，拦截视频请求
        def handle_request(request):
            url = request.url
            all_requests.append(url)
            
            # 查找视频相关的请求
            if any(ext in url.lower() for ext in ['.m3u8', '.mp4', '.flv', '.ts']):
                print(f"\n🎥 发现视频请求:")
                print(f"   {url}")
                if url not in video_urls:
                    video_urls.append(url)
        
        page.on('request', handle_request)
        
        # 1. 访问播放页面
        print(f"\n📄 访问播放页面...")
        try:
            page.goto(play_url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            print(f"⚠️ 页面加载超时，继续执行: {e}")
        
        # 2. 等待一段时间，让iframe和视频加载
        print(f"\n⏳ 等待视频加载 (15秒)...")
        
        # 打印页面内容，查找iframe
        try:
            iframe = page.frame_locator('iframe').first
            if iframe:
                print(f"\n📌 找到iframe")
        except:
            pass
        
        # 滚动页面，触发视频加载
        try:
            page.mouse.wheel(0, 500)
        except:
            pass
        
        # 等待
        time.sleep(15)
        
        # 3. 获取页面的所有src属性
        print(f"\n🔍 查找所有视频相关元素...")
        
        # 查找video标签
        videos = page.query_selector_all('video')
        if videos:
            print(f"\n📹 找到 {len(videos)} 个video标签")
            for i, video in enumerate(videos):
                src = video.get_attribute('src')
                if src:
                    print(f"\n  视频{i+1} src: {src}")
                    if src not in video_urls:
                        video_urls.append(src)
        
        # 查找iframe
        iframes = page.query_selector_all('iframe')
        if iframes:
            print(f"\n📌 找到 {len(iframes)} 个iframe")
            for i, iframe in enumerate(iframes):
                src = iframe.get_attribute('src')
                if src:
                    print(f"\n  iframe{i+1} src: {src}")
                    if any(ext in src.lower() for ext in ['.m3u8', '.mp4']):
                        if src not in video_urls:
                            video_urls.append(src)
        
        print(f"\n\n" + "="*70)
        
        # 保存所有请求用于分析
        with open('debug_all_requests.txt', 'w', encoding='utf-8') as f:
            for url in all_requests:
                f.write(f"{url}\n")
        print(f"✅ 已保存 {len(all_requests)} 个请求到 debug_all_requests.txt")
        
        browser.close()
    
    return video_urls

def main():
    print("="*70)
    print("路漫漫动漫 - 直链提取工具")
    print("="*70)
    
    # 测试视频
    play_path = "/play/5823_1_1.html"
    full_url = f"{BASE_URL}{play_path}"
    
    # 提取直链
    video_urls = extract_direct_url(full_url)
    
    print(f"\n" + "="*70)
    print("🎥 提取结果")
    print("="*70)
    
    if video_urls:
        print(f"\n✅ 找到 {len(video_urls)} 个视频地址:\n")
        for i, url in enumerate(video_urls, 1):
            print(f"  {i}. {url}")
    else:
        print(f"\n❌ 未找到视频地址")
        print(f"\n💡 建议:")
        print(f"  1. 增加等待时间")
        print(f"  2. 尝试不同的视频")
        print(f"  3. 查看 debug_all_requests.txt 分析")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
