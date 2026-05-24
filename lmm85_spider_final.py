import re
import time
import random
import base64
import json
import urllib.parse
from base.spider import Spider

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("[警告] pycryptodome 库未安装，AES解密功能将不可用")
    print("[提示] 安装命令: pip install pycryptodome")

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
        self.cookie_jar = {}
    
    def get_daes_string(self, token):
        """
        AES CBC解密token
        Drpy配置中的密钥和IV:
        - key: "ejjooopppqqqrwww"
        - iv: "1348987635684651"
        """
        if not CRYPTO_AVAILABLE:
            print("[错误] AES解密需要 pycryptodome 库")
            return None
        
        try:
            key = b'ejjooopppqqqrwww'  # 16字节密钥
            iv = b'1348987635684651'  # 16字节IV
            
            token_bytes = base64.b64decode(token)
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(token_bytes)
            
            try:
                return unpad(decrypted, AES.block_size).decode('utf-8')
            except:
                return decrypted.rstrip(b'\x00').decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[错误] AES解密失败: {str(e)}")
            return None
    
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
            url = f'{self.url}/vod/show/id/{tid}/page/{pg}.html'
            if extend:
                for key, value in extend.items():
                    if value:
                        url = url.replace(f'id/{tid}', f'id/{tid}/{key}/{value}')
            response = self.fetch(url, headers=self.header)
            return {'list': self._p(response.text), 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 9999}
        except: return {'list': []}

    def detailContent(self, ids):
        try:
            html = self.fetch(f'{self.url}/detail/{ids[0]}.html', headers=self.header).text
            v = {'vod_id': ids[0], 'vod_name': '', 'vod_pic': '', 'vod_type': '', 'vod_year': '', 'vod_area': '', 'vod_remarks': '', 'vod_actor': '', 'vod_director': '', 'vod_content': ''}
            
            m1 = re.search(r'<h1 class="page-title">(.*?)</h1>', html)
            if m1: v['vod_name'] = m1.group(1)
            
            m2 = re.search(r'class="module-item-pic.*?<img.*?src="(.*?)"', html, re.S)
            if m2: v['vod_pic'] = m2.group(1)
            
            m3 = re.search(r'class="video-info-content">(.*?)</div>', html, re.S)
            if m3: v['vod_content'] = re.sub(r'<[^>]+>', '', m3.group(1)).strip()
            
            tags = re.findall(r'<a class="tag-link"[^>]*>(.*?)</a>', html)
            if tags: v['vod_actor'] = ','.join(tags[:5])
            
            ts = list(dict.fromkeys(re.findall(r'data-dropdown-value="(.*?)"', html)))
            us = []
            for b in html.split('class="module-list')[1:]:
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
                print(f"[警告] 搜索 '{key}' 触发了验证码")
                return {'list': []}
            return {'list': self._p(html)}
        except: return {'list': []}

    def _is_captcha_page(self, html):
        keywords = ['验证码', 'captcha', '验证失败', '请输入验证码', '安全验证', '人机验证']
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in keywords)

    def playerContent(self, flag, id, vipFlags):
        """
        播放器解析核心逻辑 - 完整实现
        """
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            html = self.fetch(play_url, headers=self.header).text
            
            player_data = self._extract_player_data(html)
            if not player_data:
                print("[调试] 未找到player_data，使用降级方案")
                return {'parse': 1, 'url': id, 'header': self.header}
            
            print(f"[调试] player_data: {json.dumps(player_data, ensure_ascii=False)}")
            
            video_url = self._resolve_video_url(player_data, play_url)
            if video_url:
                return {'parse': 0, 'url': video_url, 'header': self.header}
            
            return {'parse': 1, 'url': id, 'header': self.header}
        except Exception as e:
            print(f"[错误] 播放解析失败: {str(e)}")
            import traceback
            print(f"[错误] 堆栈: {traceback.format_exc()}")
            return {'parse': 1, 'url': id, 'header': self.header}

    def _extract_player_data(self, html):
        """从HTML中提取player_.*?= {...} JSON数据"""
        patterns = [
            r'var\s+player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
            r'player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
            r'<script[^>]*>\s*var\s+player[^=]*=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;?\s*<\/script>',
            r'player_.*?=\s*(\{.*?\})\s*;',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, html, re.S):
                try:
                    data_str = match.group(1)
                    data = json.loads(data_str)
                    return data
                except json.JSONDecodeError:
                    continue
        
        return None

    def _resolve_video_url(self, player_data, referer):
        """解析视频URL"""
        try:
            url = player_data.get('url', '')
            from_name = player_data.get('from', '')
            encrypt = player_data.get('encrypt', 0)
            
            print(f"[调试] 原始URL: {url}, from: {from_name}, encrypt: {encrypt}")
            
            if encrypt == 1:
                url = urllib.parse.unquote(url)
                print(f"[调试] unescape解密后: {url}")
            elif encrypt == 2:
                try:
                    decoded = base64.b64decode(url).decode('utf-8')
                    url = urllib.parse.unquote(decoded)
                    print(f"[调试] base64+unescape解密后: {url}")
                except:
                    pass
            
            if self._is_direct_video_url(url):
                return url.split('&')[0] if '&' in url else url
            
            if not from_name:
                print("[调试] 无from信息，返回降级方案")
                return None
            
            player_js_url = f"{self.url}/static/player/{from_name}.js"
            print(f"[调试] 获取player JS: {player_js_url}")
            
            try:
                player_js = self.fetch(player_js_url, headers={
                    'Referer': referer,
                    **self.header
                }).text
            except Exception as e:
                print(f"[错误] 获取player JS失败: {str(e)}")
                return None
            
            video_url = self._parse_player_js(player_js, url, referer)
            return video_url
        except Exception as e:
            print(f"[错误] 视频URL解析失败: {str(e)}")
            return None

    def _parse_player_js(self, js_content, url, referer):
        """解析player JS，提取播放URL"""
        try:
            src_pattern = r'\.src\s*=\s*([^;]+?);'
            match = re.search(src_pattern, js_content)
            if not match:
                return None
            
            js_code = match.group(1).strip()
            print(f"[调试] JS代码片段: {js_code[:200]}")
            
            if 'MacPlayer.PlayUrl' in js_code:
                js_code = js_code.replace('MacPlayer.PlayUrl', f'"{url}"')
            
            if 'MacPlayer.Parse' in js_code:
                js_code = js_code.replace('MacPlayer.Parse', '')
            
            if '/player?type=' in js_code or 'type=' in js_code:
                return self._handle_type1(js_code, url, referer)
            
            return None
        except Exception as e:
            print(f"[错误] JS解析失败: {str(e)}")
            return None

    def _handle_type1(self, js_code, url, referer):
        """处理type1类型的播放逻辑"""
        try:
            parse_url = None
            
            if '/player?type=' in js_code:
                type_match = re.search(r'type=([^&"\']+)', js_code)
                if type_match:
                    parse_url = f"{self.url}/static/player?type={type_match.group(1)}&url="
            
            if not parse_url:
                return None
            
            response_text = self.fetch(parse_url, headers={
                'Referer': referer,
                **self.header
            }).text
            
            return self._extract_url_from_response(response_text, referer)
        except Exception as e:
            print(f"[错误] type1处理失败: {str(e)}")
            return None

    def _extract_url_from_response(self, response_text, referer):
        """从响应中提取视频URL"""
        try:
            if 'act=' in response_text or 'vid=' in response_text:
                return self._handle_post_request(response_text, referer)
            
            if 'post(' in response_text:
                return self._handle_post_request(response_text, referer)
            
            if self._is_direct_video_url(response_text):
                return response_text.split('&')[0] if '&' in response_text else response_text
            
            url_match = re.search(r'"url"\s*:\s*"([^"]+)"', response_text)
            if url_match:
                return url_match.group(1)
            
            return None
        except Exception as e:
            print(f"[错误] URL提取失败: {str(e)}")
            return None

    def _handle_post_request(self, response_text, referer):
        """处理POST请求"""
        try:
            post_api_match = re.search(r'post\(["\'](.*?)["\']', response_text)
            if not post_api_match:
                return None
            
            post_url = post_api_match.group(1)
            print(f"[调试] POST URL: {post_url}")
            
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
            
            if 'token' in body and CRYPTO_AVAILABLE:
                print(f"[调试] 解密前token: {body['token']}")
                decrypted_token = self.get_daes_string(body['token'])
                if decrypted_token:
                    print(f"[调试] 解密后token: {decrypted_token}")
                    body['token'] = decrypted_token
            
            print(f"[调试] POST body: {body}")
            
            if body:
                response = self._post_request(post_url, body, {'Referer': referer})
                if response:
                    return self._parse_video_response(response)
            
            return None
        except Exception as e:
            print(f"[错误] POST处理失败: {str(e)}")
            return None

    def _post_request(self, url, data, headers=None):
        """发送POST请求"""
        try:
            req_headers = self.header.copy()
            if headers:
                req_headers.update(headers)
            
            import urllib.request
            import urllib.parse
            import urllib.error
            
            req_data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=req_data, headers=req_headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[错误] POST请求失败: {str(e)}")
            return None

    def _parse_video_response(self, response_text):
        """解析视频响应"""
        try:
            data = json.loads(response_text)
            print(f"[调试] 响应数据: {json.dumps(data, ensure_ascii=False)}")
            
            url = data.get('url', '')
            if not url:
                return None
            
            ext = data.get('ext', '')
            print(f"[调试] URL: {url}, ext: {ext}")
            
            if ext == 'hls' or ext == 'hls_list':
                return urllib.parse.unquote(url)
            
            if ext == 'xgplayer':
                xgplayer_url = f"https://yun.366day.site/mp4hls/xgplayer.php?vid={url}"
                try:
                    response = self.fetch(xgplayer_url, headers={'Referer': self.url})
                    match = re.search(r'"url"\s*:\s*"([^"]+)"', response.text)
                    if match:
                        return match.group(1)
                except Exception as e:
                    print(f"[错误] xgplayer请求失败: {str(e)}")
                return None
            
            return url
        except Exception as e:
            print(f"[错误] 响应解析失败: {str(e)}")
            return None

    def _is_direct_video_url(self, url):
        """检查是否为直接视频URL"""
        if not url:
            return False
        
        video_extensions = ['.mp4', '.m3u8', '.flv', '.mkv', '.avi', '.ts']
        
        for ext in video_extensions:
            if ext in url.lower():
                return True
        
        return False

    def localProxy(self, param): return None

    def _p(self, html):
        l = []
        for c, t in re.findall(r'<div class="video-img-box.*?>(.*?)<h6 class="title">(.*?)</h6>', html, re.S):
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
