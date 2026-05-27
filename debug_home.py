
# coding=utf-8
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup

url = 'https://www.4kmovie.top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Referer': url,
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'Accept': '*/*'
}

print("Testing homepage: " + url)
print()

try:
    res = requests.get(url, headers=headers, timeout=10)
    print(f"Response status: {res.status_code}")
    print(f"Response headers: {dict(res.headers)}")
    print()
    
    # 保存HTML到文件
    with open('/workspace/homepage.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print("Saved homepage to /workspace/homepage.html")
    print()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    print("=== Testing different selectors: ===")
    
    # 1. 测试原来的选择器
    items1 = soup.select('.module-poster-item')
    print(f"1. .module-poster-item: {len(items1)} 个元素")
    if items1:
        print(f"   First item HTML: {str(items1[0])[:400]}")
    
    print()
    
    # 2. 搜索所有可能的视频项
    print("2. 查找所有 a 标签:")
    all_links = soup.find_all('a', href=re.compile(r'/vod(?:play|detail)/'))
    print(f"   Found {len(all_links)} 个链接指向视频详情页或播放页")
    
    print()
    
    # 3. 保存完整结构
    with open('/workspace/homepage_structure.txt', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Saved pretty-printed homepage to /workspace/homepage_structure.txt")
    
except Exception as e:
    print(f"Error: {e}")
