
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习用：加密/解密算法示例
仅用于教育目的，不涉及任何实际平台
"""

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import re
import time
from Crypto.Util.number import bytes_to_long, long_to_bytes


class DecryptExample:
    """学习用的解密示例类"""
    
    @staticmethod
    def example1_simple_aes():
        """示例1：简单的AES解密"""
        print("="*60)
        print("示例1：简单AES解密学习")
        print("="*60)
        
        # 虚构的加密数据（仅用于学习）
        key = b"1234567890123456"  # 16字节密钥
        iv = b"abcdefghijklmnop"   # 16字节IV
        original_data = b"This is a secret message!"
        
        # 先加密
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(original_data, AES.block_size)
        encrypted_bytes = cipher.encrypt(padded)
        encrypted = base64.b64encode(encrypted_bytes).decode()
        
        print(f"密钥: {key}")
        print(f"IV: {iv}")
        print(f"原始数据: {original_data}")
        print(f"加密数据(Base64): {encrypted}")
        
        # 解密
        cipher2 = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher2.decrypt(base64.b64decode(encrypted))
        decrypted = unpad(decrypted_padded, AES.block_size)
        print(f"解密结果: {decrypted}")
        print()
    
    @staticmethod
    def example2_xor_encryption():
        """示例2：XOR加密学习"""
        print("="*60)
        print("示例2：XOR加密学习")
        print("="*60)
        
        original = "Hello World!"
        key = "secretkey"
        
        print(f"原始数据: {original}")
        print(f"密钥: {key}")
        
        encrypted = []
        for i, char in enumerate(original):
            encrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
        
        encrypted_str = ''.join(encrypted)
        print(f"XOR加密结果: {encrypted_str.encode('utf-8')}")
        
        # 解密（XOR是对称的）
        decrypted = []
        for i, char in enumerate(encrypted_str):
            decrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
        
        print(f"解密结果: {''.join(decrypted)}")
        print()
    
    @staticmethod
    def example3_base64():
        """示例3：Base64编码解码"""
        print("="*60)
        print("示例3：Base64编码解码")
        print("="*60)
        
        original = "Learn cryptography!"
        
        print(f"原始: {original}")
        
        encoded = base64.b64encode(original.encode()).decode()
        print(f"Base64编码: {encoded}")
        
        decoded = base64.b64decode(encoded).decode()
        print(f"Base64解码: {decoded}")
        print()
    
    @staticmethod
    def example4_hash():
        """示例4：哈希学习"""
        print("="*60)
        print("示例4：SHA-256哈希")
        print("="*60)
        
        data = "password123"
        salt = "salt_example"
        
        print(f"数据: {data}")
        print(f"盐: {salt}")
        
        hash_obj = hashlib.sha256((data + salt).encode())
        print(f"SHA-256: {hash_obj.hexdigest()}")
        print()


def b64encode_safe(s):
    """安全的Base64编码"""
    return base64.b64encode(s.encode()).decode()


def clean_string_for_display(s):
    """清理字符串以便显示（不破坏加密数据）"""
    # 这个函数只用于显示，不用于实际解密
    return re.sub(r'[^\x20-\x7E]', '', s)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("加密算法学习示例")
    print("="*60 + "\n")
    
    DecryptExample.example1_simple_aes()
    DecryptExample.example2_xor_encryption()
    DecryptExample.example3_base64()
    DecryptExample.example4_hash()
    
    print("="*60)
    print("学习要点：")
    print("1. AES是对称加密，需要密钥和IV")
    print("2. XOR加密简单但安全性低")
    print("3. Base64是编码不是加密")
    print("4. 哈希是单向的，无法解密")
    print("="*60)
