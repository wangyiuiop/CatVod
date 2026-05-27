
# coding=utf-8
import requests
from bs4 import BeautifulSoup

url = 'https://www.4kmovie.top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Referer': url,
}

# 测试分页格式
test_urls = [
    (f"{url}/vodtype/20-2.html", "vodtype/20-2"),
    (f"{url}/vodtype/20--2.html", "vodtype/20--2"),
    (f"{url}/vodshow/20------2---.html", "vodshow/20------2---"),
]

print("测试分页URL格式：\n")

for test_url, name in test_urls:
    print(f"测试: {name}")
    print(f"URL: {test_url}")
    try:
        res = requests.get(test_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('.module-poster-item')
        print(f"找到 {len(items)} 个视频")
        
        if items:
            # 获取第一个视频的标题
            first_title = items[0].get('title', '未知')
            print(f"第1个视频: {first_title}")
        print()
    except Exception as e:
        print(f"错误: {e}\n")
