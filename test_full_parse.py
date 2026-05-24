#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试 - 模拟完整的POST请求获取视频地址
"""
import requests
import re
import json
import base64
import urllib.parse
import time
import random

BASE_URL = "https://www.lmm85.com"
API_URL = "https://yun.92cj.com/acfun58.php"

# 模拟浏览器请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': API_URL,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
}

def get(url, headers=None):
    """发送GET请求"""
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(1, 2))
    return requests.get(url, headers=req_headers, timeout=15, allow_redirects=True)

def post(url, data, headers=None):
    """发送POST请求"""
    req_headers = HEADERS.copy()
    if headers:
        req_headers.update(headers)
    time.sleep(random.uniform(1, 2))
    return requests.post(url, data=data, headers=req_headers, timeout=15)

def test_full_parse():
    """完整解析测试"""
    print("="*70)
    print("路漫漫动漫 - 完整解析测试")
    print("="*70)
    
    # 1. 第一步: 获取播放页面和API参数
    play_url = "/play/5823_1_1.html"
    api_id = "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14=&t=DU"
    referer = f"{BASE_URL}{play_url}"
    
    print(f"\n1️⃣  获取API页面...")
    api_url = f"{API_URL}?id={urllib.parse.quote(api_id)}&referer={urllib.parse.quote(referer)}"
    response = get(api_url, headers={'Referer': referer})
    
    # 2. 第二步: 从API页面提取POST参数
    print(f"\n2️⃣  提取POST参数...")
    
    # 提取参数
    html = response.text
    
    # 使用正则提取 $.post 中的参数
    post_pattern = r'\$\.post\(""\s*,\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*,'
    post_match = re.search(post_pattern, html, re.S)
    
    if not post_match:
        print("❌ 未找到POST参数")
        return
    
    post_data_str = post_match.group(1)
    
    # 转换为Python dict
    # 先简单替换一下引号使其合法
    post_data_str = re.sub(r'\s*:\s*', ':', post_data_str)
    post_data_str = re.sub(r',\s*', ',', post_data_str)
    post_data_str = re.sub(r'(\w+):', r'"\1":', post_data_str)
    
    print(f"\n📝 POST数据 (raw):")
    print(post_data_str)
    
    try:
        # 尝试直接解析 (可能会失败，因为有单引号等)
        # 用更安全的方式提取
        params = {}
        
        # 提取各个字段
        vid_match = re.search(r'"vid":"([^"]+)"', post_data_str)
        type_match = re.search(r'"type":"([^"]+)"', post_data_str)
        sing_match = re.search(r'"sing":"([^"]+)"', post_data_str)
        token_match = re.search(r'"token":"([^"]+)"', post_data_str)
        t_match = re.search(r'"t":"([^"]+)"', post_data_str)
        ti_match = re.search(r'"ti":(\d+)', post_data_str)
        
        if vid_match:
            params['vid'] = vid_match.group(1).replace(' ', '+')
        if type_match:
            params['type'] = type_match.group(1)
        if sing_match:
            params['sing'] = sing_match.group(1)
        if token_match:
            params['token'] = token_match.group(1)
        if t_match:
            params['t'] = t_match.group(1)
        if ti_match:
            params['ti'] = ti_match.group(1)
        
        print(f"\n📊 提取的参数:")
        for k, v in params.items():
            print(f"  {k}: {v}")
        
        # 3. 第三步: 发送POST请求
        print(f"\n3️⃣  发送POST请求...")
        final_response = post(API_URL, params, headers={'Referer': api_url})
        
        print(f"状态码: {final_response.status_code}")
        
        # 保存响应
        with open('debug_final_response.json', 'w', encoding='utf-8') as f:
            f.write(final_response.text)
        print("已保存到: debug_final_response.json")
        
        # 4. 第四步: 解析响应
        print(f"\n4️⃣  解析响应...")
        
        try:
            data = json.loads(final_response.text)
            print(f"\n✅ 响应JSON:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            if data.get('msg') == 200:
                print(f"\n🎉 成功!")
                
                url = data.get('url', '')
                ext = data.get('ext', '')
                
                print(f"\n📽️  播放信息:")
                print(f"  URL: {url}")
                print(f"  ext: {ext}")
                print(f"  site: {data.get('site', '')}")
                
                # 处理不同类型的ext
                if ext == 'hls' or ext == 'hls_list':
                    try:
                        real_url = urllib.parse.unquote(url)
                        print(f"\n🎥 m3u8地址: {real_url}")
                    except:
                        print(f"\n🎥 URL: {url}")
                elif ext == 'link' or ext == 'mp4':
                    print(f"\n🎥 直接地址: {url}")
                else:
                    print(f"\n⚠️  需要进一步处理的类型: {ext}")
            else:
                print(f"\n❌ 失败: {data}")
                
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print(f"\n响应内容:")
            print(final_response.text)
            
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        print(f"堆栈: {traceback.format_exc()}")
    
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)

if __name__ == "__main__":
    test_full_parse()
