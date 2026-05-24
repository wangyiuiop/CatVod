import re
import time
import random
import json
import urllib.parse
from base.spider import Spider

class Spider(Spider):
    def getName(self): return "路漫漫"
    def init(self, extend=""): pass
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self): pass
    
    def __init__(self):
        self.url = "https://www.lmm85.com"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def homeContent(self, filter):
        classes = [
            ('日本动漫', '6'),
            ('国产动漫', '7'),
            ('欧美动漫', '8'),
            ('日本动画电影', '3'),
            ('国产动画电影', '4'),
            ('欧美动画电影', '5')
        ]
        return {'class': [{'type_name': n, 'type_id': i} for n, i in classes]}

    def homeVideoContent(self):
        try:
            response = self.fetch(self.url, headers=self.header)
            return {'list': self._p(response.text)}
        except:
            return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            url = f"{self.url}/vod/show/id/{tid}/page/{pg}.html"
            response = self.fetch(url, headers=self.header)
            return {'list': self._p(response.text), 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 9999}
        except:
            return {'list': []}

    def detailContent(self, ids):
        try:
            html = self.fetch(f"{self.url}/detail/{ids[0]}.html", headers=self.header).text
            v = {'vod_id': ids[0], 'vod_name': '', 'vod_pic': '', 'vod_type': '', 'vod_year': '', 'vod_area': '', 'vod_remarks': '', 'vod_actor': '', 'vod_director': '', 'vod_content': ''}
            
            m1 = re.search(r'<h1 class="page-title">(.*?)</h1>', html)
            if m1:
                v['vod_name'] = m1.group(1)
            
            m2 = re.search(r'class="module-item-pic.*?<img.*?src="(.*?)"', html, re.S)
            if m2:
                v['vod_pic'] = m2.group(1)
            
            m3 = re.search(r'class="video-info-content">(.*?)</div>', html, re.S)
            if m3:
                v['vod_content'] = re.sub(r'<[^>]+>', '', m3.group(1)).strip()
            
            tags = re.findall(r'<a class="tag-link"[^>]*>(.*?)</a>', html)
            if tags:
                v['vod_actor'] = ','.join(tags[:5])
            
            ts = list(dict.fromkeys(re.findall(r'data-dropdown-value="(.*?)"', html)))
            us = []
            for b in html.split('class="module-list')[1:]:
                if 'module-blocklist' not in b:
                    continue
                es = [f"{n}${self.url}{u}" for u, n in re.findall(r'<a href="(/play/.*?.html)".*?<span>(.*?)</span>', b)]
                if es:
                    us.append('#'.join(es))
            
            v['vod_play_from'] = '$$$'.join(ts if len(ts) == len(us) else [f"线路{i+1}" for i in range(len(us))])
            v['vod_play_url'] = '$$$'.join(us)
            return {'list': [v]}
        except:
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        try:
            time.sleep(random.uniform(0.3, 0.8))
            search_url = f"{self.url}/vod/search/page/{pg}/wd/{key}.html"
            response = self.fetch(search_url, headers=self.header)
            html = response.text
            if self._is_captcha_page(html):
                return {'list': []}
            return {'list': self._p(html)}
        except:
            return {'list': []}

    def _is_captcha_page(self, html):
        keywords = ['验证码', 'captcha', '验证失败', '请输入验证码', '安全验证', '人机验证']
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in keywords)

    def playerContent(self, flag, id, vipFlags):
        """
        播放器解析 - 优化版
        直接返回播放页面，让播放器处理iframe和CDN
        """
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            
            # 构建完整的请求头，帮助播放CDN视频
            result = {
                'parse': 1,  # 让播放器处理解析
                'url': play_url,
                'header': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': self.url,
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'parse': 1,
                'url': id,
                'header': self.header
            }

    def localProxy(self, param):
        return None

    def _p(self, html):
        l = []
        for c, t in re.findall(r'<div class="video-img-box.*?>(.*?)<h6 class="title">(.*?)</h6>', html, re.S):
            try:
                vid = re.search(r'href="/detail/(\d+).html"', c)
                if not vid:
                    continue
                img = re.search(r'data-src="(.*?)"', c) or re.search(r'src="(.*?)"', c)
                rem = re.search(r'class="label">(.*?)</span>', c)
                tit = re.search(r'<a.*?>(.*?)</a>', t)
                l.append({
                    'vod_id': vid.group(1),
                    'vod_name': tit.group(1) if tit else '',
                    'vod_pic': img.group(1) if img else '',
                    'vod_remarks': rem.group(1) if rem else ''
                })
            except:
                pass
        return l
