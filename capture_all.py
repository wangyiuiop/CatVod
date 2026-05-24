#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright捕获完整网络请求
"""
import sys
import time
import json

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 需要安装 Playwright")
    sys.exit(1)

BASE_URL = "https://www.lmm85.com"

def capture_all():
    """
    用 Playwright 访问并捕获所有网络请求
    """
    print("="*70)
    print("捕获完整网络请求")
    print("="*70)
    
    with sync_playwright() as p:
        print(f"\n🚀 启动浏览器...")
        
        browser = p.chromium.launch(headless=False)  # 可以看看
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        all_requests = []
        all_responses = []
        
        def handle_request(request):
            all_requests.append(
                {'url': request.url, 'method': request.method, 'resource_type': request.resource_type}
            )
        
        def handle_response(response):
            try:
                content_type = response.headers.get('content-type', '')
                is_video = any(t in content_type for t in ['video', 'mpegurl', 'octet-stream'])
                is_json = 'json' in content_type
                body = ""
                
                if is_json:
                    try:
                        body = response.json()
                    except:
                        try:
                            body = response.text()
                        except:
                            pass
                
                all_responses.append({
                    'url': response.url, 'status': response.status, 'content_type': content_type,
                    'is_video': is_video, 'is_json': is_json, 'body': body
                })
                
                if is_json and response.request.method == "POST":
                    print(f"\n✨ 发现POST响应: {response.url}")
                    print(f"   {json.dumps(body, ensure_ascii=False, indent=4)}")
                
                if is_video:
                    print(f"\n🎥 发现视频请求: {response.url}")
                    
            except:
                pass
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        play_url = f"{BASE_URL}/play/5823_1_1.html"
        print(f"\n📄 访问: {play_url}")
        
        page.goto(play_url)
        
        print(f"\n⏳ 等待30秒加载...")
        time.sleep(30)
        
        print(f"\n💾 保存请求信息...")
        
        with open("capture_requests.json", "w", encoding="utf-8") as f:
            json.dump(all_requests, f, ensure_ascii=False, indent=4)
        
        with open("capture_responses.json", "w", encoding="utf-8") as f:
            json.dump(all_responses, f, ensure_ascii=False, indent=4)
        
        print(f"✅ 已保存到 capture_requests.json 和 capture_responses.json")
        
        print(f"\n统计:")
        print(f"   总请求数: {len(all_requests)}")
        print(f"   总响应数: {len(all_responses)}")
        
        video_count = sum(1 for r in all_responses if r.get('is_video'))
        print(f"   视频请求: {video_count}")
        
        post_count = sum(1 for r in all_responses if r.get('is_json') and '/acfun58.php' in r.get('url'))
        print(f"   关键POST: {post_count}")
        
        browser.close()
    
    print("\n" + "="*70)
    print("完成！")
    print("="*70)

if __name__ == "__main__":
    capture_all()
