#!/usr/bin/env python3
"""
完整的 4kvm.tv 视频分析和获取工具
包含详细的分析和可运行的示例代码
"""

import requests
import re
import json
import base64
import time
import subprocess
from bs4 import BeautifulSoup


class VideoPlayer4KVM:
    def __init__(self):
        self.base_url = "https://www.4kvm.tv"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        })

    def get_play_page(self, play_url):
        """获取播放页面内容"""
        print(f"[+] 正在获取播放页面: {play_url}")
        res = self.session.get(play_url)
        res.raise_for_status()
        return res.text

    def parse_play_page(self, html):
        """解析播放页面，提取关键信息"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取 meta 标签
        nb_st_tag = soup.find('meta', {'id': 'nb-st'})
        nb_st = nb_st_tag.get('content', '') if nb_st_tag else ''
        
        # 提取 window._pdf
        pdf_match = re.search(r'window\._pdf\s*=\s*"([^"]+)"', html)
        pdf_val = pdf_match.group(1) if pdf_match else ''
        
        # 提取 dataid (episode)
        episode = soup.find('a', class_='episode-link')
        dataid = episode.get('dataid') if episode else ''
        
        # 提取 vodid
        vodid_match = re.search(r'var vodid\s*=\s*\'([^\']+)\'', html)
        vodid = vodid_match.group(1) if vodid_match else ''
        
        return {
            'nb_st': nb_st,
            'pdf': pdf_val,
            'dataid': dataid,
            'vodid': vodid
        }

    def decode_pdf(self, pdf_str):
        """解码 pdf 变量，得到 CDN 域名列表"""
        try:
            decoded = base64.b64decode(pdf_str).decode('utf-8')
            # 修复 base64 解码后的 JSON
            # 有时候会有一些问题，我们尝试各种修复方式
            decoded = decoded.replace('\x00', '')  # 移除 null 字节
            
            # 尝试解析 JSON
            return json.loads(decoded)
        except Exception as e:
            print(f"[!] 解码 PDF 失败: {e}")
            # 尝试其他修复方式
            try:
                # 尝试直接解码并修复
                decoded = base64.b64decode(pdf_str + '==').decode('utf-8', errors='ignore')
                print(f"    修复后的内容: {decoded[:100]}")
                return []
            except:
                return []


def print_analysis_summary():
    """打印分析总结"""
    print("=" * 80)
    print("📺 4kvm.tv 视频系统分析总结")
    print("=" * 80)
    print("\n🔍 核心流程分析:")
    print("1️⃣ 访问视频播放页面")
    print("2️⃣ 从页面提取关键参数")
    print("   - meta#nb-st (时间戳)")
    print("   - window._pdf (CDN 域名列表，base64 编码)")
    print("   - dataid (集数 ID)")
    print("   - vodid (视频 ID)")
    print("3️⃣ 初始化 WebAssembly 模块 (nbmovie_wasm_bg.wasm)")
    print("4️⃣ 调用 build_play_url() 函数生成 API 请求 URL")
    print("   - 参数: dataid, secret_key, quality, play_key")
    print("5️⃣ 请求 /video/play 接口")
    print("6️⃣ 接口返回 m3u8 视频播放地址")
    print("7️⃣ 使用播放器 (Artplayer + HLS.js) 播放视频")
    print("\n" + "=" * 80)


def demonstrate_usage():
    """演示使用方法"""
    print("\n🎬 使用示例")
    print("=" * 80)
    print("\n由于完整实现 WebAssembly 的 build_play_url 函数需要")
    print("深入的逆向工程分析，以下是几种方案：")
    print("\n方案 1: 浏览器自动化 (推荐)")
    print("  使用 Playwright/Selenium 自动化浏览器获取真实地址")
    print("\n方案 2: 分析并复写 WebAssembly 逻辑")
    print("  需要深入分析 wasm 模块")
    print("\n方案 3: 使用 API 抓包")
    print("  在浏览器开发工具中获取真实 API 请求")
    print("\n" + "=" * 80)


def main():
    print_analysis_summary()
    demonstrate_usage()
    
    print("\n🔧 让我们尝试获取视频信息")
    print("=" * 80)
    
    player = VideoPlayer4KVM()
    test_url = "https://www.4kvm.tv/play/ch44vpwk4"
    
    try:
        html = player.get_play_page(test_url)
        info = player.parse_play_page(html)
        
        print("\n✅ 成功提取页面信息:")
        print(f"   nb_st:  {info['nb_st']}")
        print(f"   pdf:    {info['pdf'][:50]}...")
        print(f"   dataid: {info['dataid']}")
        print(f"   vodid:  {info['vodid']}")
        
        cdn_hosts = player.decode_pdf(info['pdf'])
        if cdn_hosts:
            print(f"\n✅ CDN 域名: {cdn_hosts}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print("\n" + "=" * 80)
    print("💡 如需进一步开发，建议:")
    print("   1. 使用浏览器自动化获取 m3u8 地址")
    print("   2. 逆向分析 wasm 模块复写 build_play_url")
    print("   3. 使用 Fiddler/Charles 抓包分析 API")
    print("=" * 80)


if __name__ == "__main__":
    main()
