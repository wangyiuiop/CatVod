#!/usr/bin/env python3
"""
WebAssembly build_play_url 逆向分析
分析 nbmovie_wasm_bg.wasm 模块并尝试复现逻辑
"""

import requests
import re
import json
import base64
import time
import hashlib
import hmac
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup

BASE_URL = "https://www.4kvm.tv"


class WasmAnalyzer:
    """WebAssembly 分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        })
        self.cdn_hosts = []
        self.dataid = ""
        self.secret_key = ""
        self.quality = "1080"
        self.play_key = ""
        
    def get_play_page(self, play_url):
        """获取播放页面并提取所有信息"""
        print(f"[+] 获取播放页面: {play_url}")
        res = self.session.get(play_url)
        html = res.text
        
        # 提取 _pdf
        pdf_match = re.search(r'window\._pdf\s*=\s*"([^"]+)"', html)
        if pdf_match:
            pdf_b64 = pdf_match.group(1)
            self.cdn_hosts = json.loads(base64.b64decode(pdf_b64).decode('utf-8'))
            print(f"[+] CDN 主机: {self.cdn_hosts}")
        
        # 提取 dataid
        dataid_match = re.search(r'dataid="([^"]+)"', html)
        if dataid_match:
            self.dataid = dataid_match.group(1)
            print(f"[+] DataID: {self.dataid}")
        
        # 提取 meta#nb-st
        soup = BeautifulSoup(html, 'html.parser')
        nb_st = soup.find('meta', {'id': 'nb-st'})
        if nb_st:
            nb_st_val = nb_st.get('content', '')
            print(f"[+] nb_st: {nb_st_val}")
        
        return html
    
    def analyze_wasm(self):
        """分析 WASM 模块特征"""
        print("\n[+] 开始分析 WASM 模块...")
        
        # 下载 WASM 文件
        wasm_url = f"{BASE_URL}/static/wasm/nbmovie_wasm_bg.d5d51939.wasm"
        print(f"[+] 下载 WASM: {wasm_url}")
        
        try:
            res = self.session.get(wasm_url)
            wasm_data = res.content
            print(f"[+] WASM 大小: {len(wasm_data)} bytes")
            
            # 分析 WASM 文件
            self.analyze_wasm_structure(wasm_data)
            
        except Exception as e:
            print(f"[-] 下载 WASM 失败: {e}")
    
    def analyze_wasm_structure(self, wasm_data):
        """分析 WASM 二进制结构"""
        print("\n[WASM 结构分析]")
        
        # 头部魔数
        magic = wasm_data[:4]
        version = wasm_data[4:8]
        print(f"  Magic: {magic.hex()}")
        print(f"  Version: {int.from_bytes(version, 'little')}")
        
        # 搜索关键字符串
        wasm_str = wasm_data.decode('latin-1', errors='ignore')
        
        # 查找可能的函数名
        patterns = [
            b'build_play_url',
            b'play_url',
            b'video',
            b'encrypt',
            b'decrypt',
            b'hash',
            b'md5',
            b'sha',
        ]
        
        print("\n[字符串分析]")
        for pattern in patterns:
            if pattern in wasm_data:
                idx = wasm_data.find(pattern)
                context = wasm_data[max(0, idx-20):idx+len(pattern)+20]
                print(f"  找到 '{pattern.decode()}': 位置 {idx}")
        
        # 分析可能的算法
        print("\n[算法分析]")
        
        # 检查是否包含加密相关的操作码
        crypto_indicators = {
            'XOR': b'\x73',  # i32.xor
            'AND': b'\x71',  # i32.and
            'OR': b'\x72',   # i32.or
            'ROT': b'\x79',  # i32.rotr
        }
        
        for name, opcode in crypto_indicators.items():
            count = wasm_data.count(opcode)
            print(f"  {name}: {count} 次")
        
        # 检查时间相关函数
        if b'Date' in wasm_data or b'date' in wasm_data:
            print("  [+] 检测到 Date 相关函数")
        
        # 检查随机数
        if b'random' in wasm_data.lower() or b'math' in wasm_data.lower():
            print("  [+] 检测到 Math/Random 相关函数")
        
        return wasm_data


class PlayUrlBuilder:
    """构建播放 URL"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.base_url = f"{BASE_URL}/video/play"
        
    def generate_signature(self, *args):
        """
        尝试生成签名
        基于观察到的参数格式
        """
        # 从之前的网络抓包中我们知道：
        # /video/play?p=33752&v=ch44vpwk4&q=1080&s=0b5c8e777e5c40cfc5761dc9e2a0684c&t=1779201337428&k=NlM7DiACN1ZlY1c3JARGI3cMBk4nNwEJLjwVUA==
        
        # 参数说明：
        # p = pid (页面ID?)
        # v = vodid/play id
        # q = quality (1080)
        # s = 某种签名/校验和
        # t = timestamp (时间戳)
        # k = 加密后的key
        
        timestamp = str(int(time.time() * 1000))
        
        return {
            'p': '33752',  # 可能需要从页面提取
            'v': self.analyzer.dataid,
            'q': self.analyzer.quality,
            't': timestamp,
        }
    
    def build_url_v1(self):
        """构建 URL - 方案1: 直接拼接"""
        params = self.generate_signature()
        query = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.base_url}?{query}"
    
    def test_url_patterns(self):
        """测试不同的 URL 模式"""
        print("\n[+] 测试 URL 模式...")
        
        patterns = [
            # 模式1: 基础参数
            f"{self.base_url}?p=33752&v={self.analyzer.dataid}&q=1080",
            # 模式2: 加上时间戳
            f"{self.base_url}?p=33752&v={self.analyzer.dataid}&q=1080&t={int(time.time()*1000)}",
            # 模式3: 完整的URL
            f"{self.base_url}?p=33752&v={self.analyzer.dataid}&q=1080&s=0b5c8e777e5c40cfc5761dc9e2a0684c&t=1779201337428&k=NlM7DiACN1ZlY1c3JARGI3cMBk4nNwEJLjwVUA==",
        ]
        
        for i, url in enumerate(patterns, 1):
            print(f"\n模式 {i}:")
            print(f"  {url[:100]}...")
        
        return patterns


def extract_page_params(html):
    """从页面提取所有可能的参数"""
    print("\n[+] 提取页面参数...")
    
    params = {}
    
    # 提取 dataid
    dataid_match = re.search(r'dataid="([^"]+)"', html)
    if dataid_match:
        params['dataid'] = dataid_match.group(1)
    
    # 提取 vodid
    vodid_match = re.search(r'var\s+vodid\s*=\s*["\']([^"\']+)["\']', html)
    if vodid_match:
        params['vodid'] = vodid_match.group(1)
    
    # 提取 meta 信息
    soup = BeautifulSoup(html, 'html.parser')
    for meta in soup.find_all('meta'):
        name = meta.get('name', '') or meta.get('property', '')
        if name:
            params[f'meta_{name}'] = meta.get('content', '')
    
    # 提取脚本中的变量
    script_vars = re.findall(r'var\s+(\w+)\s*=\s*["\']([^"\']+)["\']', html)
    for var_name, var_val in script_vars:
        params[var_name] = var_val
    
    # 提取所有可能的ID
    ids = re.findall(r'id="([^"]+)"', html)
    params['ids'] = ids[:20]  # 取前20个
    
    print(f"  找到 {len(params)} 个参数")
    for k, v in list(params.items())[:10]:
        print(f"    {k}: {str(v)[:50]}")
    
    return params


def main():
    print("="*70)
    print("4kvm.tv WASM 逆向分析工具")
    print("="*70)
    
    analyzer = WasmAnalyzer()
    
    # 获取播放页面
    test_url = "https://www.4kvm.tv/play/ch44vpwk4"
    html = analyzer.get_play_page(test_url)
    
    # 提取参数
    params = extract_page_params(html)
    
    # 分析 WASM
    analyzer.analyze_wasm()
    
    # 构建 URL
    builder = PlayUrlBuilder(analyzer)
    patterns = builder.test_url_patterns()
    
    print("\n" + "="*70)
    print("分析总结")
    print("="*70)
    print("\n根据逆向分析，build_play_url 函数可能的实现逻辑：")
    print("\n1. 接收参数:")
    print("   - dataid: 从页面提取的集数ID")
    print("   - secret_key: 预定义的密钥或从页面提取")
    print("   - quality: 视频质量 (720/1080/4k)")
    print("   - play_key: 某种加密key")
    print("\n2. 处理流程:")
    print("   - 使用 timestamp 作为时间参数")
    print("   - 计算某种签名/校验和")
    print("   - 拼接完整的 API URL")
    print("\n3. 返回格式:")
    print("   /video/play?p=xxx&v=xxx&q=xxx&s=xxx&t=xxx&k=xxx")
    print("\n[+] 由于 WASM 是编译后的二进制代码，精确逆向需要:")
    print("    1. 反编译 WASM 为 WASM Text Format")
    print("    2. 分析字节码逻辑")
    print("    3. 用 Python 重写相同算法")
    print("\n[+] 建议方案:")
    print("    1. 使用 Python 的 wasmtime 或 pywasm 库加载 WASM")
    print("    2. 直接调用编译后的 build_play_url 函数")
    print("    3. 获取返回的 URL")


if __name__ == "__main__":
    main()
