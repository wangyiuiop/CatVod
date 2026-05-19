#!/usr/bin/env python3
"""
TVBox 4kvm.tv 完整爬虫
结合 Playwright 真实调用 WebAssembly 获取播放地址
"""

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import json
import base64
import time
import urllib.parse
from playwright.sync_api import sync_playwright

app = Flask(__name__)

BASE_URL = "https://www.4kvm.tv"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
})


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


def get_real_m3u8_url(play_url):
    """
    使用 Playwright 获取真实 M3U8 地址
    这是最可靠的方法 - 真实执行 WASM 模块
    """
    m3u8_url = None
    api_response = None
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            def handle_request(request):
                nonlocal m3u8_url, api_response
                url = request.url
                
                # 捕获 M3U8 请求
                if '.m3u8' in url:
                    m3u8_url = url
                    print(f"[+] 捕获 M3U8: {url}")
                
                # 捕获 API 响应
                if '/video/play' in url and request.method == 'GET':
                    print(f"[+] 捕获 API 请求: {url}")
            
            def handle_response(response):
                nonlocal api_response
                url = response.url
                
                # 捕获 API 响应
                if '/video/play' in url:
                    try:
                        api_response = response.json()
                        print(f"[+] 捕获 API 响应: {str(api_response)[:200]}")
                    except:
                        pass
            
            page.on("request", handle_request)
            page.on("response", handle_response)
            
            print(f"[+] 访问播放页: {play_url}")
            page.goto(play_url, timeout=30000)
            
            # 等待页面加载和视频开始播放
            page.wait_for_timeout(8000)
            
            # 尝试点击播放按钮（如果需要）
            try:
                play_button = page.query_selector('button.play, [class*="play"]')
                if play_button:
                    play_button.click()
                    page.wait_for_timeout(3000)
            except:
                pass
            
            browser.close()
            
            # 如果直接捕获到 M3U8，返回它
            if m3u8_url:
                return m3u8_url
            
            # 如果捕获到 API 响应，尝试从中提取 M3U8
            if api_response:
                if isinstance(api_response, dict):
                    # 尝试各种可能的字段
                    for key in ['url', 'm3u8', 'playUrl', 'video', 'src', 'source']:
                        if key in api_response:
                            return api_response[key]
            
            return None
            
    except Exception as e:
        print(f"[-] Playwright 错误: {e}")
        return None


def reverse_engineer_build_url(dataid, vodid, quality="1080"):
    """
    尝试逆向 build_play_url 函数
    基于已知参数生成 URL
    """
    timestamp = str(int(time.time() * 1000))
    
    # 参数
    params = {
        'p': dataid,
        'v': vodid,
        'q': quality,
        't': timestamp,
    }
    
    # 生成签名 (s 参数)
    # 基于观察：s 可能是某种 MD5/SHA 哈希
    import hashlib
    
    # 尝试不同的组合
    signature_input = f"{dataid}{vodid}{quality}{timestamp}"
    signature = hashlib.md5(signature_input.encode()).hexdigest()
    params['s'] = signature
    
    # 生成 k 参数 (base64 编码)
    k_input = f"{signature}:{timestamp}"
    params['k'] = base64.b64encode(k_input.encode()).decode()
    
    # 构建 URL
    query = urllib.parse.urlencode(params)
    full_url = f"{BASE_URL}/video/play?{query}"
    
    return full_url


# ==================== API 接口 ====================

@app.route('/')
def index():
    return jsonify({
        "name": "4kvm.tv TVBox Source (WASM逆向版)",
        "status": "ok",
        "version": "3.0",
        "method": "使用 Playwright 调用真实 WASM 模块"
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
    """
    播放地址获取
    使用 Playwright 真实调用 WASM 模块
    """
    url = request.args.get('url', '')
    
    if not url.startswith('http'):
        if url.startswith('/play/'):
            url = BASE_URL + url
        else:
            url = f"{BASE_URL}/play/{url}"
    
    print(f"\n{'='*60}")
    print(f"[+] 获取播放地址: {url}")
    print(f"{'='*60}")
    
    # 方法1: 使用 Playwright (最可靠)
    m3u8_url = get_real_m3u8_url(url)
    
    if m3u8_url:
        print(f"[+] 成功获取 M3U8: {m3u8_url}")
        return jsonify({
            "parse": 1,
            "playUrl": m3u8_url,
            "url": m3u8_url,
            "jx": 0,
            "header": ""
        })
    
    # 方法2: 尝试逆向 (可能失败)
    print("[!] Playwright 方法失败，尝试逆向...")
    
    # 提取参数
    html = get_page(url)
    if html:
        dataid_match = re.search(r'dataid="([^"]+)"', html)
        vodid_match = re.search(r'var\s+vodid\s*=\s*["\']([^"\']+)["\']', html)
        
        if dataid_match and vodid_match:
            dataid = dataid_match.group(1)
            vodid = vodid_match.group(1)
            
            # 尝试生成 URL
            generated_url = reverse_engineer_build_url(dataid, vodid)
            print(f"[+] 生成的 URL: {generated_url}")
            
            return jsonify({
                "parse": 0,
                "playUrl": "",
                "url": generated_url,
                "jx": 0,
                "header": "",
                "note": "这是尝试逆向的 URL，可能需要进一步验证"
            })
    
    return jsonify({
        "parse": 0,
        "playUrl": "",
        "url": "",
        "jx": 0,
        "header": "",
        "error": "无法获取播放地址"
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
╔══════════════════════════════════════════════════════════════════╗
║            4kvm.tv TVBox 源 - WebAssembly 逆向版              ║
╠══════════════════════════════════════════════════════════════════╣
║  功能:                                                         ║
║  ✓ 首页推荐                                                    ║
║  ✓ 分类浏览 (电影/电视剧/动漫)                                  ║
║  ✓ 搜索功能                                                    ║
║  ✓ 详情获取                                                    ║
║  ✓ Playwright 真实调用 WASM 获取播放地址                       ║
║                                                              ║
║  安装:                                                        ║
║  pip install flask requests beautifulsoup4 playwright        ║
║  playwright install chromium                                  ║
║                                                              ║
║  运行: python tvbox_final_solution.py                         ║
║  TVBox配置: http://127.0.0.1:5000/config.js                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
