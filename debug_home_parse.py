
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

try:
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    items = soup.select('.module-poster-item')[:10]  # 只看前10个
    print(f"=== 解析前 10 个元素 ===")
    
    videos = []
    for i, item in enumerate(items):
        print(f"\n--- 元素 {i+1} ---")
        
        href = item.get('href', '')
        print(f"href: {href}")
        
        vod_id_match = re.search(r'/vod(?:play|detail)/(\d+)', href)
        vod_id = vod_id_match.group(1) if vod_id_match else ''
        print(f"vod_id: {vod_id}")
        
        title_elem = item.select_one('.module-poster-item-title')
        title = item.get('title') or (title_elem.text.strip() if title_elem else '')
        print(f"title: {title}")
        
        img_elem = item.select_one('.module-item-pic img')
        pic = ''
        if img_elem:
            pic = img_elem.get('data-original') or img_elem.get('src', '')
        print(f"pic: {pic}")
        
        note_elem = item.select_one('.module-item-note')
        remarks = note_elem.text.strip() if note_elem else ''
        print(f"remarks: {remarks}")
        
        video_data = {
            'vod_id': vod_id,
            'vod_name': title,
            'vod_pic': pic,
            'vod_remarks': remarks
        }
        videos.append(video_data)
    
    print(f"\n\n=== 完整解析结果前 3 项 ===")
    print(json.dumps(videos[:3], ensure_ascii=False, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
