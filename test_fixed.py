
# coding=utf-8
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup

# 模拟基类以便测试
class Spider:
    def getName(self):
        return ""

    def init(self, extend=""):
        pass

    def homeContent(self, filter):
        return {'class': [], 'filters': {}}

    def homeVideoContent(self):
        return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        return {'list': []}

    def detailContent(self, array):
        return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        return {}

class FixedSpider(Spider):
    def getName(self):
        return "4K电影"

    def init(self, extend=""):
        self.url = 'https://www.4kmovie.top'
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
        self.headers = {
            'User-Agent': self.UA,
            'Referer': self.url,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'Accept': '*/*'
        }

    def searchContent(self, key, quick, pg="1"):
        pg = pg or "1"
        link = f"{self.url}/vodsearch/{urllib.parse.quote(key)}----------{pg}---.html"
        res = requests.get(link, headers=self.headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        videos = []
        for item in soup.select('.module-card-item'):
            # 获取链接和ID
            poster = item.select_one('.module-card-item-poster')
            if not poster:
                continue
                
            href = poster.get('href')
            vod_id_match = re.search(r'/vod(?:play|detail)/(\d+)', href)
            vod_id = vod_id_match.group(1) if vod_id_match else ''
            
            # 获取标题
            title_a = item.select_one('.module-card-item-title a')
            title = title_a.text.strip() if title_a else ''
            
            # 获取图片
            img_elem = item.select_one('.module-item-pic img')
            pic = ''
            if img_elem:
                pic = img_elem.get('data-original') or img_elem.get('src', '')
            
            # 获取备注
            note_elem = item.select_one('.module-item-note')
            remarks = note_elem.text.strip() if note_elem else ''

            videos.append({
                'vod_id': vod_id,
                'vod_name': title,
                'vod_pic': pic,
                'vod_remarks': remarks
            })

        has_more = len(soup.select('.page-next')) > 0
        pg_int = int(pg)

        return {
            'page': pg_int,
            'pagecount': pg_int + 1 if has_more else pg_int,
            'limit': len(videos),
            'total': len(videos) * (pg_int + 1 if has_more else pg_int),
            'list': videos
        }

# 测试我们的修复是否有效
if __name__ == "__main__":
    spider = FixedSpider()
    spider.init()
    
    print("测试搜索功能...")
    result = spider.searchContent('良陈美锦', False, '1')
    
    print(f"搜索结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['list']:
        print("\n✅ 搜索成功！")
        for item in result['list']:
            print(f"\n标题: {item['vod_name']}")
            print(f"ID: {item['vod_id']}")
            print(f"备注: {item['vod_remarks']}")
            print(f"封面: {item['vod_pic']}")
    else:
        print("\n❌ 搜索失败，没有找到结果")
