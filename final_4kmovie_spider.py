
# coding=utf-8
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
from base.spider import Spider


class Spider(Spider):
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

    def homeContent(self, filter):
        classes = [
            {'type_id': 20, 'type_name': '电影'},
            {'type_id': 37, 'type_name': '电视剧'},
            {'type_id': 45, 'type_name': '综艺'},
            {'type_id': 43, 'type_name': '动漫'},
            {'type_id': 47, 'type_name': 'B站'}
        ]

        filterObj = {
            '20': [{'key': 'class', 'name': '剧情', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '恐怖', 'v': '恐怖'}, {'n': '动作', 'v': '动作'}, {'n': '科幻', 'v': '科幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '战争', 'v': '战争'}, {'n': '警匪', 'v': '警匪'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动画', 'v': '动画'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '武侠', 'v': '武侠'}, {'n': '冒险', 'v': '冒险'}, {'n': '枪战', 'v': '枪战'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '经典', 'v': '经典'}, {'n': '青春', 'v': '青春'}, {'n': '文艺', 'v': '文艺'}, {'n': '古装', 'v': '古装'}, {'n': '历史', 'v': '历史'}, {'n': '运动', 'v': '运动'}, {'n': '网络电影', 'v': '网络电影'}]}, {'key': 'area', 'name': '地区', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '大陆', 'v': '大陆'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '美国', 'v': '美国'}, {'n': '法国', 'v': '法国'}, {'n': '英国', 'v': '英国'}, {'n': '日本', 'v': '日本'}, {'n': '韩国', 'v': '韩国'}, {'n': '德国', 'v': '德国'}, {'n': '泰国', 'v': '泰国'}, {'n': '印度', 'v': '印度'}, {'n': '意大利', 'v': '意大利'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '其他', 'v': '其他'}]}, {'key': 'lang', 'name': '语言', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '法语', 'v': '法语'}, {'n': '德语', 'v': '德语'}, {'n': '其它', 'v': '其它'}]}, {'key': 'year', 'name': '年份', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '2026', 'v': '2026'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}]}, {'key': 'letter', 'name': '字母', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': 'A', 'v': 'A'}, {'n': 'B', 'v': 'B'}, {'n': 'C', 'v': 'C'}, {'n': 'D', 'v': 'D'}, {'n': 'E', 'v': 'E'}, {'n': 'F', 'v': 'F'}, {'n': 'G', 'v': 'G'}, {'n': 'H', 'v': 'H'}, {'n': 'I', 'v': 'I'}, {'n': 'J', 'v': 'J'}, {'n': 'K', 'v': 'K'}, {'n': 'L', 'v': 'L'}, {'n': 'M', 'v': 'M'}, {'n': 'N', 'v': 'N'}, {'n': 'O', 'v': 'O'}, {'n': 'P', 'v': 'P'}, {'n': 'Q', 'v': 'Q'}, {'n': 'R', 'v': 'R'}, {'n': 'S', 'v': 'S'}, {'n': 'T', 'v': 'T'}, {'n': 'U', 'v': 'U'}, {'n': 'V', 'v': 'V'}, {'n': 'W', 'v': 'W'}, {'n': 'X', 'v': 'X'}, {'n': 'Y', 'v': 'Y'}, {'n': 'Z', 'v': 'Z'}, {'n': '0-9', 'v': '0-9'}]}, {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}],
            '37': [{'key': 'class', 'name': '剧情', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '古装', 'v': '古装'}, {'n': '战争', 'v': '战争'}, {'n': '青春偶像', 'v': '青春偶像'}, {'n': '喜剧', 'v': '喜剧'}, {'n': '家庭', 'v': '家庭'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动作', 'v': '动作'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '历史', 'v': '历史'}, {'n': '经典', 'v': '经典'}, {'n': '乡村', 'v': '乡村'}, {'n': '情景', 'v': '情景'}, {'n': '商战', 'v': '商战'}, {'n': '网剧', 'v': '网剧'}, {'n': '其他', 'v': '其他'}]}, {'key': 'area', 'name': '地区', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '内地', 'v': '内地'}, {'n': '韩国', 'v': '韩国'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '日本', 'v': '日本'}, {'n': '美国', 'v': '美国'}, {'n': '泰国', 'v': '泰国'}, {'n': '印度', 'v': '印度'}, {'n': '英国', 'v': '英国'}, {'n': '新加坡', 'v': '新加坡'}, {'n': '其他', 'v': '其他'}]}, {'key': 'lang', 'name': '语言', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '其它', 'v': '其它'}]}, {'key': 'year', 'name': '年份', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '2026', 'v': '2026'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}]}, {'key': 'letter', 'name': '字母', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': 'A', 'v': 'A'}, {'n': 'B', 'v': 'B'}, {'n': 'C', 'v': 'C'}, {'n': 'D', 'v': 'D'}, {'n': 'E', 'v': 'E'}, {'n': 'F', 'v': 'F'}, {'n': 'G', 'v': 'G'}, {'n': 'H', 'v': 'H'}, {'n': 'Z', 'v': 'Z'}, {'n': '0-9', 'v': '0-9'}]}, {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}],
            '45': [{'key': 'class', 'name': '剧情', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '选秀', 'v': '选秀'}, {'n': '情感', 'v': '情感'}, {'n': '访谈', 'v': '访谈'}, {'n': '播报', 'v': '播报'}, {'n': '旅游', 'v': '旅游'}, {'n': '音乐', 'v': '音乐'}, {'n': '美食', 'v': '美食'}, {'n': '纪实', 'v': '纪实'}, {'n': '游戏互动', 'v': '游戏互动'}, {'n': '财经', 'v': '财经'}, {'n': '求职', 'v': '求职'}]}, {'key': 'area', 'name': '地区', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '内地', 'v': '内地'}, {'n': '港台', 'v': '港台'}, {'n': '日韩', 'v': '日韩'}, {'n': '欧美', 'v': '欧美'}]}, {'key': 'year', 'name': '年份', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '2026', 'v': '2026'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}]}, {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}],
            '43': [{'key': 'class', 'name': '剧情', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '情感', 'v': '情感'}, {'n': '科幻', 'v': '科幻'}, {'n': '热血', 'v': '热血'}, {'n': '推理', 'v': '推理'}, {'n': '搞笑', 'v': '搞笑'}, {'n': '冒险', 'v': '冒险'}, {'n': '萝莉', 'v': '萝莉'}, {'n': '校园', 'v': '校园'}, {'n': '动作', 'v': '动作'}, {'n': '机战', 'v': '机战'}, {'n': '运动', 'v': '运动'}, {'n': '战争', 'v': '战争'}, {'n': '原创', 'v': '原创'}, {'n': '其他', 'v': '其他'}]}, {'key': 'area', 'name': '地区', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '国产', 'v': '国产'}, {'n': '日本', 'v': '日本'}, {'n': '欧美', 'v': '欧美'}, {'n': '其他', 'v': '其他'}]}, {'key': 'year', 'name': '年份', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': '2026', 'v': '2026'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}]}, {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}],
            '47': [{'key': 'letter', 'name': '字母', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': 'A', 'v': 'A'}, {'n': 'B', 'v': 'B'}, {'n': 'C', 'v': 'C'}, {'n': 'D', 'v': 'D'}, {'n': 'E', 'v': 'E'}, {'n': 'F', 'v': 'F'}, {'n': 'G', 'v': 'G'}, {'n': 'H', 'v': 'H'}, {'n': 'I', 'v': 'I'}, {'n': 'J', 'v': 'J'}, {'n': 'K', 'v': 'K'}, {'n': 'L', 'v': 'L'}, {'n': 'M', 'v': 'M'}, {'n': 'N', 'v': 'N'}, {'n': 'O', 'v': 'O'}, {'n': 'P', 'v': 'P'}, {'n': 'Q', 'v': 'Q'}, {'n': 'R', 'v': 'R'}, {'n': 'S', 'v': 'S'}, {'n': 'T', 'v': 'T'}, {'n': 'U', 'v': 'U'}, {'n': 'V', 'v': 'V'}, {'n': 'W', 'v': 'W'}, {'n': 'X', 'v': 'X'}, {'n': 'Y', 'v': 'Y'}, {'n': 'Z', 'v': 'Z'}, {'n': '0-9', 'v': '0-9'}]}, {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}]
        }

        return {'class': classes, 'filters': filterObj}

    def homeVideoContent(self):
        try:
            res = requests.get(self.url, headers=self.headers, timeout=10)
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
            return {'list': videos}
        except Exception as e:
            return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        pg = pg or "1"
        pg_int = int(pg)
        
        # 修复的URL格式：使用 /vodtype/{tid}-{pg}.html
        if pg_int > 1:
            link = f"{self.url}/vodtype/{tid}-{pg}.html"
        else:
            link = f"{self.url}/vodtype/{tid}.html"
        
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
            
            return {
                'page': pg_int,
                'pagecount': pg_int + 1 if has_more else pg_int,
                'limit': len(videos),
                'total': len(videos) * (pg_int + 1 if has_more else pg_int),
                'list': videos
            }
        except Exception as e:
            return {
                'page': pg_int,
                'pagecount': pg_int,
                'limit': 0,
                'total': 0,
                'list': []
            }

    def detailContent(self, array):
        vod_id = array[0]
        res = requests.get(f"{self.url}/voddetail/{vod_id}.html", headers=self.headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        vod = {'vod_id': vod_id}
        
        heading = soup.select_one('.module-info-heading h1')
        if heading:
            a_tag = heading.find('a')
            vod['vod_name'] = a_tag.text.strip() if a_tag else heading.text.strip()
        else:
            vod['vod_name'] = ''

        img_elem = soup.select_one('.module-item-pic img')
        if img_elem:
            vod['vod_pic'] = img_elem.get('data-original') or img_elem.get('src', '')
        else:
            vod['vod_pic'] = ''

        notes = soup.select('.module-item-note')
        vod['vod_remarks'] = notes[0].text.strip() if notes else ''

        contents = soup.select('.module-info-item-content')
        vod['vod_content'] = contents[-1].text.strip() if contents else ''

        play_map = {}
        tabs = soup.select('.module-tab-items .module-tab-item')
        lists = soup.select('.module-play-list-content')

        for i, tab in enumerate(tabs):
            small_elem = tab.find('small')
            if small_elem:
                small_text = small_elem.text
                from_name = tab.text.replace(small_text, '').strip()
            else:
                from_name = tab.text.strip()

            if not from_name:
                from_name = f'线路{i + 1}'

            if i >= len(lists):
                continue

            a_list = lists[i].select('a.module-play-list-link')
            episode_list = []
            
            for a in a_list:
                span = a.find('span')
                title = span.text.strip() if span else a.text.strip()
                play_id = a.get('href')
                episode_list.append(f"{title}${play_id}")
            
            if episode_list:
                play_map[from_name] = "#".join(episode_list)

        vod['vod_play_from'] = "$$$".join(play_map.keys())
        vod['vod_play_url'] = "$$$".join(play_map.values())

        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        pg = pg or "1"
        link = f"{self.url}/vodsearch/{urllib.parse.quote(key)}----------{pg}---.html"
        res = requests.get(link, headers=self.headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        videos = []
        for item in soup.select('.module-card-item'):
            poster = item.select_one('.module-card-item-poster')
            if not poster:
                continue
                
            href = poster.get('href')
            vod_id_match = re.search(r'/vod(?:play|detail)/(\d+)', href)
            vod_id = vod_id_match.group(1) if vod_id_match else ''
            
            title_a = item.select_one('.module-card-item-title a')
            title = title_a.text.strip() if title_a else ''
            
            img_elem = item.select_one('.module-item-pic img')
            pic = ''
            if img_elem:
                pic = img_elem.get('data-original') or img_elem.get('src', '')
            
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

    def playerContent(self, flag, id, vipFlags):
        try:
            play_link = id if id.startswith('http') else self.url + id
            res = requests.get(play_link, headers=self.headers, timeout=10)
            html = res.text

            match = re.search(r'var player_aaaa\s*=\s*(\{.*?\})<', html)
            play_url = ''

            if match:
                try:
                    player = json.loads(match.group(1))
                    play_url = player.get('url', '')
                except:
                    pass

            if not play_url:
                return {'parse': 1, 'jx': 1, 'url': play_link}

            play_url = play_url.replace('\\/', '/').replace('\\\\', '\\')

            if '.m3u8' in play_url or '.mp4' in play_url:
                return {
                    'parse': 0,
                    'jx': 0,
                    'url': play_url,
                    'header': {
                        'Referer': self.url,
                        'User-Agent': self.UA
                    }
                }

            try:
                svip_url = 'https://svip.qlplayer.cyou/?url=' + urllib.parse.quote(play_url)
                svip_headers = self.headers.copy()
                svip_headers['Referer'] = self.url
                
                svip_html = requests.get(svip_url, headers=svip_headers, timeout=10).text
                token_match = re.search(r'apiToken:\s*"([^"]+)"', svip_html)

                if token_match:
                    token = token_match.group(1)
                    api_url = 'https://svip.qlplayer.cyou/api/resolve.php?token=' + urllib.parse.quote(token)
                    
                    api_headers = self.headers.copy()
                    api_headers.update({
                        'Referer': 'https://svip.qlplayer.cyou/',
                        'Origin': 'https://svip.qlplayer.cyou',
                        'Accept': 'application/json, text/plain, */*'
                    })
                    
                    api_res_str = requests.get(api_url, headers=api_headers, timeout=10).text
                    data = json.loads(api_res_str or '{}')

                    if data.get('code') == 200 and data.get('url'):
                        return {
                            'parse': 0,
                            'jx': 0,
                            'url': data['url'],
                            'header': {
                                'Referer': 'https://svip.qlplayer.cyou/',
                                'User-Agent': self.UA
                            }
                        }
            except Exception:
                pass

            return {'parse': 1, 'jx': 1, 'url': play_url}
        except Exception:
            return {'parse': 1, 'jx': 1, 'url': id}
