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
        self.url = 'https://www.lmm85.com'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
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
            base_url = f'{self.url}/vod/show'
            
            order_by = extend.get('by', '')
            year = extend.get('year', '')
            
            if order_by:
                u = f'{base_url}/by/{order_by}/id/{tid}'
            else:
                u = f'{base_url}/id/{tid}'
            
            if year:
                u = f'{u}/year/{year}'
            
            u = f'{u}/page/{pg}.html'
            
            response = self.fetch(u, headers=self.header)
            html = response.text
            
            page_info = self._extract_page_info(html)
            
            return {
                'list': self._p(html),
                'page': int(pg),
                'pagecount': page_info['pagecount'],
                'limit': 20,
                'total': page_info['total']
            }
        except Exception as e:
            print(f"[错误] categoryContent: {str(e)}")
            return {'list': [], 'page': 1, 'pagecount': 0, 'limit': 20, 'total': 0}

    def _extract_page_info(self, html):
        result = {'pagecount': 1, 'total': 0}
        
        total_match = re.search(r'(\d+)\s*部影片', html)
        if total_match:
            result['total'] = int(total_match.group(1))
        
        last_page_match = re.search(r'最后\s*».*?/page/(\d+)\.html', html)
        if last_page_match:
            result['pagecount'] = int(last_page_match.group(1))
        else:
            page_matches = re.findall(r'/page/(\d+)\.html', html)
            if page_matches:
                result['pagecount'] = max(int(p) for p in page_matches)
        
        return result

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
            encoded_key = urllib.parse.quote(key)
            
            url1 = f'{self.url}/vod/search/page/{pg}/wd/{encoded_key}.html'
            res1 = self.fetch(url1, headers=self.header).text
            if not self._is_captcha_page(res1):
                results = self._p(res1)
                if results: return {'list': results}
            
            print("[提示] 方案 1 触发验证或无结果，切入方案 2 (动态搜索)...")
            url2 = f'{self.url}/index.php/vod/search.html?wd={encoded_key}&page={pg}'
            res2 = self.fetch(url2, headers=self.header).text
            if not self._is_captcha_page(res2):
                results = self._p(res2)
                if results: return {'list': results}

            print("[提示] 方案 2 触发验证或无结果，切入方案 3 (长划线路由)...")
            url3 = f'{self.url}/vodsearch/{encoded_key}----------{pg}---.html'
            res3 = self.fetch(url3, headers=self.header).text
            if not self._is_captcha_page(res3):
                results = self._p(res3)
                if results: return {'list': results}

            print("[警告] 网页搜索全部被拦截，启用最终 Ajax 联想接口越轨抓取...")
            return self._ajax_search_fallback(encoded_key)

        except Exception as e:
            print(f"[错误] 搜索发生严重异常: {str(e)}")
            return {'list': []}

    def _ajax_search_fallback(self, encoded_key):
        try:
            ajax_url = f'{self.url}/index.php/ajax/suggest?mid=1&wd={encoded_key}&limit=50'
            ajax_headers = self.header.copy()
            ajax_headers['X-Requested-With'] = 'XMLHttpRequest'
            ajax_headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            
            res_text = self.fetch(ajax_url, headers=ajax_headers).text
            if self._is_captcha_page(res_text):
                return {'list': []}
                
            data = json.loads(res_text)
            if data and isinstance(data, dict) and data.get('list'):
                fallback_list = [{
                    'vod_id': str(item.get('id', '')),
                    'vod_name': item.get('name', ''),
                    'vod_pic': item.get('pic', ''),
                    'vod_remarks': '高速线路'
                } for item in data['list']]
                return {'list': fallback_list}
            return {'list': []}
        except Exception as e:
            print(f"[错误] Ajax 兜底彻底失效: {str(e)}")
            return {'list': []}

    def _is_captcha_page(self, html):
        keywords = ['身份验证', '验证码', 'captcha', '验证失败', '请输入验证码', '安全验证', '人机验证', '不要频繁操作']
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in keywords)

    def playerContent(self, flag, id, vipFlags):
        try:
            play_url = f"{self.url}{id}" if id.startswith('/') else id
            
            result = {
                'parse': 1,
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
                vid = re.search(r'href="/detail/(\d+)\.html"', c)
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
