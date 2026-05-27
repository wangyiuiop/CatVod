
# coding=utf-8
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.url = 'https://www.4kmovie.top'
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
        self.headers = {
            'User-Agent': self.UA,
            'Referer': self.url,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'Accept': '*/*'
        }

    def categoryContent(self, tid, pg="1", filter=False, extend=None):
        pg = pg or "1"
        pg_int = int(pg)
        
        if pg_int > 1:
            link = f"{self.url}/vodtype/{tid}-{pg}.html"
        else:
            link = f"{self.url}/vodtype/{tid}.html"
        
        print(f"测试分类: {tid} - {link}")
        
        try:
            res = requests.get(link, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            videos = []
            for a in soup.select('.module-poster-item'):
                href = a.get('href', '')
                if not href:
                    continue

                vod_id_match = re.search(r'/vod(?:play|detail)/(\d+)', href)
                vod_id = vod_id_match.group(1) if vod_id_match else ''
                
                title_elem = a.select_one('.module-poster-item-title')
                title = a.get('title') or (title_elem.text.strip() if title_elem else '')
                
                img_elem = a.select_one('.module-item-pic img')
                pic = ''
                if img_elem:
                    pic = img_elem.get('data-original') or img_elem.get('src', '')

                note_elem = a.select_one('.module-item-note')
                remarks = note_elem.text.strip() if note_elem else ''

                videos.append({
                    'vod_id': vod_id,
                    'vod_name': title,
                    'vod_pic': pic,
                    'vod_remarks': remarks
                })

            has_more = len(soup.select('.page-next')) > 0 or len(soup.select('.next')) > 0
            
            result = {
                'page': pg_int,
                'pagecount': pg_int + 1 if has_more else pg_int,
                'limit': len(videos),
                'total': len(videos) * (pg_int + 1 if has_more else pg_int),
                'list': videos
            }
            
            print(f"找到 {len(result['list'])} 个视频")
            
            if len(result['list']) > 0:
                print(f"前3个视频:")
                for v in result['list'][:3]:
                    print(f"  - {v['vod_name']} ({v['vod_remarks']})")
            
            return result
        except Exception as e:
            print(f"错误: {e}")
            return {
                'page': pg_int,
                'pagecount': pg_int,
                'limit': 0,
                'total': 0,
                'list': []
            }


if __name__ == "__main__":
    print("=== 测试修复后的分类功能 ===")
    spider = Spider()
    
    test_categories = [
        (20, "电影"),
        (37, "电视剧"),
        (45, "综艺"),
        (43, "动漫"),
        (47, "B站")
    ]
    
    for tid, name in test_categories:
        print(f"\n--- {name} (ID: {tid}) ---")
        spider.categoryContent(tid)
