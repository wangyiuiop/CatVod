
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
        
        area = extend.get('area', '') if extend else ''
        by = extend.get('by', 'time') if extend else 'time'
        cls = extend.get('class', '') if extend else ''
        lang = extend.get('lang', '') if extend else ''
        letter = extend.get('letter', '') if extend else ''
        year = extend.get('year', '') if extend else ''
        
        has_filter = any([area, by != 'time', cls, lang, letter, year])
        
        if has_filter:
            link = f"{self.url}/vodshow/{tid}-{area}-{by}-{cls}-{lang}-{letter}---{pg}---{year}.html"
            link_type = "vodshow（带筛选）"
        else:
            if pg_int > 1:
                link = f"{self.url}/vodtype/{tid}-{pg}.html"
                link_type = "vodtype（分页）"
            else:
                link = f"{self.url}/vodtype/{tid}.html"
                link_type = "vodtype（第1页）"
        
        print(f"\n测试分类 {tid} - {link_type}")
        print(f"URL: {link}")
        print(f"筛选条件: area={area}, by={by}, class={cls}, lang={lang}, letter={letter}, year={year}")
        
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
            
            print(f"找到 {len(videos)} 个视频")
            
            if len(videos) > 0:
                print("前5个视频:")
                for i, v in enumerate(videos[:5]):
                    print(f"  {i+1}. {v['vod_name']} ({v['vod_remarks']})")
            
            return {
                'page': pg_int,
                'pagecount': pg_int + 1 if has_more else pg_int,
                'limit': len(videos),
                'total': len(videos) * (pg_int + 1 if has_more else pg_int),
                'list': videos
            }
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
    print("=== 测试筛选功能 ===")
    spider = Spider()
    
    # 测试1：电影分类，无筛选（第1页）
    spider.categoryContent(20, "1", False, {})
    
    # 测试2：电影分类，按地区筛选
    spider.categoryContent(20, "1", False, {'area': '美国'})
    
    # 测试3：电影分类，按年份筛选
    spider.categoryContent(20, "1", False, {'year': '2024'})
    
    # 测试4：电影分类，按剧情类型筛选
    spider.categoryContent(20, "1", False, {'class': '喜剧'})
    
    # 测试5：电影分类，多个筛选条件
    spider.categoryContent(20, "1", False, {'area': '美国', 'year': '2024', 'class': '动作'})
    
    # 测试6：电视剧分类，无筛选（第1页）
    spider.categoryContent(37, "1", False, {})
    
    # 测试7：电视剧分类，按地区筛选
    spider.categoryContent(37, "1", False, {'area': '内地'})
    
    # 测试8：电影分类，无筛选（第2页）
    spider.categoryContent(20, "2", False, {})
