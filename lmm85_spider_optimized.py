import re
import time
import random
import json
import base64
from urllib.parse import urljoin, parse_qs, urlencode
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
        self._session_initialized = False
        self._http_session = None
    
    def _init_session(self):
        if not self._session_initialized:
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
                self._session_initialized = True
    
    def fetch(self, url, headers=None):
        """重写fetch方法，维护Cookie"""
        self._init_session()
        
        if self._http_session:
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
        """
        播放器解析核心逻辑
        分析网站视频播放机制：
        1. 大多数视频网站使用 m3u8 流媒体格式
        2. 可能使用 iframe 嵌套第三方播放器
        3. 可能使用 JavaScript 动态加载视频地址
        4. 可能使用 base64 或其他编码混淆视频URL
        
        针对不同情况返回正确的播放信息
        """
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            
            headers = {
                'Referer': self.url + '/',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate'
            }
            
            html = self.fetch(play_url, headers=headers).text
            
            video_url = self._extract_video_url(html)
            
            if video_url:
                return {
                    'parse': 0,
                    'url': video_url,
                    'header': self.header,
                    'redirect': ''
                }
            
            iframe_url = self._extract_iframe_url(html)
            if iframe_url:
                return {
                    'parse': 1,
                    'url': iframe_url,
                    'header': self.header,
                    'redirect': ''
                }
            
            return {'parse': 1, 'url': id, 'header': self.header}
            
        except Exception as e:
            print(f"[错误] 播放解析失败: {str(e)}")
            return {'parse': 1, 'url': id, 'header': self.header}

    def _extract_video_url(self, html):
        """提取直接的视频URL"""
        
        patterns = [
            r'video.*?src=["\'](.*?\.mp4)["\']',
            r'<source.*?src=["\'](.*?)["\']',
            r'player\.src\(["\'](.*?)["\']',
            r'"url"\s*:\s*["\'](.*?\.m3u8)["\']',
            r'"url"\s*:\s*["\'](.*?\.mp4)["\']',
            r'data-url=["\'](.*?)["\']',
            r'videoUrl\s*=\s*["\'](.*?)["\']',
            r'"(https?://[^"\']+\.m3u8[^"\']*)"',
            r'"(https?://[^"\']+\.mp4[^"\']*)"'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                url = match if isinstance(match, str) else match[0] if isinstance(match, tuple) else ''
                if url and (url.endswith('.m3u8') or url.endswith('.mp4')):
                    if self._is_valid_video_url(url):
                        return url
        
        return None

    def _extract_iframe_url(self, html):
        """提取iframe嵌套的播放源"""
        patterns = [
            r'<iframe[^>]+src=["\'](.*?)["\']',
            r'iframe.*?src=(["\'])(.*?)\1',
            r'src=["\'](.*?player.*?)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                url = match if isinstance(match, str) else match[1] if isinstance(match, tuple) else ''
                if url and 'player' in url.lower():
                    return url
        
        return None

    def _is_valid_video_url(self, url):
        """验证URL是否有效"""
        if not url:
            return False
        if url.startswith('//'):
            url = 'https:' + url
        if not url.startswith('http'):
            return False
        if 'localhost' in url or '127.0.0.1' in url:
            return False
        return True

    def _decode_video_url(self, encoded_url):
        """解码混淆的视频URL"""
        try:
            if '+' in encoded_url or '-' in encoded_url:
                decoded = base64.b64decode(encoded_url.encode()).decode()
                return decoded
        except:
            pass
        return encoded_url

    def _analyze_m3u8_playlist(self, m3u8_url):
        """分析m3u8播放列表，返回最佳清晰度的URL"""
        try:
            response = self.fetch(m3u8_url, headers={
                'Referer': self.url,
                'Accept': '*/*'
            })
            
            lines = response.text.split('\n')
            base_url = m3u8_url.rsplit('/', 1)[0] + '/'
            
            urls = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        urls.append(line)
                    else:
                        urls.append(base_url + line)
            
            if urls:
                return urls[-1]
            
        except Exception as e:
            print(f"[错误] m3u8解析失败: {str(e)}")
        
        return m3u8_url

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
