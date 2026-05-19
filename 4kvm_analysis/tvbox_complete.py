#!/usr/bin/env python3
"""
TVBox 源 - 4kvm.tv (完整版本)
包含 Playwright 自动化获取真实播放地址
"""

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import json
import base64
import time
import urllib.parse
import threading
from queue import Queue

app = Flask(__name__)

BASE_URL = "https://www.4kvm.tv"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
})

# 全局 Playwright 浏览器实例
browser_instance = None
browser_lock = threading.Lock()


def init_browser():
    """初始化浏览器"""
    global browser_instance
    if browser_instance is None:
        try:
            from playwright.sync_api import sync_playwright
            p = sync_playwright().start()
            browser_instance = p.chromium.launch(headless=True)
            print("[+] 浏览器初始化成功")
        except Exception as e:
            print(f"[-] 浏览器初始化失败: {e}")


def get_page(url):
    """获取页面内容"""
    try:
        res = session.get(url, timeout=15)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"获取页面失败: {e}")
        return None


def parse_cards(html):
    """从页面解析内容卡片"""
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    
    # 查找所有卡片
    seen = set()
    for link in soup.select('a[href*="/play/"]'):
        href = link.get('href', '')
        if not href or href in seen:
            continue
        
        seen.add(href)
        
        title_tag = link.find('h2') or link.find('h3') or link.find('h1')
        img_tag = link.find('img')
        
        if title_tag and img_tag:
            title = title_tag.get_text(strip=True)
            cover = img_tag.get('src', '')
            
            if cover.startswith('//'):
                cover = 'https:' + cover
            
            items.append({
                "vod_id": href,
                "vod_name": title,
                "vod_pic": cover,
                "vod_remarks": ""
            })
    
    return items


def parse_detail(html):
    """解析详情页"""
    soup = BeautifulSoup(html, 'html.parser')
    vod = {
        "vod_id": "",
        "vod_name": "",
        "vod_pic": "",
        "type_name": "",
        "vod_year": "",
        "vod_area": "",
        "vod_actor": "",
        "vod_director": "",
        "vod_content": "",
        "vod_play_from": "4kvm",
        "vod_play_url": ""
    }
    
    title_tag = soup.find('h1') or soup.find('h2')
    if title_tag:
        vod["vod_name"] = title_tag.get_text(strip=True)
    
    poster = soup.select_one('.video-player img') or soup.select_one('img')
    if poster:
        vod["vod_pic"] = poster.get('src', '')
    
    desc = soup.select_one('div.text-gray-300, div.space-y-2, p')
    if desc:
        vod["vod_content"] = desc.get_text(strip=True)
    
    play_list = []
    episode_links = soup.select('a.episode-link')
    for link in episode_links:
        ep_title = link.get_text(strip=True)
        ep_href = link.get('href', '')
        if ep_title and ep_href:
            play_list.append(f"{ep_title}${ep_href}")
    
    if play_list:
        vod["vod_play_url"] = '#'.join(play_list)
    
    return vod


def get_m3u8_with_playwright(play_url):
    """使用 Playwright 获取真实 M3U8 地址"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            m3u8_url = None
            
            def capture_request(request):
                nonlocal m3u8_url
                url = request.url
                if '.m3u8' in url or 'm3u8' in url:
                    m3u8_url = url
                    print(f"[+] 捕获到 M3U8: {m3u8_url}")
            
            page.on("request", capture_request)
            
            print(f"[+] 访问播放页: {play_url}")
            page.goto(play_url, timeout=30000)
            page.wait_for_timeout(5000)
            
            browser.close()
            
            return m3u8_url
    except Exception as e:
        print(f"[-] Playwright 错误: {e}")
        return None


@app.route('/')
def index():
    return jsonify({
        "name": "4kvm.tv TVBox Source (Complete)",
        "status": "ok",
        "version": "2.0"
    })


@app.route('/api.php/provide/vod/')
def vod_api():
    ac = request.args.get('ac', '')
    t = request.args.get('t', '')
    wd = request.args.get('wd', '')
    pg = request.args.get('pg', '1')
    ids = request.args.get('ids', '')
    
    if ac == 'list':
        return list_vod(t, pg)
    elif ac == 'videolist' and ids:
        return get_detail(ids)
    elif ac == 'detail':
        return get_detail(request.args.get('id', ''))
    elif wd:
        return search_vod(wd, pg)
    else:
        return home_page()


def home_page():
    html = get_page(BASE_URL)
    if not html:
        return jsonify({"list": []})
    list_data = parse_cards(html)
    return jsonify({"code": 1, "list": list_data})


def list_vod(category, pg):
    category_map = {"1": "movie", "2": "tv", "3": "anime"}
    path = category_map.get(category, "movie")
    html = get_page(f"{BASE_URL}/{path}")
    if not html:
        return jsonify({"list": []})
    list_data = parse_cards(html)
    return jsonify({
        "code": 1,
        "list": list_data,
        "page": int(pg),
        "pagecount": 1,
        "limit": 20,
        "total": len(list_data)
    })


def search_vod(wd, pg):
    url = f"{BASE_URL}/search?q={urllib.parse.quote(wd)}"
    html = get_page(url)
    if not html:
        return jsonify({"list": []})
    list_data = parse_cards(html)
    return jsonify({"code": 1, "list": list_data})


def get_detail(vod_id):
    if not vod_id.startswith('http'):
        if vod_id.startswith('/play/'):
            url = BASE_URL + vod_id
        else:
            url = f"{BASE_URL}/play/{vod_id}"
    else:
        url = vod_id
    
    html = get_page(url)
    if not html:
        return jsonify({"list": []})
    
    vod = parse_detail(html)
    vod["vod_id"] = vod_id
    return jsonify({"code": 1, "list": [vod]})


@app.route('/api.php/provide/vod/play/')
def play_api():
    url = request.args.get('url', '')
    
    if not url.startswith('http'):
        if url.startswith('/play/'):
            url = BASE_URL + url
        else:
            url = f"{BASE_URL}/play/{url}"
    
    print(f"[+] 获取播放地址: {url}")
    
    m3u8_url = get_m3u8_with_playwright(url)
    
    return jsonify({
        "parse": 0,
        "playUrl": "",
        "url": m3u8_url if m3u8_url else "",
        "jx": 0,
        "header": ""
    })


@app.route('/config.js')
def config_js():
    return """var rule = {
        title: '4kvm.tv',
        host: 'http://127.0.0.1:5000',
        url: '/api.php/provide/vod/',
        searchUrl: '/api.php/provide/vod/?ac=list&wd=*',
        class_name: '电影&电视剧&动漫',
        class_url: '1&2&3',
        playUrl: '/api.php/provide/vod/play/?url=*'
    };"""


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║              4kvm.tv 完整 TVBox 源                           ║
╠══════════════════════════════════════════════════════════════╣
║  功能:                                                       ║
║  ✓ 首页推荐                                                  ║
║  ✓ 分类浏览 (电影/电视剧/动漫)                               ║
║  ✓ 搜索功能                                                  ║
║  ✓ 详情获取                                                  ║
║  ✓ Playwright 自动化获取播放地址                             ║
║                                                              ║
║  安装依赖: pip install flask requests beautifulsoup4 playwright
║  安装浏览器: playwright install chromium                    ║
║  TVBox配置: http://127.0.0.1:5000/config.js                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
