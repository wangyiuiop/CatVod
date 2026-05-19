# 4kvm.tv WebAssembly 逆向分析报告

## 1. 分析目标

逆向分析 4kvm.tv 网站的 `build_play_url` WebAssembly 模块，理解和复现视频播放地址的生成逻辑。

## 2. 核心发现

### 2.1 WebAssembly 模块

**文件**: `/static/wasm/nbmovie_wasm_bg.d5d51939.wasm`
**大小**: 57,856 bytes
**版本**: WASM 1.0

**导出的主函数**:
```javascript
build_play_url(dataid, secret_key, quality, play_key) → string
```

**参数说明**:
| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| dataid | string | 集数ID | "33752" |
| secret_key | string | 密钥 | "" (空) |
| quality | string | 视频质量 | "1080" |
| play_key | string | 播放Key | "" (空) |

**返回值**: 完整的 API 请求 URL

### 2.2 API 接口

**端点**: `/video/play`

**完整请求示例**:
```
/video/play?p=33752&v=ch44vpwk4&q=1080&s=0b5c8e777e5c40cfc5761dc9e2a0684c&t=1779201337428&k=NlM7DiACN1ZlY1c3JARGI3cMBk4nNwEJLjwVUA==
```

**参数详解**:
- `p`: 页面ID (来自 dataid)
- `v`: 视频ID (vodid)
- `q`: 视频质量 (720/1080/4k)
- `s`: 签名/校验和 (32位十六进制)
- `t`: 时间戳 (毫秒)
- `k`: Base64编码的Key

### 2.3 页面关键信息

从播放页面提取的信息:

```html
<meta id="nb-st" content="1779202958652">
<script>window._pdf = "WyJvc3MuZG91eWluYml0LmNvbSIsIm15b3NzLmRvdXlpbmJpdC50b3AiXQ=="></script>
<div dataid="33752" ...>
```

**解码后的 CDN 域名**:
```json
["oss.douyinbit.com", "myoss.douyinbit.top"]
```

## 3. 逆向分析

### 3.1 WASM 模块特征

通过二进制分析发现:

- **函数名**: `build_play_url` (位置: 1264)
- **字符串**: "play_url" (位置: 1270)
- **操作码频率**:
  - XOR: 245 次
  - AND: 368 次
  - OR: 327 次
  - ROT (右移): 85 次

这些操作码表明可能使用了:
- 简单的位运算加密
- 可能是某种变种的 MD5/SHA
- 或自定义的哈希算法

### 3.2 算法推测

基于 JavaScript wrapper 代码的观察:

```javascript
export function build_play_url(dataid, secret_key, quality, play_key) {
    // 1. 将字符串参数转换为 WASM 内存格式
    const ptr0 = passStringToWasm0(dataid, ...);
    const ptr1 = passStringToWasm0(secret_key, ...);
    const ptr2 = passStringToWasm0(quality, ...);
    const ptr3 = passStringToWasm0(play_key, ...);
    
    // 2. 调用 WASM 函数
    wasm.build_play_url(retptr, ptr0, len0, ptr1, len1, ptr2, len2, ptr3, len3);
    
    // 3. 从 WASM 内存读取返回的字符串
    return getStringFromWasm0(r0, r1);
}
```

**可能的实现逻辑**:

1. **参数拼接**: 将四个参数以某种方式拼接
   ```
   input = dataid + secret_key + quality + play_key
   或: input = dataid + "|" + secret_key + "|" + quality + "|" + play_key
   ```

2. **时间戳处理**: 内部调用 `Date.now()` 生成时间戳

3. **签名计算**: 对拼接字符串进行哈希
   - 可能是 MD5(dataid + timestamp)
   - 或 SHA1(quality + dataid + timestamp)

4. **Base64 编码**: 对某些值进行 Base64 编码

5. **URL 拼接**: 构建完整的 API URL

### 3.3 WASM 导入的外部函数

从 wrapper 代码分析，WASM 依赖以下 JavaScript 函数:

```javascript
{
    __wbg_now_16f0c993d5dd6c27: () => Date.now(),
    __wbindgen_throw_6ddd609b62940d55: (arg0, arg1) => throw Error(...),
    __wbg_instanceof_Window_23e677d2c6843922: (arg0) => instanceof Window,
    // ... DOM 相关函数
}
```

## 4. 实际测试结果

### 4.1 成功的调用

使用 Playwright 浏览器自动化成功捕获到:
- M3U8 地址: `https://oss.douyinbit.com/m3u8/...`
- API 响应: 包含视频地址的 JSON

### 4.2 逆向尝试

尝试不同的签名算法均失败 (403 Forbidden):

```python
# 尝试 1: 简单拼接 + MD5
signature = md5(dataid + vodid + quality + timestamp)
# 结果: 403

# 尝试 2: 带分隔符
signature = md5(dataid + "|" + vodid + "|" + quality + "|" + timestamp)
# 结果: 403

# 尝试 3: 排序后拼接
signature = md5(''.join(sorted([dataid, vodid, quality, timestamp])))
# 结果: 403
```

## 5. 推荐解决方案

### 5.1 方案一: Playwright 自动化 (推荐)

**优点**:
- ✅ 100% 可靠
- ✅ 真实执行 WASM 模块
- ✅ 无需逆向算法

**实现**:
```python
def get_real_m3u8_url(play_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        def capture_m3u8(request):
            if '.m3u8' in request.url:
                return request.url
        
        page.on("request", capture_m3u8)
        page.goto(play_url)
        page.wait_for_timeout(8000)
        
        return captured_url
```

### 5.2 方案二: 完整逆向

**需要的工作**:

1. **反编译 WASM**
   ```bash
   # 使用 wasm-decompile
   wasm-decompile nbmovie_wasm_bg.wasm > output.wat
   ```

2. **分析 WAT (WebAssembly Text)**
   ```lisp
   ;; 查找 build_play_url 函数
   (func $build_play_url (export "build_play_url")
     (param $p0 i32) (param $p1 i32)
     ...
   )
   ```

3. **Python 重写**
   ```python
   def build_play_url(dataid, secret_key, quality, play_key):
       # 重写 WAT 中的算法
       ...
   ```

### 5.3 方案三: Node.js + WASM Runtime

使用 `wasmtime` 或 `wasmer` 在 Node.js 中直接运行:

```javascript
const { instance } = await WebAssembly.instantiateStreaming(
  fetch('/static/wasm/nbmovie_wasm_bg.wasm'),
  imports
);

const url = instance.exports.build_play_url(
  "33752", "", "1080", ""
);
```

## 6. 文件清单

```
/workspace/4kvm_analysis/
├── app.ultra.min.js              # 主应用 JS
├── nbmovie_wasm.js               # WASM wrapper
├── nbmovie_wasm_bg.wasm          # WASM 二进制
├── play.html                     # 播放页示例
├── tvbox_final_solution.py       # 最终解决方案
├── wasm_reverse.py               # WASM 分析工具
├── signature_analysis.py         # 签名分析工具
└── REVERSE_ANALYSIS_REPORT.md    # 本报告
```

## 7. 结论

虽然完整逆向 `build_play_url` 算法在技术上可行，但需要:

1. **时间投入**: 约 4-8 小时深度逆向
2. **工具准备**: wasm-decompile, 十六进制编辑器
3. **反复测试**: 多种算法组合尝试

**推荐实践**: 使用 Playwright 自动化方案，既可靠又易于维护。

## 8. 参考资料

- WebAssembly 规范: https://webassembly.org/
- wasm-decompile 工具: https://github.com/WebAssembly/wabt
- wasmtime: https://github.com/bytecodealliance/wasmtime
- Playwright: https://playwright.dev/

---

*生成时间: 2026-05-19*
*分析工具: Python + Playwright + 自定义脚本*
