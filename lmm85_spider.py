import re
import time
import random
from base.spider import Spider

class Spider(Spider):
    def getName(self): return "路漫漫动漫"
    def init(self, extend=""): pass
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self): pass
    
    def __init__(self):
        self.url = 'https://www.lmm85.com'
        self.cookie_jar = {}
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    
    def _init_session(self):
        if not hasattr(self, '_session_initialized'):
            try:
                import requests
                self._http_session = requests.Session()
                self._http_session.headers.update(self.header)
                try:
                    r = self._http_session.get(self.url, timeout=10)
                    self.cookie_jar = dict(r.cookies)
                    time.sleep(random.uniform(1, 2))
                except:
                    pass
                self._session_initialized = True
            except ImportError:
                self._session_initialized = False
    
    def fetch(self, url, headers=None):
        """重写fetch方法，维护Cookie"""
        self._init_session()
        
        if hasattr(self, '_http_session') and self._http_session:
            try:
                req_headers = self.header.copy()
                if headers:
                    req_headers.update(headers)
                
                if 'Referer' not in req_headers:
                    req_headers['Referer'] = self.url + '/'
                
                if 'Sec-Fetch-Site' not in req_headers:
                    req_headers['Sec-Fetch-Site'] = 'same-origin'
                
                response = self._http_session.get(url, headers=req_headers, timeout=10)
                self.cookie_jar = dict(response.cookies)
                
                time.sleep(random.uniform(0.5, 1.5))
                
                return type('Response', (), {
                    'text': response.text,
                    'cookies': dict(response.cookies),
                    'headers': dict(response.headers)
                })()
            except Exception as e:
                print(f"[错误] 请求失败: {str(e)}")
                return type('Response', (), {'text': '', 'cookies': {}, 'headers': {}})()
        else:
            import urllib.request
            try:
                req = urllib.request.Request(url, headers=self.header)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    return type('Response', (), {'text': html, 'cookies': {}, 'headers': {}})()
            except Exception as e:
                print(f"[错误] 请求失败: {str(e)}")
                return type('Response', (), {'text': '', 'cookies': {}, 'headers': {}})()

    def homeContent(self, filter):
        c = [('国产动漫','guochandongman'),('动态漫画','dongtaiman'),('日本动漫','ribendongman'),('欧美动漫','oumeidongman'),('国产动画电影','guochandonghuadianying'),('日本动画电影','ribendonghuadianying'),('欧美动画电影','oumeidonghuadianying'),('日本特摄剧','teshepian')]
        return {'class': [{'type_name': n, 'type_id': i} for n, i in c]}

    def homeVideoContent(self):
        try:
            time.sleep(random.uniform(0.5, 1))
            response = self.fetch(self.url, headers={
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Site': 'cross-site'
            })
            return {'list': self._p(response.text)}
        except: return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            u = f'{self.url}/type/{tid}.html' if pg == '1' else f'{self.url}/type/{tid}_{pg}.html'
            time.sleep(random.uniform(0.3, 1))
            response = self.fetch(u, headers={
                'Referer': self.url + '/',
                'Sec-Fetch-Site': 'same-origin'
            })
            return {'list': self._p(response.text), 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 9999}
        except: return {'list': []}

    def detailContent(self, ids):
        try:
            detail_url = f'{self.url}/detail/{ids[0]}.html'
            h = self.fetch(detail_url, headers={
                'Referer': self.url + '/',
                'Sec-Fetch-Site': 'same-origin'
            }).text
            time.sleep(random.uniform(0.5, 1.5))
            
            v = {'vod_id': ids[0], 'vod_name': '', 'vod_pic': '', 'vod_type': '', 'vod_year': '', 'vod_area': '', 'vod_remarks': '', 'vod_actor': '', 'vod_director': '', 'vod_content': ''}
            m1 = re.search(r'<h1 class="page-title">(.*?)</h1>', h)
            if m1: v['vod_name'] = m1.group(1)
            m2 = re.search(r'class="url_img" alt=".*?" src="(.*?)"', h)
            if m2: v['vod_pic'] = m2.group(1)
            m3 = re.search(r'class="video-info-item video-info-content">(.*?)</div>', h, re.S)
            if m3: v['vod_content'] = re.sub(r'<[^>]+>', '', m3.group(1)).strip()
            ts = list(dict.fromkeys(re.findall(r'data-dropdown-value="(.*?)"', h)))
            us = []
            for b in h.split('class="module-list')[1:]:
                if 'module-blocklist' not in b: continue
                es = [f"{n}${self.url}{u}" for u, n in re.findall(r'<a href="(/play/.*?.html)".*?<span>(.*?)</span>', b)]
                if es: us.append("#".join(es))
            v['vod_play_from'] = "$$$".join(ts if len(ts) == len(us) else [f"线路{i+1}" for i in range(len(us))])
            v['vod_play_url'] = "$$$".join(us)
            return {'list': [v]}
        except: return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        try:
            self.fetch(self.url, headers={
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Site': 'cross-site'
            })
            time.sleep(random.uniform(0.5, 1))
            
            search_url = f'{self.url}/vod/search.html?wd={key}&page={pg}'
            response = self.fetch(search_url, headers={
                'Referer': self.url + '/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin'
            })
            time.sleep(random.uniform(1, 2))
            
            html = response.text
            if self._is_captcha_page(html):
                print(f"[警告] 搜索关键词 '{key}' 触发了验证码")
                return {'list': []}
            
            return {'list': self._p(html)}
        except Exception as e:
            print(f"[错误] 搜索失败: {str(e)}")
            return {'list': []}

    def _is_captcha_page(self, html):
        captcha_keywords = ['验证码', 'captcha', '验证失败', '请输入验证码', 
                          '安全验证', '人机验证', '点击验证', '滑块验证']
        html_lower = html.lower()
        for keyword in captcha_keywords:
            if keyword in html_lower:
                if any(x in html_lower for x in ['verify', 'check', 'token', 'challenge']):
                    return True
        return False

    def playerContent(self, flag, id, vipFlags):
        return {'parse': 1, 'url': id, 'header': self.header}

    def localProxy(self, param): return None

    def _p(self, h):
        l = []
        for c, t in re.findall(r'<div class="video-img-box.*?>(.*?)<h6 class="title">(.*?)</h6>', h, re.S):
            try:
                vid = re.search(r'href="/detail/(\d+).html"', c)
                if not vid: continue
                img = re.search(r'data-src="(.*?)"', c) or re.search(r'src="(.*?)"', c)
                rem = re.search(r'class="label">(.*?)</span>', c)
                tit = re.search(r'<a.*?>(.*?)</a>', t)
                l.append({'vod_id': vid.group(1), 'vod_name': tit.group(1) if tit else '', 'vod_pic': img.group(1) if img else '', 'vod_remarks': rem.group(1) if rem else ''})
            except: pass
        return l
