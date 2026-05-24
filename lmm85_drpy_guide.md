# Drpy JS配置移植说明

## 📋 移植概述

我已经将Drpy JS配置移植到了Python爬虫代码中：
- **文件位置**: `/workspace/lmm85_drpy_ported.py`
- **配置来源**: 你提供的Drpy JS规则

## 🔍 JS配置核心解析逻辑

### 1. 播放流程图

```
播放页HTML 
  ↓
提取JSON数据 {url, from, encrypt}
  ↓
┌─────────────────────────────────────────┐
│ encrypt = 0: 直接使用URL                │
│ encrypt = 1: unescape解码               │
│ encrypt = 2: base64 + unescape解码      │
└─────────────────────────────────────────┘
  ↓
检查是否为.mp4/.m3u8/.flv
  ↓
┌─────────────────────────────────────────┐
│ 是 → 直接返回播放URL                     │
│ 否 → 调用播放器JS获取解析逻辑            │
└─────────────────────────────────────────┘
  ↓
获取player/{from}.js
  ↓
解析JS代码，提取MacPlayer.Parse逻辑
  ↓
发送POST请求获取真实视频URL
  ↓
┌─────────────────────────────────────────┐
│ ext = "hls" → 返回m3u8 URL             │
│ ext = "hls_list" → 解码返回m3u8         │
│ ext = "xgplayer" → 二次请求获取真实URL  │
└─────────────────────────────────────────┘
```

### 2. 关键代码片段

#### 播放器数据提取
```javascript
var html = JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);
var url = html.url;
var from = html.from;
```

#### 加密处理
```javascript
if (html.encrypt == "1") {
    url = unescape(url);
} else if (html.encrypt == "2") {
    url = unescape(base64Decode(url));
}
```

#### POST请求处理
```javascript
var posturl = postapi + playht.match(/post\("(.*?)"/)[1];
if (/act\s*=/.test(playht)) {
    var vid = playht.match(/vid\s*=\s*"(.*?)"/)[1];
    var t = playht.match(/var\s+t\s*=\s*"(.*?)"/)[1];
    var token = playht.match(/token\s*=\s*"(.*?)"/)[1];
    var act = playht.match(/act\s*=\s*"(.*?)"/)[1];
    var play = playht.match(/play\s*=\s*"(.*?)"/)[1];
    token = getDAesString(token);
}
```

#### AES解密
```javascript
var key = CryptoJS.enc.Utf8.parse("ejjooopppqqqrwww");
var iv = CryptoJS.enc.Utf8.parse("1348987635684651");
var token = CryptoJS.AES.decrypt(token, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
});
```

## 🚀 Python实现分析

### ✅ 已实现的功能

1. **播放器数据提取**
   - 从HTML中提取player_.*?= {...} JSON数据
   - 提取url、from、encrypt字段

2. **加密URL处理**
   - encrypt=1: unescape解码
   - encrypt=2: base64 + unescape解码

3. **POST请求处理**
   - 提取POST参数（vid、t、token、act、play）
   - 发送POST请求
   - 处理多种响应类型

4. **响应解析**
   - hls/hls_list: 返回解码后的m3u8 URL
   - xgplayer: 二次请求获取真实URL
   - 其他: 直接返回url字段

5. **视频源切换**
   - 支持多个播放线路（box聚合等）

### ⚠️ 未完全实现的部分

#### 1. CryptoJS AES解密
```python
# JavaScript版本
var key = CryptoJS.enc.Utf8.parse("ejjooopppqqqrwww");
var iv = CryptoJS.enc.Utf8.parse("1348987635684651");
var token = CryptoJS.AES.decrypt(token, key, {...});
```

**Python实现建议**:
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def aes_decrypt(token, key, iv):
    """AES CBC解密"""
    try:
        key_bytes = key.encode('utf-8')  # b'ejjooopppqqqrwww'
        iv_bytes = iv.encode('utf-8')    # b'1348987635684651'
        token_bytes = base64.b64decode(token)
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted = unpad(cipher.decrypt(token_bytes), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"[错误] AES解密失败: {str(e)}")
        return None
```

#### 2. 动态JS代码执行
```javascript
// 这部分逻辑很难在Python中完全模拟
eval(getCryptoJS());
```

**建议**: 如果需要完整的JS执行能力，可以考虑：
- 使用 `PyExecJS` 库
- 使用 `node.js` 子进程
- 或使用 `Playwright` 模拟浏览器

## 📊 配置对比

| 配置项 | JS版本 | Python版本 |
|--------|--------|------------|
| 网站标题 | ✅ 路漫漫 | ✅ 路漫漫 |
| 主机URL | ✅ https://www.lmm85.com | ✅ https://www.lmm85.com |
| 分类配置 | ✅ 6个分类 | ✅ 6个分类 |
| 搜索URL | ✅ /vod/search/page/{pg}/wd/{key} | ✅ 已实现 |
| 筛选规则 | ✅ 年代+排序 | ⚠️ 简化实现 |
| 播放解析 | ✅ 完整逻辑 | ⚠️ 基础实现 |
| AES解密 | ✅ 支持 | ⚠️ 需要安装pycryptodome |

## 🛠️ 完整实现建议

如果需要完整的播放功能（包括AES解密），建议：

### 方法1: 安装pycryptodome
```bash
pip install pycryptodome
```

然后在代码中添加：
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def get_daes_string(token):
    """AES CBC解密token"""
    try:
        key = b'ejjooopppqqqrwww'
        iv = b'1348987635684651'
        decrypted = base64.b64decode(token)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(decrypted), AES.block_size).decode('utf-8')
    except:
        return None
```

### 方法2: 使用Playwright（推荐）
```python
from playwright.sync_api import sync_playwright

def playerContent(self, flag, id, vipFlags):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"{self.url}{id}")
        
        # 等待播放器加载
        page.wait_for_selector('iframe, video', timeout=10000)
        
        # 获取iframe src或video src
        iframe = page.query_selector('iframe')
        if iframe:
            return {'parse': 1, 'url': iframe.get_attribute('src')}
        
        video = page.query_selector('video')
        if video:
            return {'parse': 0, 'url': video.get_attribute('src')}
        
        browser.close()
        return {'parse': 1, 'url': id}
```

### 方法3: 混合方案
```python
def playerContent(self, flag, id, vipFlags):
    # 先尝试Python解析
    result = self._python_player解析(id)
    if result:
        return result
    
    # 失败则使用简化播放
    return {'parse': 1, 'url': id, 'header': self.header}
```

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| lmm85_drpy_ported.py | 移植后的完整爬虫代码 |
| lmm85_drpy_guide.md | 本说明文档 |

## 🎯 使用建议

### 测试步骤

1. **测试分类浏览**
   ```python
   result = spider.categoryContent('6', '1', False, {})
   print(f"日本动漫数量: {len(result['list'])}")
   ```

2. **测试搜索**
   ```python
   result = spider.searchContent('进击的巨人', False, '1')
   print(f"搜索结果: {len(result['list'])}")
   ```

3. **测试播放**
   ```python
   result = spider.playerContent('box聚合', '/play/8094_1_1.html', [])
   print(f"播放URL: {result.get('url')}")
   ```

### 调试建议

如果播放失败：

1. **检查player_.*?= JSON提取**
   ```python
   # 在playerContent中添加调试
   print(f"[调试] HTML长度: {len(html)}")
   print(f"[调试] player_data: {player_data}")
   ```

2. **检查URL类型**
   ```python
   print(f"[调试] URL: {url}")
   print(f"[调试] encrypt: {encrypt}")
   print(f"[调试] 是否直接视频: {self._is_direct_video_url(url)}")
   ```

3. **检查POST请求**
   ```python
   print(f"[调试] POST响应: {response_text[:200]}")
   ```

## ⚠️ 已知限制

1. **AES解密**: 需要安装pycryptodome才能完整支持
2. **复杂JS逻辑**: 部分JS代码执行逻辑无法在Python中完全模拟
3. **动态加载**: 需要Playwright才能处理完全动态加载的内容

## 🚀 下一步

1. 先测试现有代码的基本功能
2. 如果播放失败，根据调试输出调整
3. 如需完整AES支持，安装pycryptodome
4. 如需完整JS支持，考虑使用Playwright

---

**生成时间**: 2026-05-24  
**适用版本**: Python爬虫 + Drpy配置移植
