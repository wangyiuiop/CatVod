#!/usr/bin/env python3
"""
TVBox 源 - 4kvm.tv
包含完整功能：主页、分类、搜索、详情、播放
"""

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import json
import base64
import time
import urllib.parse

app = Flask(__name__)

BASE_URL = "https://www.4kvm.tv"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
})


def get_page(url):
    """获取页面内容"""
    try:
        res = session.get(url, timeout=10)
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
    # 查找包含 play 链接和图片的元素
    for link in soup.select('a[href*="/play/"]'):
        href = link.get('href', '')
        if not href or href in seen:
            continue
        
        seen.add(href)
        
        # 查找标题和封面
        title_tag = link.find('h2') or link.find('h3') or link.find('h1')
        img_tag = link.find('img')
        
        if title_tag and img_tag:
            title = title_tag.get_text(strip=True)
            cover = img_tag.get('src', '')
            # 处理图片地址
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
    
    # 获取标题
    title_tag = soup.find('h1') or soup.find('h2')
    if title_tag:
        vod["vod_name"] = title_tag.get_text(strip=True)
    
    # 获取封面
    poster = soup.select_one('.video-player img') or soup.select_one('img')
    if poster:
        vod["vod_pic"] = poster.get('src', '')
    
    # 获取简介
    desc = soup.select_one('div.text-gray-300, div.space-y-2, p')
    if desc:
        vod["vod_content"] = desc.get_text(strip=True)
    
    # 获取播放列表
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


def extract_m3u8_from_network(html):
    """
    尝试从页面中找到线索 (简化版)
    实际生产建议使用 Playwright/Selenium
    """
    # 从页面提取关键参数
    info = {}
    
    # 查找 pdf
    pdf_match = re.search(r'window\._pdf\s*=\s*"([^"]+)"', html)
    if pdf_match:
        info['pdf'] = pdf_match.group(1)
    
    # 查找 dataid
    dataid_match = re.search(r'dataid="([^"]+)"', html)
    if dataid_match:
        info['dataid'] = dataid_match.group(1)
    
    # 查找 meta
    soup = BeautifulSoup(html, 'html.parser')
    nb_st = soup.find('meta', {'id': 'nb-st'})
    if nb_st:
        info['nb_st'] = nb_st.get('content', '')
    
    # 返回一个 placeholder，实际生产使用浏览器自动化
    return {
        "parse": 0,
        "playUrl": "",
        "url": "",
        "jx": 0,
        "header": "",
        "extra": {
            "info": info
        }
    }


@app.route('/')
def index():
    return jsonify({
        "name": "4kvm.tv TVBox Source",
        "status": "ok",
        "author": "Generated"
    })


@app.route('/api.php/provide/vod/')
def vod_api():
    ac = request.args.get('ac', '')
    t = request.args.get('t', '')
    wd = request.args.get('wd', '')
    pg = request.args.get('pg', '1')
    ids = request.args.get('ids', '')
    
    if ac == 'list':
        # 获取列表
        return list_vod(t, pg)
    elif ac == 'videolist' and ids:
        # 获取详情
        return get_detail(ids)
    elif ac == 'detail':
        return get_detail(request.args.get('id', ''))
    elif wd:
        # 搜索
        return search_vod(wd, pg)
    else:
        # 主页
        return home_page()


def home_page():
    """首页内容"""
    html = get_page(BASE_URL)
    if not html:
        return jsonify({"list": []})
    
    list_data = parse_cards(html)
    return jsonify({
        "code": 1,
        "list": list_data
    })


def list_vod(category, pg):
    """分类列表"""
    category_map = {
        "1": "movie",
        "2": "tv",
        "3": "anime"
    }
    path = category_map.get(category, "movie")
    url = f"{BASE_URL}/{path}"
    
    html = get_page(url)
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
    """搜索功能"""
    url = f"{BASE_URL}/search?q={urllib.parse.quote(wd)}"
    html = get_page(url)
    if not html:
        return jsonify({"list": []})
    
    list_data = parse_cards(html)
    return jsonify({
        "code": 1,
        "list": list_data
    })


def get_detail(vod_id):
    """获取详情"""
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
    return jsonify({
        "code": 1,
        "list": [vod]
    })


@app.route('/api.php/provide/vod/play/')
def play_api():
    """
    播放地址获取
    注意：需要配合 Playwright 使用，
    这里仅做框架
    """
    url = request.args.get('url', '')
    if not url.startswith('http'):
        if url.startswith('/play/'):
            url = BASE_URL + url
    
    html = get_page(url)
    result = extract_m3u8_from_network(html)
    
    return jsonify(result)


@app.route('/config.js')
def config_js():
    """返回 TVBox 配置"""
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
║                    4kvm.tv TVBox 源                           ║
╠══════════════════════════════════════════════════════════════╣
║  使用说明:                                                    ║
║  1. 运行本服务: python tvbox_4kvm.py                         ║
║  2. 在TVBox中配置: http://127.0.0.1:5000/config.js           ║
║                                                              ║
║  为了获取完整播放地址，建议搭配使用:                        ║
║  - Playwright/Selenium 自动化浏览器                         ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
