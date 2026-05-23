#!/usr/bin/env python3
import re
import urllib.request
import urllib.parse
import json

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1'

def fetch_page(url):
    """获取页面内容"""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"获取页面失败: {e}")
        return None

def parse_list(html):
    """解析列表页"""
    items = []
    pattern = r'<li><a href="/vod-detail-id-(\d+)\.html" title="([^"]+)">[\s\S]*?data-echo="([^"]+)"[\s\S]*?<span class="sTit">([^<]+)</span>[\s\S]*?<span class="sDes">([^<]+)</span>'
    
    matches = re.findall(pattern, html)
    for match in matches:
        items.append({
            'id': match[0],
            'title': match[1],
            'pic': match[2],
            'name': match[3],
            'des': match[4]
        })
    
    return items

def parse_detail(html):
    """解析详情页"""
    result = {}
    
    title_match = re.search(r'<h1 class="title"><a href="[^"]*" title="([^"]+)">', html)
    if title_match:
        result['title'] = title_match.group(1)
    
    pic_match = re.search(r'<section class="page-hd"><a href="[^"]*" title="[^"]*"><img src="([^"]+)"', html)
    if pic_match:
        result['pic'] = pic_match.group(1)
    
    actor_match = re.search(r'主演:&nbsp;<\/span>(?:<[^>]*>)*([^<&\s]+(?:<[^>]*>[^<]*</[^>]*>)*[^<]*)', html)
    if not actor_match:
        temp_html = re.sub(r'<a[^>]*>', '', html)
        temp_html = re.sub(r'</a>', '', temp_html)
        actor_match = re.search(r'主演:&nbsp;</span>([^<]+)', temp_html)
    if actor_match:
        result['actor'] = actor_match.group(1).strip()
    
    director_match = re.search(r'导演:&nbsp;</span>(?:<[^>]*>)*([^<&]*)', html)
    if director_match:
        director_text = director_match.group(1).strip()
        if director_text and director_text != '</a>':
            result['director'] = director_text
        else:
            result['director'] = '未知'
    else:
        result['director'] = '未知'
    
    year_match = re.search(r'年代:&nbsp;</span><a[^>]*>([^<]+)</a>', html)
    if year_match:
        result['year'] = year_match.group(1)
    
    desc_match = re.search(r'简[\s&nbsp;]+介：([^<]+)</p>', html)
    if desc_match:
        result['content'] = desc_match.group(1).strip()
    
    play_list = []
    play_pattern = r'<a href="/vod-play-id-\d+-src-\d+-num-\d+\.html"[^>]*>([^<]+)</a>'
    play_matches = re.findall(play_pattern, html)
    result['playList'] = [p.strip() for p in play_matches]
    
    return result

def get_categories():
    """获取分类列表"""
    return [
        {'type_id': '1', 'type_name': '电影'},
        {'type_id': '2', 'type_name': '连续剧'},
        {'type_id': '3', 'type_name': '综艺'},
        {'type_id': '4', 'type_name': '动漫'},
        {'type_id': '26', 'type_name': '短剧'},
        {'type_id': '20', 'type_name': '小姐姐'},
        {'type_id': '31', 'type_name': '音乐'}
    ]

def get_category_url(type_id, page=1, order='time'):
    """生成分类URL"""
    order_map = {'time': 'time', 'hits': 'hits', 'score': 'score'}
    order_by = order_map.get(order, 'time')
    return f'/index.php?m=vod-list-id-{type_id}-pg-{page}-order--by-{order_by}-class-0-year-0-letter--area--lang-.html'

def get_detail_url(id):
    """生成详情页URL"""
    return f'/vod-detail-id-{id}.html'

def get_search_url(keyword):
    """生成搜索URL"""
    encoded_keyword = urllib.parse.quote(keyword)
    return f'/index.php?m=vod-search&wd={encoded_keyword}'

def get_play_url(id, src=1, num=1):
    """生成播放页URL"""
    return f'/vod-play-id-{id}-src-{src}-num-{num}.html'

if __name__ == '__main__':
    print("=== 旺旺影视爬虫测试 ===\n")
    
    BASE_URL = 'https://vip.wwgz.cn:5200'
    
    print("1. 分类列表:")
    categories = get_categories()
    for cat in categories:
        print(f"   [{cat['type_id']}] {cat['type_name']}")
    
    print("\n2. URL生成测试:")
    print(f"   电影第1页: {get_category_url('1', 1)}")
    print(f"   电视剧第5页: {get_category_url('2', 5)}")
    print(f"   搜索'东北往事': {get_search_url('东北往事')}")
    print(f"   详情页90063: {get_detail_url('90063')}")
    
    print("\n3. 测试获取电影分类第1页...")
    url = BASE_URL + get_category_url('1', 1)
    html = fetch_page(url)
    
    if html:
        items = parse_list(html)
        print(f"   成功! 解析到 {len(items)} 条数据\n")
        
        if items:
            print("   示例数据(前3条):")
            for i, item in enumerate(items[:3], 1):
                print(f"\n   [{i}] {item['title']}")
                print(f"       图片: {item['pic'][:60]}...")
                print(f"       描述: {item['des']}")
    else:
        print("   获取失败")
    
    print("\n4. 测试获取详情页...")
    url = BASE_URL + get_detail_url('90063')
    html = fetch_page(url)
    
    if html:
        detail = parse_detail(html)
        print(f"   成功解析详情!\n")
        print(f"   标题: {detail.get('title', 'N/A')}")
        print(f"   图片: {detail.get('pic', 'N/A')[:60]}...")
        print(f"   主演: {detail.get('actor', 'N/A')}")
        print(f"   导演: {detail.get('director', 'N/A')}")
        print(f"   年代: {detail.get('year', 'N/A')}")
        print(f"   简介: {detail.get('content', 'N/A')[:100]}...")
        print(f"   播放列表: {detail.get('playList', [])[:5]}...")
    else:
        print("   获取失败")
    
    print("\n=== 测试完成 ===")
