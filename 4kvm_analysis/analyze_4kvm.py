#!/usr/bin/env python3
"""
分析 4kvm.tv 网站的视频生成和解密逻辑
完整的流程演示脚本
"""

import requests
import re
import json
import base64
import time
from bs4 import BeautifulSoup


class Analyzer4KVM:
    def __init__(self):
        self.base_url = "https://www.4kvm.tv"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        })

    def get_page_content(self, play_url):
        """获取播放页面内容"""
        print(f"正在获取页面: {play_url}")
        res = self.session.get(play_url)
        res.raise_for_status()
        return res.text

    def extract_page_info(self, html_content):
        """从页面提取必要信息"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取 meta 标签
        nb_st = soup.find('meta', {'id': 'nb-st'})
        nb_st_content = nb_st.get('content', '') if nb_st else ''
        
        # 提取 _pdf 变量
        pdf_match = re.search(r'window\._pdf\s*=\s*"([^"]+)"', html_content)
        pdf_value = pdf_match.group(1) if pdf_match else ''
        
        # 查找 episode 信息
        episode_link = soup.find('a', class_='episode-link')
        dataid = episode_link.get('dataid') if episode_link else ''
        
        # 查找 vodid
        vodid_match = re.search(r'var vodid\s*=\s*\'([^\']+)\'', html_content)
        vodid = vodid_match.group(1) if vodid_match else ''
        
        return {
            'nb_st': nb_st_content,
            'pdf': pdf_value,
            'dataid': dataid,
            'vodid': vodid
        }

    def decode_pdf(self, pdf_value):
        """解码 pdf 变量，获取 CDN 主机列表"""
        try:
            decoded = base64.b64decode(pdf_value).decode('utf-8')
            return json.loads(decoded)
        except Exception as e:
            print(f"解码 pdf 失败: {e}")
            return []

    def get_video_info(self, play_url):
        """完整流程：获取视频播放 URL"""
        print("="*60)
        print("开始分析")
        print("="*60)
        
        # 第一步：获取播放页面
        html = self.get_page_content(play_url)
        page_info = self.extract_page_info(html)
        
        print("\n提取到的页面信息:")
        print(f"  nb_st (timestamp): {page_info['nb_st']}")
        print(f"  pdf: {page_info['pdf'][:100]}...")
        print(f"  dataid: {page_info['dataid']}")
        print(f"  vodid: {page_info['vodid']}")
        
        # 解码 pdf 获取 CDN 主机
        cdn_hosts = self.decode_pdf(page_info['pdf'])
        print(f"\n可用的 CDN 主机: {cdn_hosts}")
        
        print("\n" + "="*60)
        print("注意：实际的 build_play_url 是在 WebAssembly 中实现的")
        print("="*60)
        print("\n为了完整功能，我们需要:")
        print("1. 使用 WebAssembly 模块调用 build_play_url 函数")
        print("2. 或者模拟请求的参数生成")
        print("\n这是一个基础分析脚本，完整实现需要:")
        print("- 分析 WASM 模块的逻辑")
        print("- 生成正确的签名参数")
        print("- 调用 /video/play 接口")
        print("- 解析返回的 m3u8 地址")


def main():
    # 示例视频 URL: 《飞驰人生3》
    test_url = "https://www.4kvm.tv/play/ch44vpwk4"
    
    analyzer = Analyzer4KVM()
    analyzer.get_video_info(test_url)


if __name__ == "__main__":
    main()
