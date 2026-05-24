# 路漫漫动漫网站视频播放逻辑分析报告

## 📋 分析概述

本报告详细分析了 https://www.lmm85.com 网站的视频播放地址生成和解密逻辑，并提供了完整的Python实现。

---

## 🎯 核心发现

### 1. 播放页面数据结构

访问播放页面（如 https://www.lmm85.com/play/8094_1_1.html）后，页面会包含一个 `player_*` 变量，存储JSON格式的播放数据：

```javascript
var player_8094_1_1 = {
    "url": "加密或编码后的视频地址",
    "from": "player类型",
    "encrypt": 0|1|2  // 加密类型
};
```

### 2. 加密类型说明

| 加密类型(encrypt) | 说明 | 解密方式 |
|-------------------|------|---------|
| 0 | 未加密 | 直接使用 |
| 1 | unescape编码 | 使用 `unescape()` 解码 |
| 2 | base64编码 + unescape | 先base64解码，再unescape |

### 3. AES解密关键参数

Drpy配置中发现的AES加密参数：

```javascript
var key = CryptoJS.enc.Utf8.parse("ejjooopppqqqrwww");
var iv = CryptoJS.enc.Utf8.parse("1348987635684651");
```

- **密钥(Key)**: `ejjooopppqqqrwww` (16字节 = 128位)
- **初始化向量(IV)**: `1348987635684651` (16字节)
- **加密模式**: AES.CBC
- **填充方式**: CryptoJS.pad.Pkcs7

---

## 🔍 播放流程分析

### 完整播放流程

```
1. 访问播放页面 (play.html)
   ↓
2. 提取 player_* JSON数据
   ├── url: 视频地址（可能加密）
   ├── from: 播放器类型
   └── encrypt: 加密类型（0,1,2）
   ↓
3. 解密/解码 URL (如需要)
   ├── encrypt=0 → 直接使用
   ├── encrypt=1 → unescape()
   └── encrypt=2 → base64.decode() → unescape()
   ↓
4. 检查是否为直接视频 (mp4/m3u8/flv)
   ├── 是 → 直接播放
   └── 否 → 进入下一步
   ↓
5. 获取 player/from.js 解析文件
   ↓
6. 解析JS，提取API调用
   ↓
7. 发送POST请求到视频API
   ├── vid: 视频ID
   ├── t: 时间戳
   ├── token: AES加密的token（需要解密）
   ├── act: 操作类型
   └── play: 播放参数
   ↓
8. 解析API响应，获取真实视频地址
   ├── ext="hls" → 返回m3u8
   ├── ext="xgplayer" → 二次请求
   └── 其他 → 直接返回url
```

---

## 💻 Python实现详解

### 1. AES解密函数

```python
def get_daes_string(self, token):
    """
    AES CBC解密token
    """
    try:
        key = b'ejjooopppqqqrwww'  # 16字节密钥
        iv = b'1348987635684651'  # 16字节IV
        
        token_bytes = base64.b64decode(token)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(token_bytes)
        
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except Exception as e:
        print(f"[错误] AES解密失败: {str(e)}")
        return None
```

### 2. 播放数据提取

```python
def _extract_player_data(self, html):
    """从HTML中提取player_.*?= {...} JSON数据"""
    patterns = [
        r'var\s+player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
        r'player_.*?=\s*(\{[^{]*?(?:\{[^{]*\}[^{]*)*\})\s*;',
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.S):
            try:
                data_str = match.group(1)
                data = json.loads(data_str)
                return data
            except json.JSONDecodeError:
                continue
    return None
```

### 3. 加密URL处理

```python
def _resolve_video_url(self, player_data, referer):
    url = player_data.get('url', '')
    encrypt = player_data.get('encrypt', 0)
    
    if encrypt == 1:
        url = urllib.parse.unquote(url)
    elif encrypt == 2:
        decoded = base64.b64decode(url).decode('utf-8')
        url = urllib.parse.unquote(decoded)
    
    return url
```

### 4. POST请求处理

```python
def _handle_post_request(self, response_text, referer):
    # 提取参数
    post_url = re.search(r'post\(["\'](.*?)["\']', response_text).group(1)
    vid = re.search(r'vid\s*=\s*["\'](.*?)["\']', response_text).group(1)
    token = re.search(r'token\s*=\s*["\'](.*?)["\']', response_text).group(1)
    
    # AES解密token
    decrypted_token = self.get_daes_string(token)
    
    # 发送POST请求
    body = {
        'vid': vid,
        'token': decrypted_token,
        'act': act,
        'play': play
    }
    
    response = self._post_request(post_url, body)
    return self._parse_video_response(response)
```

---

## 📦 完整文件

### 1. lmm85_spider_final.py

完整的Python爬虫实现，包含：
- ✅ 完整的AES解密功能
- ✅ 播放地址解析
- ✅ 分类浏览
- ✅ 搜索功能
- ✅ 详细的调试输出

### 2. 依赖安装

```bash
pip install pycryptodome
```

### 3. 使用示例

```python
# 测试播放
spider = Spider()
result = spider.playerContent('box聚合', '/play/8094_1_1.html', [])
print(f"播放地址: {result.get('url')}")
```

---

## ⚠️ 注意事项

### 1. 合法性

请仅将此代码用于学习研究目的，不要用于商业用途或未经授权的数据采集。

### 2. 网站变化

网站的加密参数、接口地址等可能会随时变化，需要定期更新。

### 3. 性能

建议：
- 合理控制请求频率，避免对网站造成负担
- 添加适当的延时和重试机制

---

## 🔧 调试技巧

### 1. 启用调试输出

代码中已添加详细的调试信息，运行时会显示：
- player_data
- URL解密过程
- POST请求参数
- API响应数据

### 2. 检查关键点

```
关键点1: 能否正确提取 player_data
关键点2: URL解密是否正确
关键点3: token是否能成功AES解密
关键点4: POST请求是否成功
关键点5: API响应是否包含真实视频地址
```

---

## 📝 总结

本报告和配套代码完整实现了：
1. ✅ 网站视频播放数据提取
2. ✅ 加密URL解密（unescape、base64）
3. ✅ AES解密token
4. ✅ POST请求处理
5. ✅ 真实视频地址解析

如有问题，请查看调试输出或重新分析网站结构。
