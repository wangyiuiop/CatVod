#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入分析AES解密问题
"""
import base64

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    print("❌ 需要安装 pycryptodome")
    exit(1)

# 测试token
TOKEN = "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==34"

print("="*70)
print("深入分析 AES 解密")
print("="*70)

print(f"\n原始Token: {TOKEN}")

# 1. Base64解码
print(f"\n1️⃣ Base64解码:")
try:
    token_bytes = base64.b64decode(TOKEN)
    print(f"   ✅ 成功! 长度: {len(token_bytes)}")
    print(f"   十六进制: {token_bytes.hex()}")
except Exception as e:
    print(f"   ❌ 失败: {e}")
    
    # 尝试补齐base64
    print(f"\n   尝试补齐Base64...")
    padded_token = TOKEN + "=="
    try:
        token_bytes = base64.b64decode(padded_token)
        print(f"   ✅ 成功补齐! 长度: {len(token_bytes)}")
        print(f"   十六进制: {token_bytes.hex()}")
    except:
        padded_token = TOKEN + "="
        try:
            token_bytes = base64.b64decode(padded_token)
            print(f"   ✅ 成功补齐! 长度: {len(token_bytes)}")
            print(f"   十六进制: {token_bytes.hex()}")
        except Exception as e2:
            print(f"   ❌ 补齐也失败: {e2}")
            exit(1)

# 2. 尝试添加padding
print(f"\n2️⃣ 尝试添加padding使其为16字节倍数:")

# 长度54，补齐到56（最近的16倍数）
padded_length = ((len(token_bytes) // 16) + 1) * 16
padding_needed = padded_length - len(token_bytes)

padded_bytes = token_bytes + b'\x00' * padding_needed
print(f"   原始长度: {len(token_bytes)}")
print(f"   补齐后长度: {len(padded_bytes)}")
print(f"   补齐的字节: {padding_needed}")

# 3. 测试不同的key/iv组合
print(f"\n3️⃣ 尝试不同的Key/IV组合:")

combinations = [
    ("ejjooopppqqqrwww", "1348987635684651"),
    ("ejjooopppqqqrwww", "1234567890123456"),
    ("1234567890123456", "1348987635684651"),
    ("abcdefghijklmnop", "1234567890123456"),
    ("passwordpassword", "1234567890123456"),
]

KEY = b'ejjooopppqqqrwww'
IV = b'1348987635684651'

for i, (key_str, iv_str) in enumerate(combinations):
    print(f"\n   组合{i+1}: Key='{key_str}', IV='{iv_str}'")
    
    key = key_str.encode('utf-8')[:16].ljust(16, b'\x00')
    iv = iv_str.encode('utf-8')[:16].ljust(16, b'\x00')
    
    print(f"   Key(16): {key}")
    print(f"   IV(16): {iv}")
    
    # 测试不同模式
    for mode_name, mode in [("CBC", AES.MODE_CBC), ("ECB", AES.MODE_ECB)]:
        try:
            if mode == AES.MODE_ECB:
                cipher = AES.new(key, mode)
            else:
                cipher = AES.new(key, mode, iv)
            
            decrypted = cipher.decrypt(padded_bytes)
            print(f"   {mode_name}解密: {decrypted}")
            
            # 检查结果
            try:
                result = decrypted.rstrip(b'\x00').decode('utf-8')
                if result and len(result) > 0:
                    print(f"   ✅ 可读: '{result}'")
            except:
                pass
                
        except Exception as e:
            print(f"   {mode_name}失败: {e}")

# 4. 直接从视频URL测试
print(f"\n4️⃣ 分析token组成:")
print(f"   Token看起来是: Base64(加密数据) + 2位数字")
print(f"   最后两位 '34' 可能是校验位")
print(f"   实际Base64: {TOKEN[:-2]}")

real_token = TOKEN[:-2]
try:
    real_bytes = base64.b64decode(real_token)
    print(f"   实际数据长度: {len(real_bytes)}")
    
    # 补齐到16字节
    padded = real_bytes + b'\x00' * (16 - len(real_bytes) % 16)
    print(f"   补齐后长度: {len(padded)}")
    
    print(f"\n   尝试解密实际数据:")
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(padded)
    print(f"   结果: {decrypted}")
    
    try:
        result = decrypted.rstrip(b'\x00').decode('utf-8')
        print(f"   ✅ 可读: '{result}'")
    except:
        pass
        
except Exception as e:
    print(f"   失败: {e}")

print("\n" + "="*70)
print("分析完成!")
print("="*70)
