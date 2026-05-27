
# coding=utf-8
import re
import json
from bs4 import BeautifulSoup

with open('/workspace/search_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
items = soup.select('.module-card-item')

print(f"Found {len(items)} .module-card-item items")
print()

for i, item in enumerate(items):
    print(f"=== Item {i+1} ===")
    print(f"HTML snippet: {str(item)[:500]}")
    print()
    
    # 查找海报链接
    poster = item.select_one('.module-card-item-poster')
    if poster:
        print(f"Poster href: {poster.get('href')}")
        
    # 查找图片
    img = item.select_one('.module-item-pic img')
    if img:
        print(f"Image tag found")
        print(f"  data-original: {img.get('data-original')}")
        print(f"  src: {img.get('src')}")
    else:
        print(f"Looking for images in other places...")
        all_imgs = item.find_all('img')
        for img in all_imgs:
            print(f"  Image found: src={img.get('src')}, data-original={img.get('data-original')}")
            
    # 查找标题
    title_a = item.select_one('.module-card-item-title a')
    if title_a:
        print(f"Title A found: {title_a.text.strip()}")
    else:
        print(f"Looking for titles...")
        all_a = item.find_all('a')
        for a in all_a:
            if a.text.strip():
                print(f"  Link: {a.text.strip()}, href={a.get('href')}")
                
    # 查找备注
    note = item.select_one('.module-item-note')
    if note:
        print(f"Note found: {note.text.strip()}")
        
    print()
