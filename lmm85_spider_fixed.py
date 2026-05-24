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
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Referer': self.url}

    def homeContent(self, filter):
        c = [('国产动漫','guochandongman'),('动态漫画','dongtaiman'),('日本动漫','ribendongman'),('欧美动漫','oumeidongman'),('国产动画电影','guochandonghuadianying'),('日本动画电影','ribendonghuadianying'),('欧美动画电影','oumeidonghuadianying'),('日本特摄剧','teshepian')]
        return {'class': [{'type_name': n, 'type_id': i} for n, i in c]}

    def homeVideoContent(self):
        try: return {'list': self._p(self.fetch(self.url, headers=self.header).text)}
        except: return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            u = f'{self.url}/type/{tid}.html' if pg == '1' else f'{self.url}/type/{tid}_{pg}.html'
            return {'list': self._p(self.fetch(u, headers=self.header).text), 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 9999}
        except: return {'list': []}

    def detailContent(self, ids):
        try:
            h = self.fetch(f'{self.url}/detail/{ids[0]}.html', headers=self.header).text
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
            time.sleep(random.uniform(0.5, 1))
            response = self.fetch(f'{self.url}/vod/search.html?wd={key}&page={pg}', headers=self.header)
            html = response.text
            if self._is_captcha_page(html):
                time.sleep(random.uniform(1, 2))
                response = self.fetch(f'{self.url}/vod/search.html?wd={key}&page={pg}', headers=self.header)
                html = response.text
            if self._is_captcha_page(html):
                print(f"[警告] 搜索关键词 '{key}' 可能触发了验证码")
                return {'list': []}
            return {'list': self._p(html)}
        except Exception as e:
            print(f"[错误] 搜索失败: {str(e)}")
            return {'list': []}

    def _is_captcha_page(self, html):
        captcha_keywords = ['验证码', 'captcha', '验证失败', '请输入验证码', 
                          '安全验证', '人机验证', '访问异常', '系统检测']
        html_lower = html.lower()
        for keyword in captcha_keywords:
            if keyword in html_lower:
                return True
        return False

    def playerContent(self, flag, id, vipFlags):
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            h = self.fetch(play_url, headers=self.header).text
            video_url = self._extract_video_url(h)
            if video_url:
                return {'parse': 0, 'url': video_url, 'header': self.header}
            iframe_url = self._extract_iframe_url(h)
            if iframe_url:
                return {'parse': 1, 'url': iframe_url, 'header': self.header}
            return {'parse': 1, 'url': id, 'header': self.header}
        except Exception as e:
            print(f"[错误] 播放解析失败: {str(e)}")
            return {'parse': 1, 'url': id, 'header': self.header}

    def _extract_video_url(self, html):
        patterns = [
            r'video.*?src=["\'](.*?\.mp4)["\']',
            r'<source.*?src=["\'](.*?)["\']',
            r'"url"\s*:\s*["\'](.*?)["\']',
            r'"(https?://[^"\']+\.(?:m3u8|mp4)[^"\']*)"',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                url = match if isinstance(match, str) else match[0]
                if url and (url.endswith('.m3u8') or url.endswith('.mp4') or 'player' in url.lower()):
                    return url
        return None

    def _extract_iframe_url(self, html):
        patterns = [
            r'<iframe[^>]+src=["\'](.*?)["\']',
            r'<iframe.*?src=(["\'])(.*?)\1',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                url = match if isinstance(match, str) else match[1] if isinstance(match, tuple) else ''
                if url and ('player' in url.lower() or 'embed' in url.lower()):
                    return url
        return None

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
