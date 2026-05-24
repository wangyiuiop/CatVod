#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AES解密是否正确
"""
import base64

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    print("✅ pycryptodome 已安装")
except ImportError:
    print("❌ pycryptodome 未安装")
    print("请运行: pip install pycryptodome")
    exit(1)

# 从之前的分析中提取的token
TOKEN_FROM_API = "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==34"

# Drpy配置中的密钥和IV
KEY = b'ejjooopppqqqrwww'  # 16字节
IV = b'1348987635684651'    # 16字节

def test_aes_decrypt(token):
    """
    测试AES解密
    """
    print("="*70)
    print("测试 AES 解密")
    print("="*70)
    
    print(f"\n原始Token:")
    print(f"  {token}")
    
    print(f"\n密钥 (16字节):")
    print(f"  {KEY.decode()}")
    print(f"  十六进制: {KEY.hex()}")
    
    print(f"\nIV (16字节):")
    print(f"  {IV.decode()}")
    print(f"  十六进制: {IV.hex()}")
    
    print(f"\n尝试解密...")
    
    try:
        # 1. Base64解码
        print(f"\n1️⃣ Base64解码:")
        token_bytes = base64.b64decode(token)
        print(f"   长度: {len(token_bytes)} 字节")
        print(f"   十六进制: {token_bytes.hex()}")
        
        # 2. AES CBC 解密
        print(f"\n2️⃣ AES CBC 解密:")
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(token_bytes)
        print(f"   解密后 (原始): {decrypted}")
        
        # 3. 移除PKCS7填充
        print(f"\n3️⃣ 移除PKCS7填充:")
        try:
            unpadded = unpad(decrypted, AES.block_size)
            result = unpadded.decode('utf-8')
            print(f"   ✅ 成功! 解密结果:")
            print(f"   '{result}'")
            return result
        except Exception as e:
            print(f"   ❌ 移除填充失败: {e}")
            
            # 尝试手动移除null字节
            result = decrypted.rstrip(b'\x00')
            print(f"\n   尝试移除null: {result}")
            
            # 尝试移除其他可能的填充
            for i in range(1, 17):
                test = decrypted.rstrip(decrypted[-i:])
                if len(test) % 16 == 0:
                    result = test
                    break
            
            try:
                result = result.decode('utf-8')
                print(f"   ✅ 成功! 解密结果:")
                print(f"   '{result}'")
                return result
            except:
                print(f"   ❌ 最终失败")
                return None
            
    except Exception as e:
        print(f"\n❌ 解密失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_multiple_tokens():
    """
    测试多个可能的token
    """
    print("\n\n" + "="*70)
    print("测试多个Token")
    print("="*70)
    
    # 从之前分析中获取的所有token
    tokens = [
        "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==34",
        "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==349",
        "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==347",
        "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==348",
    ]
    
    for i, token in enumerate(tokens):
        print(f"\n{'='*70}")
        print(f"测试 Token {i+1}")
        print(f"{'='*70}")
        result = test_aes_decrypt(token)
        if result:
            print(f"\n✅ Token {i+1} 解密成功!")
        else:
            print(f"\n❌ Token {i+1} 解密失败")

def test_different_modes():
    """
    尝试不同的解密模式
    """
    print("\n\n" + "="*70)
    print("尝试不同的解密模式")
    print("="*70)
    
    token = TOKEN_FROM_API
    
    try:
        token_bytes = base64.b64decode(token)
    except:
        print("Base64解码失败")
        return
    
    modes = [
        ("AES.MODE_CBC", AES.MODE_CBC),
        ("AES.MODE_ECB", AES.MODE_ECB),
        ("AES.MODE_CFB", AES.MODE_CFB),
        ("AES.MODE_OFB", AES.MODE_OFB),
    ]
    
    for mode_name, mode in modes:
        print(f"\n{mode_name}:")
        try:
            if mode == AES.MODE_ECB:
                cipher = AES.new(KEY, mode)
            else:
                cipher = AES.new(KEY, mode, IV)
            
            decrypted = cipher.decrypt(token_bytes)
            print(f"  {decrypted}")
            
            # 检查是否有可读字符
            try:
                result = decrypted.rstrip(b'\x00').decode('utf-8')
                print(f"  ✅ 可读: {result}")
            except:
                print(f"  ❌ 不可读")
        except Exception as e:
            print(f"  ❌ 失败: {e}")

if __name__ == "__main__":
    # 先测试主要token
    test_aes_decrypt(TOKEN_FROM_API)
    
    # 然后测试多个token
    test_multiple_tokens()
    
    # 最后测试不同模式
    test_different_modes()
