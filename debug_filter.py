
# coding=utf-8
import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup


url = 'https://www.4kmovie.top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Referer': url,
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'Accept': '*/*'
}


def test_filter(tid, name, filters=None):
    print(f"\n=== 测试筛选: {name} (ID: {tid}) ===")
    
    if filters is None:
        filters = {}
    
    # 尝试不同的URL结构
    test_urls = []
    
    # 1. vodshow格式（带筛选条件）
    area = filters.get('area', '')
    by = filters.get('by', 'time')
    cls = filters.get('class', '')
    lang = filters.get('lang', '')
    letter = filters.get('letter', '')
    year = filters.get('year', '')
    pg = filters.get('pg', '1')
    
    test_urls.append({
        'name': 'vodshow带筛选',
        'url': f"{url}/vodshow/{tid}-{area}-{by}-{cls}-{lang}-{letter}---{pg}---{year}.html"
    })
    
    # 2. vodtype格式（不同分页）
    if pg == '1':
        test_urls.append({
            'name': 'vodtype第1页',
            'url': f"{url}/vodtype/{tid}.html"
        })
    else:
        test_urls.append({
            'name': 'vodtype分页',
            'url': f"{url}/vodtype/{tid}-{pg}.html"
        })
    
    # 3. 可能的其他格式
    test_urls.append({
        'name': 'vodtype带筛选',
        'url': f"{url}/vodtype/{tid}-{cls}-{area}-{lang}-{year}-{letter}-{by}-{pg}.html"
    })
    
    for test_info in test_urls:
        test_url = test_info['url']
        print(f"\n尝试: {test_info['name']}")
        print(f"URL: {test_url}")
        
        try:
            res = requests.get(test_url, headers=headers, timeout=10)
            print(f"状态码: {res.status_code}")
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # 统计视频数量
                items = soup.select('.module-poster-item')
                print(f"找到 {len(items)} 个视频")
                
                if items and len(items) > 0:
                    # 保存第一个URL的成功结果
                    with open(f'/workspace/filter_debug_{tid}.html', 'w', encoding='utf-8') as f:
                        f.write(res.text)
                    print(f"保存页面到 /workspace/filter_debug_{tid}.html")
                    
                    print("前3个视频:")
                    for i, item in enumerate(items[:3]):
                        title = item.get('title', '')
                        note = item.select_one('.module-item-note')
                        note_text = note.text.strip() if note else ''
                        print(f"  {i+1}. {title} ({note_text})")
                    
                    # 返回这个URL
                    return test_info['name'], test_url
        except Exception as e:
            print(f"错误: {e}")
    
    return None, None


if __name__ == "__main__":
    print("=== 测试筛选功能 ===")
    
    # 测试1：电影分类，不带筛选
    test_filter(20, '电影', {})
    
    # 测试2：电影分类，按地区筛选
    test_filter(20, '电影-美国', {'area': '美国'})
    
    # 测试3：电影分类，按年份筛选
    test_filter(20, '电影-2024', {'year': '2024'})
    
    # 测试4：电影分类，按剧情类型筛选
    test_filter(20, '电影-喜剧', {'class': '喜剧'})
    
    # 测试5：电视剧分类，按地区筛选
    test_filter(37, '电视剧-内地', {'area': '内地'})
