
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


def test_category(tid, name):
    print(f"\n=== 测试分类: {name} (ID: {tid}) ===")
    
    # 尝试不同的URL结构
    test_urls = [
        f"{url}/vodshow/{tid}-------1---.html",
        f"{url}/vodtype/{tid}.html",
        f"{url}/list/{tid}.html",
    ]
    
    for test_url in test_urls:
        print(f"\n尝试URL: {test_url}")
        try:
            res = requests.get(test_url, headers=headers, timeout=10)
            print(f"状态码: {res.status_code}")
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # 尝试多种选择器
                selectors_to_test = [
                    '.module-poster-item',
                    '.module-card-item',
                    '.module-items a',
                    '.item',
                    '.video-item',
                ]
                
                for selector in selectors_to_test:
                    items = soup.select(selector)
                    print(f"选择器 '{selector}' 找到 {len(items)} 个项")
                    if items and len(items) > 0:
                        print(f"前3个项预览:")
                        for i, item in enumerate(items[:3]):
                            print(f"  项{i}: {str(item)[:200]}")
                        break
                
                # 保存HTML
                with open(f'/workspace/category_debug_{tid}.html', 'w', encoding='utf-8') as f:
                    f.write(res.text)
                print(f"\n保存页面到 /workspace/category_debug_{tid}.html")
                break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    test_categories = [
        (20, '电影'),
        (37, '电视剧'),
        (45, '综艺'),
    ]
    
    for tid, name in test_categories:
        test_category(tid, name)
