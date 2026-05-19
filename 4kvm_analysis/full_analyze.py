#!/usr/bin/env python3
"""
深度分析 4kvm.tv 视频生成逻辑
"""

import re
import json
import base64
import requests


def analyze_js_file():
    """分析主要的 JS 文件，寻找相关函数"""
    with open("app.ultra.min.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    
    print("="*70)
    print("分析 app.ultra.min.js")
    print("="*70)
    
    # 查找所有包含函数定义的模式
    function_patterns = [
        r'function\s+([a-zA-Z_][\w]*)\s*\(',
        r'([a-zA-Z_][\w]*)\s*[:=]\s*function\s*\(',
        r'const\s+([a-zA-Z_][\w]*)\s*=\s*\(',
        r'let\s+([a-zA-Z_][\w]*)\s*=\s*\(',
        r'var\s+([a-zA-Z_][\w]*)\s*=\s*\('
    ]
    
    print(f"\n文件大小: {len(js_content)} 字符")
    print("\n查找可能的函数名...")
    
    # 查找与 play、video、url 相关的字符串
    keywords = ['play', 'video', 'url', 'build', 'encrypt', 'decrypt', 'wasm', 'nbmovie', 'secret']
    
    print(f"\n查找包含关键词的代码段:")
    print("-"*70)
    
    for keyword in keywords:
        matches = [m.start() for m in re.finditer(re.escape(keyword), js_content, re.IGNORECASE)]
        if matches:
            print(f"\n找到 '{keyword}': {len(matches)} 次")
            # 打印前几个匹配的上下文
            for idx, pos in enumerate(matches[:3]):
                start = max(0, pos - 100)
                end = min(len(js_content), pos + 200)
                context = js_content[start:end]
                print(f"\n上下文 #{idx+1}:")
                print(context)


def test_wasm():
    """简单测试 wasm 加载"""
    print("\n" + "="*70)
    print("WebAssembly 模块分析")
    print("="*70)
    
    # 尝试加载 wasm 模块
    try:
        print("\nWASM 文件大小:", end=" ")
        with open("nbmovie_wasm_bg.wasm", "rb") as f:
            wasm_data = f.read()
        print(f"{len(wasm_data)} bytes")
        
        print("\nWASM 文件前 200 字节（十六进制）:")
        print(wasm_data[:200].hex())
        
    except Exception as e:
        print(f"无法加载 wasm 文件: {e}")


def main():
    analyze_js_file()
    test_wasm()
    
    print("\n" + "="*70)
    print("分析总结")
    print("="*70)
    print("\n根据我们的分析，网站流程如下:")
    print("1. 访问播放页面")
    print("2. 提取必要参数（nb_st, vodid, dataid, _pdf）")
    print("3. 使用 WebAssembly 中的 build_play_url 函数生成 URL 参数")
    print("4. 调用 /video/play 接口，得到加密后的视频 URL")
    print("5. 使用 m3u8 播放器播放视频")


if __name__ == "__main__":
    main()
