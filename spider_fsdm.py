import re
import time
import random
import json
import urllib.parse
from base.spider import Spider

class Spider(Spider):
    def getName(self): return "番薯动漫"
    def init(self, extend=""): pass
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self): pass
    
    def __init__(self):
        self.url = 'https://www.fsdm02.com'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
    
    def homeContent(self, filter):
        classes = [
            ('TV番剧', '1'),
            ('国产动漫', '2'),
            ('剧场版', '3'),
            ('4k分区', '4'),
            ('欧美动漫', '5')
        ]
        return {'class': [{'type_name': n, 'type_id': i} for n, i in classes]}

    def homeVideoContent(self):
        try:
            response = self.fetch(self.url, headers=self.header)
            return {'list': self._p(response.text)}
        except Exception as e:
            print(f"[错误] homeVideoContent: {str(e)}")
            return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            if int(pg) > 1:
                u = f'{self.url}/vodtype/{tid}-{pg}.html'
            else:
                u = f'{self.url}/vodtype/{tid}.html'
            
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
        
        total_match = re.search(r'共\s*(\d+)\s*部', html)
        if total_match:
            result['total'] = int(total_match.group(1))
        
        last_page_match = re.search(r'<a[^>]*href="[^"]*/vodtype/[^"]*-(\d+)\.html"[^>]*>末页</a>', html)
        if last_page_match:
            result['pagecount'] = int(last_page_match.group(1))
        else:
            page_matches = re.findall(r'/vodtype/[^"]*-(\d+)\.html', html)
            if page_matches:
                page_numbers = [int(p) for p in page_matches if p.isdigit()]
                if page_numbers:
                    result['pagecount'] = max(page_numbers)
        
        return result

    def detailContent(self, ids):
        try:
            h = self.fetch(f'{self.url}/voddetail/{ids[0]}.html', headers=self.header).text
            v = {'vod_id': ids[0], 'vod_name': '', 'vod_pic': '', 'vod_type': '', 'vod_year': '', 'vod_area': '', 'vod_remarks': '', 'vod_actor': '', 'vod_director': '', 'vod_content': ''}
            
            m1 = re.search(r'<h1[^>]*>([^<]+)</h1>', h)
            if m1: v['vod_name'] = m1.group(1).strip()
            
            m2 = re.search(r'<img[^>]*class="[^"]*lazyload[^"]*"[^>]*data-src="([^"]+)"', h) or re.search(r'<img[^>]*src="([^"]+)"[^>]*class="[^"]*lazyload', h)
            if m2: v['vod_pic'] = m2.group(1)
            
            m3 = re.search(r'<div[^>]*class="[^"]*desc[^"]*"[^>]*>(.*?)</div>', h, re.S) or re.search(r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>', h, re.S)
            if m3: v['vod_content'] = re.sub(r'<[^>]+>', '', m3.group(1)).strip()
            
            info_text = h
            year_match = re.search(r'年份</span>[:：]\s*<a[^>]*>([^<]+)</a>', info_text) or re.search(r'(\d{4})', info_text[:500])
            if year_match: v['vod_year'] = year_match.group(1).strip()
            
            area_match = re.search(r'地区</span>[:：]\s*<a[^>]*>([^<]+)</a>', info_text)
            if area_match: v['vod_area'] = area_match.group(1).strip()
            
            actor_match = re.search(r'主演</span>[:：]\s*(.*?)</li>', info_text, re.S)
            if actor_match: v['vod_actor'] = re.sub(r'<[^>]+>', '', actor_match.group(1)).strip()
            
            play_list_match = re.search(r'<ul[^>]*class="[^"]*scroll-content[^"]*"[^>]*>(.*?)</ul>', h, re.S)
            us = []
            if play_list_match:
                episodes = re.findall(r'<a[^>]*href="/vodplay/([^"]+)"[^>]*>([^<]+)</a>', play_list_match.group(1))
                if episodes:
                    es = [f"{n}${self.url}/vodplay/{u}" for u, n in episodes]
                    us.append("#".join(es))
            
            v['vod_play_from'] = "$$$".join([f"线路{i+1}" for i in range(len(us))])
            v['vod_play_url'] = "$$$".join(us)
            return {'list': [v]}
        except Exception as e:
            print(f"[错误] detailContent: {str(e)}")
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        try:
            time.sleep(random.uniform(0.3, 0.8))
            encoded_key = urllib.parse.quote(key)
            
            url1 = f'{self.url}/vodsearch/{encoded_key}----------{pg}---.html'
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
        keywords = ['身份验证', '验证码', 'captcha', '验证失败', '请输入验证码', '安全验证', '人机验证', '不要频繁操作', 'Security Verification']
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in keywords)

    def playerContent(self, flag, id, vipFlags):
        try:
            play_url = id if id.startswith('http') else (f"{self.url}{id}" if id.startswith('/') else f"{self.url}/{id}")
            
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
        for match in re.finditer(r'<div[^>]*class="[^"]*module-card-poster[^"]*"[^>]*>(.*?)</div>', html, re.S):
            try:
                c = match.group(1)
                vid_match = re.search(r'href="/voddetail/([^"]+)\.html"', c)
                if not vid_match:
                    continue
                
                vid = vid_match.group(1)
                
                img = re.search(r'data-src="([^"]+)"', c) or re.search(r'src="([^"]+)"', c)
                
                rem_match = re.search(r'<span[^>]*class="[^"]*score[^"]*"[^>]*>([^<]+)</span>', c) or re.search(r'<span[^>]*class="[^"]*remark[^"]*"[^>]*>([^<]+)</span>', c)
                
                tit = re.search(r'<a[^>]*href="/voddetail/[^"]+\.html"[^>]*>([^<]+)</a>', c)
                
                l.append({
                    'vod_id': vid,
                    'vod_name': tit.group(1).strip() if tit else '',
                    'vod_pic': img.group(1) if img else '',
                    'vod_remarks': rem_match.group(1).strip() if rem_match else ''
                })
            except Exception as e:
                print(f"[错误] _p: {str(e)}")
        return l
