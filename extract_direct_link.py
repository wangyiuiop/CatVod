#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright拦截版 - 静默获取直链
"""
import sys
import time
import random

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 请先安装Playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

BASE_URL = "https://www.lmm85.com"

def extract_direct_link(play_path):
    """
    使用Playwright静默提取真实视频直链
    """
    full_url = f"{BASE_URL}{play_path}"
    video_urls = []
    
    with sync_playwright() as p:
        print(f"\n🎬 正在提取直链...")
        print(f"📄 播放页面: {full_url}")
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            extra_http_headers={'Referer': BASE_URL}
        )
        
        page = context.new_page()
        
        # 监听所有网络响应
        def handle_response(response):
            url = response.url
            # 查找视频相关响应
            if any(ext in url.lower() for ext in ['.m3u8', '.mp4', '.flv', '.ts']):
                print(f"\n🎥 捕获视频地址:")
                print(f"   {url}")
                if url not in video_urls:
                    video_urls.append(url)
        
        page.on('response', handle_response)
        
        # 访问播放页面
        try:
            page.goto(full_url, wait_until='networkidle', timeout=30000)
        except:
            pass
        
        # 等待视频加载
        print(f"\n⏳ 等待视频加载 (20秒)...")
        time.sleep(20)
        
        browser.close()
    
    return video_urls

def main():
    print("="*70)
    print("路漫漫动漫 - 直链提取工具")
    print("="*70)
    
    # 测试视频
    test_path = "/play/5823_1_1.html"
    
    # 提取
    urls = extract_direct_link(test_path)
    
    print(f"\n" + "="*70)
    print("🎥 提取结果")
    print("="*70)
    
    if urls:
        print(f"\n✅ 成功提取 {len(urls)} 个视频直链:\n")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
    else:
        print(f"\n❌ 未捕获到视频直链")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
