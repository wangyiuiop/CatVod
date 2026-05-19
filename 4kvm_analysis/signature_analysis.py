#!/usr/bin/env python3
"""
签名算法逆向分析工具
分析 /video/play API 的签名生成逻辑
"""

import requests
import re
import json
import base64
import time
import hashlib
import hmac
from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup

BASE_URL = "https://www.4kvm.tv"


class SignatureAnalyzer:
    """签名分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        })
        
    def get_play_page(self, play_url):
        """获取播放页面"""
        print(f"[+] 获取页面: {play_url}")
        res = self.session.get(play_url)
        html = res.text
        
        # 提取 dataid
        dataid_match = re.search(r'dataid="([^"]+)"', html)
        self.dataid = dataid_match.group(1) if dataid_match else ""
        
        # 提取 vodid
        vodid_match = re.search(r'var\s+vodid\s*=\s*["\']([^"\']+)["\']', html)
        self.vodid = vodid_match.group(1) if vodid_match else ""
        
        # 提取 meta#nb-st
        soup = BeautifulSoup(html, 'html.parser')
        nb_st = soup.find('meta', {'id': 'nb-st'})
        self.timestamp = nb_st.get('content', '') if nb_st else str(int(time.time() * 1000))
        
        # 提取 _pdf
        pdf_match = re.search(r'window\._pdf\s*=\s*"([^"]+)"', html)
        if pdf_match:
            self.cdn_hosts = json.loads(base64.b64decode(pdf_match.group(1)).decode())
        
        print(f"  dataid: {self.dataid}")
        print(f"  vodid: {self.vodid}")
        print(f"  timestamp: {self.timestamp}")
        
        return html
    
    def decode_k_parameter(self, k_str):
        """解码 k 参数"""
        try:
            decoded = base64.b64decode(k_str).decode('utf-8')
            return decoded
        except:
            return k_str
    
    def analyze_signature_pattern(self):
        """
        分析签名模式
        基于已知参数尝试不同的组合
        """
        print("\n[+] 分析签名生成模式...")
        
        # 已知信息
        dataid = self.dataid
        vodid = self.vodid
        timestamp = self.timestamp
        quality = "1080"
        
        # 参数组合
        params_str = f"{dataid}{vodid}{quality}{timestamp}"
        print(f"\n参数组合测试:")
        print(f"  concat(dataid, vodid, quality, timestamp): {params_str}")
        
        # 尝试不同的哈希算法
        hash_algorithms = ['md5', 'sha1', 'sha256']
        
        for algo in hash_algorithms:
            if algo == 'md5':
                hash_result = hashlib.md5(params_str.encode()).hexdigest()
            elif algo == 'sha1':
                hash_result = hashlib.sha1(params_str.encode()).hexdigest()
            elif algo == 'sha256':
                hash_result = hashlib.sha256(params_str.encode()).hexdigest()
            
            print(f"  {algo}(params): {hash_result}")
        
        # 尝试带分隔符的组合
        params_str2 = f"{dataid}|{vodid}|{quality}|{timestamp}"
        md5_result = hashlib.md5(params_str2.encode()).hexdigest()
        print(f"\n  md5('{params_str2}'): {md5_result}")
        
        # 尝试不同的排序
        params_list = [dataid, vodid, quality, timestamp]
        params_sorted = ''.join(sorted(params_list))
        md5_sorted = hashlib.md5(params_sorted.encode()).hexdigest()
        print(f"  md5(sorted(params)): {md5_sorted}")
        
        return {
            'dataid': dataid,
            'vodid': vodid,
            'quality': quality,
            'timestamp': timestamp,
            'params_str': params_str
        }
    
    def test_api_call(self, params):
        """测试 API 调用"""
        print("\n[+] 测试 API 调用...")
        
        # 构建基础 URL
        base_api = f"{BASE_URL}/video/play"
        
        # 参数
        query_params = {
            'p': params['dataid'],
            'v': params['vodid'],
            'q': params['quality'],
            't': params['timestamp'],
        }
        
        # 添加签名
        params_str = params['params_str']
        signature = hashlib.md5(params_str.encode()).hexdigest()
        query_params['s'] = signature
        
        # 生成 k 参数 (base64编码的某个值)
        k_raw = f"{signature}:{params['timestamp']}"
        k_encoded = base64.b64encode(k_raw.encode()).decode()
        query_params['k'] = k_encoded
        
        # 构建完整 URL
        query_str = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        full_url = f"{base_api}?{query_str}"
        
        print(f"\n构建的 URL:")
        print(f"  {full_url}")
        
        # 尝试请求
        print(f"\n[+] 发送请求...")
        try:
            res = self.session.get(base_api, params=query_params, timeout=10)
            print(f"  状态码: {res.status_code}")
            print(f"  响应长度: {len(res.text)} bytes")
            
            if res.text:
                print(f"\n响应内容前200字符:")
                print(f"  {res.text[:200]}")
                
            return res
        except Exception as e:
            print(f"  请求失败: {e}")
            return None
    
    def reverse_engineer_k_param(self):
        """
        尝试理解 k 参数的生成方式
        """
        print("\n[+] 分析 k 参数...")
        
        # 已知的 k 值
        known_k = "NlM7DiACN1ZlY1c3JARGI3cMBk4nNwEJLjwVUA=="
        
        # 解码
        decoded_k = base64.b64decode(known_k).decode('utf-8', errors='ignore')
        print(f"  Base64 解码: {decoded_k}")
        print(f"  原始 bytes: {base64.b64decode(known_k).hex()}")
        
        # 尝试不同的解码方式
        for enc in ['utf-8', 'latin-1', 'utf-16']:
            try:
                decoded = base64.b64decode(known_k).decode(enc)
                print(f"  {enc} 解码: {decoded}")
            except:
                pass
        
        # 尝试不同的输入组合
        dataid = self.dataid
        vodid = self.vodid
        timestamp = "1779201337428"
        
        inputs = [
            f"{dataid}{vodid}{timestamp}",
            f"{dataid}|{vodid}|{timestamp}",
            f"{timestamp}{dataid}{vodid}",
            hashlib.md5(f"{dataid}{vodid}".encode()).hexdigest() + timestamp,
        ]
        
        print(f"\n可能的 k 输入:")
        for i, inp in enumerate(inputs, 1):
            k_test = base64.b64encode(inp.encode()).decode()
            print(f"  {i}. input='{inp}' -> k='{k_test}'")
        
        return known_k


def main():
    print("="*70)
    print("签名算法逆向分析")
    print("="*70)
    
    analyzer = SignatureAnalyzer()
    
    # 获取播放页面
    test_url = "https://www.4kvm.tv/play/ch44vpwk4"
    html = analyzer.get_play_page(test_url)
    
    # 分析签名模式
    params = analyzer.analyze_signature_pattern()
    
    # 分析 k 参数
    analyzer.reverse_engineer_k_param()
    
    # 测试 API 调用
    analyzer.test_api_call(params)
    
    print("\n" + "="*70)
    print("分析总结")
    print("="*70)
    print("\n[+] 关键发现:")
    print("    1. dataid, vodid, quality, timestamp 是基础参数")
    print("    2. s 参数可能是某种签名/校验和")
    print("    3. k 参数是 base64 编码的字符串")
    print("    4. 需要找到确切的算法才能生成正确的签名")
    print("\n[+] 下一步:")
    print("    1. 使用 wasmtime 库直接调用 WASM 模块")
    print("    2. 或者继续逆向 WASM 二进制代码")
    print("    3. 或者使用 JavaScript 引擎 (如 quickjs) 调用")


if __name__ == "__main__":
    main()
