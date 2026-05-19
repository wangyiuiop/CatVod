# 4kvm.tv TVBox 源

完整的 4kvm.tv 爬虫，用于 TVBox，包含所有功能：主页、分类、搜索、详情、播放地址获取。

## 功能特点

- ✅ **首页推荐** - 获取首页热门内容
- ✅ **分类浏览** - 电影、电视剧、动漫
- ✅ **搜索功能** - 关键词搜索
- ✅ **详情获取** - 视频介绍、播放列表
- ✅ **播放解析** - 使用 Playwright 浏览器自动化获取真实 M3U8 地址

## 安装使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器
```bash
playwright install chromium
```

### 3. 运行服务
```bash
python tvbox_complete.py
```

### 4. 配置 TVBox
在 TVBox 中添加源地址：
```
http://127.0.0.1:5000/config.js
```

## 文件说明

- `tvbox_complete.py` - 完整版本，含 Playwright 播放解析
- `tvbox_4kvm.py` - 基础版本，不含 Playwright
- `analyze_website_structure.py` - 网站结构分析工具
- `requirements.txt` - Python 依赖包

## API 接口

| 接口 | 功能 |
|------|------|
| `/` | 服务状态 |
| `/api.php/provide/vod/` | 主接口（列表、搜索、详情） |
| `/api.php/provide/vod/play/` | 播放地址解析 |
| `/config.js` | TVBox 配置 |

## 技术说明

### 网站结构
该网站使用 WebAssembly 实现的 `build_play_url` 函数来加密生成视频地址，我们使用浏览器自动化来绕过逆向分析。

### 核心流程
1. 请求播放页面
2. 等待 WebAssembly 模块加载
3. 拦截网络请求捕获真实 M3U8 地址
4. 返回给 TVBox 播放

## 测试

访问以下地址测试各功能：

- 主页：http://127.0.0.1:5000/api.php/provide/vod/
- 搜索：http://127.0.0.1:5000/api.php/provide/vod/?wd=飞驰
- 电影分类：http://127.0.0.1:5000/api.php/provide/vod/?ac=list&t=1

## 免责声明

本项目仅供学习研究使用，请勿用于商业用途。请遵守版权法，支持正版内容。
