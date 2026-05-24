#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JS混淆代码分析
"""
import re

def analyze_obfuscated_js():
    """
    分析 /jsplayer/b.js 中的混淆代码
    """
    print("="*70)
    print("分析混淆的 JS 代码")
    print("="*70)
    
    # 读取混淆的JS
    with open('jsplayer_1.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    
    print("\n原始混淆代码:")
    print(js_code[:200])
    print("...")
    
    # 提取 eval 中的内容
    print("\n" + "="*70)
    print("尝试解混淆")
    print("="*70)
    
    # 提取整个eval函数
    eval_pattern = r"eval\s*\(\s*function\s*\(\s*p\s*,\s*a\s*,\s*c\s*,\s*k\s*,\s*e\s*,\s*r\s*\)"
    
    if re.search(eval_pattern, js_code):
        print("\n✅ 找到标准的packer混淆")
        
        # 这是 Dean Edwards 的 Packer 混淆
        # 格式: eval(function(p,a,c,k,e,r){...}('...',62,69,...))
        
        # 提取参数
        params_match = re.search(r"function\s*\(\s*p\s*,\s*a\s*,\s*c\s*,\s*k\s*,\s*e\s*,\s*r\s*\)\s*\{(.*?)\}\s*\('(.*)'\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*'(.*?)'\.split\s*\('\|'\s*\)", js_code, re.S)
        
        if params_match:
            print("\n提取到参数:")
            print(f"  函数体: {params_match.group(1)[:100]}...")
            print(f"  加密字符串: {params_match.group(2)[:50]}...")
            print(f"  数字参数: {params_match.group(3)}, {params_match.group(4)}")
            print(f"  字符串键: {params_match.group(5)[:50]}...")
    
    # 尝试简单替换
    print("\n" + "="*70)
    print("手动分析关键部分")
    print("="*70)
    
    # 提取字符串替换表
    string_keys_match = re.search(r"'(.*?)'\.split\s*\('\|'\s*\)", js_code)
    if string_keys_match:
        keys_string = string_keys_match.group(1)
        keys = keys_string.split('|')
        print(f"\n字符串替换表 ({len(keys)} 个):")
        for i, key in enumerate(keys):
            print(f"  {i}: {key}")
    
    # 查找关键函数调用
    print("\n查找关键函数:")
    
    if 'md5' in js_code:
        print("  ✅ 包含 md5")
    
    if 'base64' in js_code.lower():
        print("  ✅ 包含 base64")
    
    if 'encrypt' in js_code.lower() or 'decrypt' in js_code.lower():
        print("  ✅ 包含加密/解密")
    
    # 查找eval调用的参数
    print("\n分析 eval 调用:")
    
    # 提取被混淆的字符串
    obfuscated_string_match = re.search(r"\}','([^']+)',\d+,\d+,'", js_code)
    if obfuscated_string_match:
        obfuscated = obfuscated_string_match.group(1)
        print(f"  混淆字符串长度: {len(obfuscated)}")
        print(f"  前100字符: {obfuscated[:100]}")
    
    # 保存详细分析
    with open('js_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("混淆JS代码分析\n")
        f.write("="*70 + "\n\n")
        
        f.write("原始代码:\n")
        f.write(js_code + "\n\n")
        
        if string_keys_match:
            f.write("字符串替换表:\n")
            for i, key in enumerate(keys):
                f.write(f"  {i}: {key}\n")
        
        if obfuscated_string_match:
            f.write("\n混淆字符串:\n")
            f.write(obfuscated + "\n")
    
    print("\n✅ 详细分析已保存到 js_analysis.txt")
    
    print("\n" + "="*70)
    print("结论")
    print("="*70)
    print("\n这段代码看起来是反调试/检测代码，")
    print("真正的token生成可能在其他JS文件中。")
    print("\n建议:")
    print("1. 分析 API 页面的完整执行流程")
    print("2. 使用 Playwright 捕获所有网络请求")
    print("3. 或者找到其他包含完整算法的JS文件")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    analyze_obfuscated_js()
