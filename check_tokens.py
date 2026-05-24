#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有Token的Base64有效性
"""
import base64

# 从API获取的所有token
tokens = {
    'token': "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==34",
    'token1': "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==349",
    'token2': "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==347",
    'token3': "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==348",
}

print("="*70)
print("检查所有Token的Base64有效性")
print("="*70)

for name, token in tokens.items():
    print(f"\n{name}:")
    print(f"  原始: {token}")
    
    # 尝试各种base64变体
    variants = [
        token,
        token + "==",
        token + "=",
        token[:-2],
        token[:-2] + "==",
        token[:-2] + "=",
    ]
    
    for variant in variants:
        try:
            decoded = base64.b64decode(variant)
            print(f"  ✅ 成功: {variant[:50]}... -> {len(decoded)} 字节")
            print(f"     十六进制: {decoded.hex()}")
            
            # 检查是否是16字节倍数
            if len(decoded) % 16 == 0:
                print(f"     ⭐ 正好是16字节倍数! 可以直接AES解密")
            else:
                # 计算需要填充多少
                padding_needed = 16 - (len(decoded) % 16)
                print(f"     需要填充: {padding_needed} 字节")
                
        except Exception as e:
            pass

print("\n" + "="*70)
print("分析结论")
print("="*70)
print("\n看起来:")
print("1. 末尾的数字可能是某种校验或版本号")
print("2. 实际的Base64应该是去掉末尾数字的部分")
print("3. 但是数据长度(54或52)不是16的倍数")
print("\n可能的解决方案:")
print("1. 填充null字节到16倍数")
print("2. 使用其他解密算法")
print("3. 或者这些token本身就不需要解密")
