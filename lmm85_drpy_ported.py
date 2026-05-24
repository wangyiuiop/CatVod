import re
import time
import random
import base64
import json
from urllib.parse import urljoin, parse_qs, urlencode
from base.spider import Spider

class Spider(Spider):
    def getName(self): return "路漫漫"
    def init(self, extend=""): pass
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self): pass
    
    def __init__(self):
        self.url = 'https://www.lmm85.com'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Referer': self.url,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
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
        except: return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            u = f'{self.url}/vod/show/id/{tid}/page/{pg}.html'
            if extend:
                for key, value in extend.items():
                    if value:
                        u = u.replace('id/' + tid, f'id/{tid}/{key}/{value}')
            response = self.fetch(u, headers=self.header)
            return {'list': self._p(response.text), 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 9999}
        except: return {'list': []}

    def detailContent(self, ids):
        try:
            h = self.fetch(f'{self.url}/detail/{ids[0]}.html', headers=self.header).text
            v = {'vod_id': ids[0], 'vod_name': '', 'vod_pic': '', 'vod_type': '', 'vod_year': '', 'vod_area': '', 'vod_remarks': '', 'vod_actor': '', 'vod_director': '', 'vod_content': ''}
            m1 = re.search(r'<h1 class="page-title">(.*?)</h1>', h)
            if m1: v['vod_name'] = m1.group(1)
            m2 = re.search(r'class="module-item-pic.*?<img.*?src="(.*?)"', h, re.S)
            if m2: v['vod_pic'] = m2.group(1)
            m3 = re.search(r'<div class="video-info-content">(.*?)</div>', h, re.S)
            if m3: v['vod_content'] = re.sub(r'<[^>]+>', '', m3.group(1)).strip()
            
            tags = re.findall(r'<a class="tag-link"[^>]*>(.*?)</a>', h)
            if tags: v['vod_actor'] = ','.join(tags[:5])
            
            areas = re.findall(r'<a class="tag-link"[^>]*href="[^"]*area/[^"]*"[^>]*>(.*?)</a>', h)
            if areas: v['vod_area'] = areas[0]
            
            years = re.findall(r'<a class="tag-link"[^>]*href="[^"]*year/[^"]*"[^>]*>(.*?)</a>', h)
            if years: v['vod_year'] = years[0]
            
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
            time.sleep(random.uniform(0.3, 0.8))
            search_url = f'{self.url}/vod/search/page/{pg}/wd/{key}.html'
            response = self.fetch(search_url, headers=self.header)
            html = response.text
            if self._is_captcha_page(html):
                print(f"[警告] 搜索 '{key}' 可能触发了验证码")
                return {'list': []}
            return {'list': self._p(html)}
        except: return {'list': []}

    def _is_captcha_page(self, html):
        keywords = ['验证码', 'captcha', '验证失败', '请输入验证码', '安全验证', '人机验证']
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in keywords)

    def playerContent(self, flag, id, vipFlags):
        """
        播放器解析核心逻辑
        从Drpy JS配置移植，包含复杂的AES加密和POST请求处理
        """
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            html = self.fetch(play_url, headers=self.header).text
            
            player_data = self._extract_player_data(html)
            if not player_data:
                return {'parse': 1, 'url': id, 'header': self.header}
            
            video_url = self._resolve_video_url(player_data, play_url)
            if video_url:
                return {'parse': 0, 'url': video_url, 'header': self.header}
            
            return {'parse': 1, 'url': id, 'header': self.header}
            
        except Exception as e:
            print(f"[错误] 播放解析失败: {str(e)}")
            return {'parse': 1, 'url': id, 'header': self.header}

    def _extract_player_data(self, html):
        """从HTML中提取播放器数据"""
        patterns = [
            r'player_.*?=\s*(\{.*?\});?\s*</script>',
            r'<script[^>]*>\s*var\s+player_.*?=\s*(\{.*?\})\s*;?\s*</script>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.S)
            if match:
                try:
                    player_str = match.group(1)
                    player_json = json.loads(player_str)
                    return player_json
                except:
                    continue
        return None

    def _resolve_video_url(self, player_data, referer):
        """解析视频URL，处理加密和重定向"""
        try:
            url = player_data.get('url', '')
            from_name = player_data.get('from', '')
            encrypt = player_data.get('encrypt', 0)
            
            if encrypt == 1:
                url = self._decrypt_url_type1(url)
            elif encrypt == 2:
                url = self._decrypt_url_type2(url)
            
            if self._is_direct_video_url(url):
                return url.split('&')[0] if '&' in url else url
            
            if not from_name:
                return url
            
            player_js_url = f"{self.url}/static/player/{from_name}.js"
            player_js = self.fetch(player_js_url, headers={
                'Referer': referer,
                **self.header
            }).text
            
            video_url = self._parse_player_js(player_js, url, referer)
            return video_url
            
        except Exception as e:
            print(f"[错误] 视频URL解析失败: {str(e)}")
            return None

    def _decrypt_url_type1(self, url):
        """解密类型1：直接unescape"""
        try:
            import urllib.parse
            return urllib.parse.unquote(url)
        except:
            return url

    def _decrypt_url_type2(self, url):
        """解密类型2：base64 + unescape"""
        try:
            import urllib.parse
            decoded = base64.b64decode(url).decode('utf-8')
            return urllib.parse.unquote(decoded)
        except:
            return url

    def _parse_player_js(self, js_content, url, referer):
        """解析播放器JS文件，提取视频URL"""
        try:
            src_pattern = r'\.src\s*=\s*(.*?);'
            match = re.search(src_pattern, js_content)
            if not match:
                return None
            
            js_code = match.group(1).strip()
            js_code = js_code.replace("'", "").replace("+", "").replace(" ", "")
            
            if 'MacPlayer.PlayUrl' in js_code:
                js_code = js_code.replace('MacPlayer.PlayUrl', f'"{url}"')
            
            if '/player?type=' in js_code or 'type=' in js_code:
                parse_url = self._build_parse_url(js_code, referer)
                if parse_url:
                    response = self.fetch(parse_url, headers={
                        'Referer': referer,
                        **self.header
                    })
                    return self._extract_url_from_response(response.text, js_code, referer)
            
            return None
            
        except Exception as e:
            print(f"[错误] JS解析失败: {str(e)}")
            return None

    def _build_parse_url(self, js_code, referer):
        """构建解析URL"""
        try:
            if 'player?type=' in js_code:
                type_match = re.search(r'type=([^&"\']+)', js_code)
                if type_match:
                    return f"{self.url}/static/player.php?type={type_match.group(1)}&url="
            return None
        except:
            return None

    def _extract_url_from_response(self, response_text, js_code, referer):
        """从响应中提取视频URL"""
        try:
            if 'act=' in response_text or 'vid=' in response_text:
                return self._handle_post_request(response_text, js_code, referer)
            
            if 'post(' in response_text:
                return self._handle_post_request(response_text, js_code, referer)
            
            if self._is_direct_video_url(response_text):
                return response_text.split('&')[0] if '&' in response_text else response_text
            
            return None
            
        except Exception as e:
            print(f"[错误] URL提取失败: {str(e)}")
            return None

    def _handle_post_request(self, response_text, js_code, referer):
        """处理POST请求获取视频URL"""
        try:
            post_api_match = re.search(r'^(.*?\/\/.*?\/.*?)\/', response_text)
            if not post_api_match:
                post_api_match = re.search(r'posturl\s*=\s*["\'](.*?)["\']', response_text)
            
            if not post_api_match:
                return None
            
            post_url = post_api_match.group(1) if 'posturl' not in str(post_api_match.groups()) else post_api_match.group(1)
            
            body = {}
            
            vid_match = re.search(r'vid\s*=\s*["\'](.*?)["\']', response_text)
            if vid_match:
                body['vid'] = vid_match.group(1)
            
            t_match = re.search(r'var\s+t\s*=\s*["\'](.*?)["\']', response_text)
            if t_match:
                body['t'] = t_match.group(1)
            
            token_match = re.search(r'token\s*=\s*["\'](.*?)["\']', response_text)
            if token_match:
                body['token'] = token_match.group(1)
            
            act_match = re.search(r'act\s*=\s*["\'](.*?)["\']', response_text)
            if act_match:
                body['act'] = act_match.group(1)
            
            play_match = re.search(r'play\s*=\s*["\'](.*?)["\']', response_text)
            if play_match:
                body['play'] = play_match.group(1)
            
            if body:
                response = self._post_request(post_url, body, {'Referer': referer})
                if response:
                    return self._parse_video_response(response)
            
            return None
            
        except Exception as e:
            print(f"[错误] POST请求处理失败: {str(e)}")
            return None

    def _post_request(self, url, data, headers=None):
        """发送POST请求"""
        try:
            import urllib.parse
            body = urllib.parse.urlencode(data)
            headers = headers or self.header
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            import urllib.request
            req = urllib.request.Request(url, data=body.encode(), headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[错误] POST请求失败: {str(e)}")
            return None

    def _parse_video_response(self, response_text):
        """解析视频响应"""
        try:
            data = json.loads(response_text)
            url = data.get('url', '')
            
            if not url:
                return None
            
            ext = data.get('ext', '')
            
            if ext == 'hls' or ext == 'hls_list':
                from urllib.parse import unquote
                return unquote(url)
            
            if ext == 'xgplayer':
                xgplayer_url = f"https://yun.366day.site/mp4hls/xgplayer.php?vid={url}"
                response = self.fetch(xgplayer_url, headers={'Referer': self.url})
                match = re.search(r'"url":\s*"(.*?)"', response.text)
                if match:
                    return match.group(1)
                return None
            
            return url
            
        except Exception as e:
            print(f"[错误] 响应解析失败: {str(e)}")
            return None

    def _is_direct_video_url(self, url):
        """检查是否为直接视频URL"""
        if not url:
            return False
        video_extensions = ['.mp4', '.m3u8', '.flv', '.mkv', '.avi']
        return any(url.lower().endswith(ext) for ext in video_extensions)

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
                l.append({
                    'vod_id': vid.group(1),
                    'vod_name': tit.group(1) if tit else '',
                    'vod_pic': img.group(1) if img else '',
                    'vod_remarks': rem.group(1) if rem else ''
                })
            except: pass
        return l
