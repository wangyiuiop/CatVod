#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析这个视频链接为什么不能播放
"""
import requests
import time
from datetime import datetime

video_url = "https://p3-dcd-sign.byteimg.com/tos-cn-i-f042mdwyw7/c9fb29b4bbfd477e8b5a7958fe31bd68~tplv-jxcbcipi3j-image.image?lk3s=13ddc783&x-expires=1779624700&x-signature=drqMunj14aUGjGzHjFqg2KYGVx8%3D"

print("="*70)
print("分析视频链接问题")
print("="*70)

# 1. 分析链接结构
print(f"\n1️⃣ 链接分析:")
print(f"   完整链接: {video_url}")

# 2. 检查过期时间
print(f"\n2️⃣ 检查过期时间:")
expires = 1779624700
current = int(time.time())

expire_time = datetime.fromtimestamp(expires)
current_time = datetime.fromtimestamp(current)

print(f"   过期时间: {expire_time}")
print(f"   当前时间: {current_time}")

if expires < current:
    print(f"   ❌ 链接已过期!")
else:
    print(f"   ✅ 链接未过期")

# 3. 检查域名
print(f"\n3️⃣ 分析域名:")
print(f"   域名: p3-dcd-sign.byteimg.com")
print(f"   这是抖音/西瓜视频的CDN!")

# 4. 尝试访问
print(f"\n4️⃣ 尝试访问链接:")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.lmm85.com/',
}

try:
    response = requests.head(video_url, headers=headers, timeout=10)
    print(f"   状态码: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', '')}")
    print(f"   Content-Length: {response.headers.get('Content-Length', '')}")
    
    if response.status_code == 200:
        print(f"\n   ✅ 链接有效! 但可能需要正确的Referer或其他条件")
    elif response.status_code == 403:
        print(f"\n   ❌ 403 Forbidden - 权限不足，可能:")
        print(f"      1. 链接已过期")
        print(f"      2. Referer不匹配")
        print(f"      3. 签名失效")
        
    # 检查Content-Type
    ct = response.headers.get('Content-Type', '')
    if 'image' in ct:
        print(f"\n   ⚠️ 这个URL返回的是图片! 不是视频!")
    
except Exception as e:
    print(f"   ❌ 访问失败: {e}")

# 5. 检查文件名
print(f"\n5️⃣ 检查文件名:")
print(f"   文件名: c9fb29b4bbfd477e8b5a7958fe31bd68~tplv-jxcbcipi3j-image.image")
print(f"   后缀是 .image 不是视频格式 (mp4/m3u8/flv等)")

print(f"\n" + "="*70)
print("总结问题")
print("="*70)

print(f"\n问题1: 链接格式不正确")
print(f"   - 这个URL看起来是图片URL，不是视频URL")
print(f"   - 后缀是 .image 不是视频格式")

print(f"\n问题2: 临时签名链接")
print(f"   - x-expires 和 x-signature 说明这是临时链接")
print(f"   - 有效期很短，很快会过期")

print(f"\n问题3: 来源是抖音/西瓜视频CDN")
print(f"   - 这个CDN有防盗链机制")
print(f"   - 需要正确的Referer和Cookie")

print(f"\n" + "="*70)
print("建议")
print("="*70)
print(f"\n1. 重新获取播放页面，拿到新的链接")
print(f"2. 检查是否有m3u8格式的链接")
print(f"3. 确保Referer正确")
print(f"4. 可能需要模拟完整的浏览器环境")
