#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度测试 - 访问真实API获取播放地址
"""
import requests
import re
import json
import base64
import urllib.parse
import time
import random

BASE_URL = "https://www.lmm85.com"
API_URL_TEMPLATE = "https://yun.92cj.com/acfun58.php?id={}&referer={}"

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
    time.sleep(random.uniform(1, 2))
    return requests.get(url, headers=req_headers, timeout=15, allow_redirects=True)

def test_api_access():
    """测试API访问"""
    print("="*70)
    print("路漫漫动漫 - 真实API访问测试")
    print("="*70)
    
    # 从之前的测试中获取的信息
    play_url = "/play/5823_1_1.html"
    api_id = "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14=&t=DU"
    referer = f"{BASE_URL}{play_url}"
    
    print(f"\n🎬 播放页面: {referer}")
    print(f"🔑 API ID: {api_id}")
    
    # 构建API URL
    api_url = API_URL_TEMPLATE.format(
        urllib.parse.quote(api_id),
        urllib.parse.quote(referer)
    )
    print(f"\n🌐 API地址: {api_url}")
    
    # 访问API
    print("\n📡 正在访问API...")
    try:
        response = get(api_url, headers={
            'Referer': referer,
            'Accept': '*/*',
        })
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', '')}")
        
        # 保存响应
        with open('debug_api_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("已保存到: debug_api_response.html")
        
        # 分析响应
        print(f"\n📊 响应长度: {len(response.text)} 字符")
        print(f"\n📝 响应内容预览:")
        print(response.text[:500])
        
        # 尝试提取视频地址
        print(f"\n🔍 尝试提取视频地址...")
        
        # 查找video标签
        video_matches = re.findall(r'<video[^>]*src=["\']([^"\']+)["\']', response.text, re.I)
        if video_matches:
            print(f"\n✅ 找到 video src:")
            for match in video_matches:
                print(f"   {match}")
        
        # 查找iframe
        iframe_matches = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', response.text, re.I)
        if iframe_matches:
            print(f"\n✅ 找到 iframe src:")
            for match in iframe_matches:
                print(f"   {match}")
        
        # 查找m3u8地址
        m3u8_matches = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
        if m3u8_matches:
            print(f"\n✅ 找到 m3u8 地址:")
            for match in m3u8_matches:
                print(f"   {match}")
        
        # 查找JSON
        try:
            json_data = json.loads(response.text)
            print(f"\n✅ 响应为JSON:")
            print(json.dumps(json_data, ensure_ascii=False, indent=2))
        except:
            pass
        
        # 查找script中的URL
        script_urls = re.findall(r'(https?://[^\s"\'<>]+)', response.text)
        if script_urls:
            print(f"\n📋 找到 {len(script_urls)} 个可能的URL")
            for i, url in enumerate(script_urls[:5]):
                print(f"  {i+1}. {url}")
                
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        print(f"堆栈: {traceback.format_exc()}")
    
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)

if __name__ == "__main__":
    test_api_access()
