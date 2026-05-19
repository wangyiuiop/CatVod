#!/usr/bin/env python3
"""
分析 4kvm.tv 的完整网站结构
获取API
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import base64

BASE_URL = "https://www.4kvm.tv"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})

def get_page(url):
    print(f"[+] 访问: {url}")
    res = session.get(url)
    res.raise_for_status()
    return res.text

def analyze_homepage():
    """分析主页结构"""
    print("\n" + "="*60)
    print("分析主页")
    print("="*60)
    html = get_page(BASE_URL)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找导航菜单
    print("\n[*] 导航菜单:")
    nav_links = soup.select('nav a')
    for link in nav_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        if href and text and href.startswith('/'):
            print(f"  - {text}: {BASE_URL}{href}")
    
    # 查找分类
    print("\n[*] 可能的分类页:")
    for link in nav_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        if any(x in href.lower() for x in ['movie', 'tv', 'anime', 'movie']):
            print(f"  {text}: {BASE_URL}{href}")
    
    # 查找热门推荐
    print("\n[*] 热门推荐内容:")
    cards = soup.select('a[href*="/play/"]')
    a_set = set()
    for a in cards[:20]:
        href = a.get('href', '')
        if '/play/' in href and href not in a_set:
            a_set.add(href)
            print(f"  {href}")
    
    return html

def analyze_category(url):
    """分析分类页"""
    print("\n" + "="*60)
    print(f"分析分类页: {url}")
    print("="*60)
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找内容卡片
    print("\n[*] 分类内容:")
    cards = soup.select('a[href*="/play/"]')
    print(f"  找到 {len(cards)} 个播放链接")
    
    # 搜索功能
    print("\n[*] 搜索功能:")
    search_form = soup.select('form[action*="/search"]')
    print(f"  搜索表单: {'找到!' if search_form else '未找到'}")

def main():
    # 分析主页
    analyze_homepage()
    
    # 分析几个分类页
    analyze_category(f"{BASE_URL}/movie")
    analyze_category(f"{BASE_URL}/tv")
    
    print("\n" + "="*60)
    print("完成分析")
    print("="*60)

if __name__ == "__main__":
    main()
