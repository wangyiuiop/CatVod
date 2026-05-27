
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

# 测试搜索功能
search_key = '良陈美锦'
search_url = f"{url}/vodsearch/{urllib.parse.quote(search_key)}----------1---.html"

print(f"Testing search URL: {search_url}")
print()

try:
    res = requests.get(search_url, headers=headers, timeout=10)
    print(f"Response status: {res.status_code}")
    print(f"Response headers: {dict(res.headers)}")
    print()
    
    # 保存HTML到文件以便检查
    with open('/workspace/search_page.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print("Saved search page to /workspace/search_page.html")
    print()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # 查找所有可能的选择器
    print("Testing different selectors:")
    
    # 1. 原代码的选择器
    items1 = soup.select('.module-card-item')
    print(f"  - .module-card-item: {len(items1)} items found")
    
    # 2. 查找所有带有 module-poster-item 类的元素（和首页相同）
    items2 = soup.select('.module-poster-item')
    print(f"  - .module-poster-item: {len(items2)} items found")
    
    # 3. 查找所有 module-items 容器
    module_items = soup.select('.module-items')
    print(f"  - .module-items: {len(module_items)}")
    
    if module_items:
        # 查看第一个module-items内部结构
        print(f"  - First module-items contents: {str(module_items[0].contents)[:200]}")
    
    # 4. 查找所有a标签
    all_links = soup.find_all('a')
    print(f"  - Total &lt;a&gt; tags: {len(all_links)}")
    
    # 5. 保存完整的HTML结构以便分析
    with open('/workspace/search_page_structure.txt', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print()
    print("Saved pretty-printed search page to /workspace/search_page_structure.txt")
    
except Exception as e:
    print(f"Error: {e}")
