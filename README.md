# 路漫漫动漫爬虫 - 完整使用说明

## 📦 最终文件

| 文件 | 说明 |
|------|------|
| **lmm85_spider_final.py** | 最终爬虫，双模式播放 |
| ANALYSIS_REPORT.md | 完整分析报告 |
| extract_direct_link.py | 独立直链提取工具 |
| test_*.py | 各种测试脚本 |
| debug_*.* | 调试文件 |

## 🚀 使用指南

### 方式1: 基本稳定模式 (推荐直接使用)
不需要任何额外依赖，直接使用 `lmm85_spider_final.py`：
- 自动返回播放页面URL
- 播放器会自己处理iframe和播放
- 稳定，不依赖额外库

### 方式2: 高级直链提取模式 (需要Playwright)
如果你想提取真实的直链，安装Playwright：

```bash
# 安装Playwright
pip install playwright

# 安装Chromium
playwright install chromium
```

然后 `lmm85_spider_final.py` 会自动：
1. 首先尝试用Playwright提取真实视频地址
2. 如果失败，自动降级到基本模式

### 方式3: 使用独立的直链提取工具
运行 `extract_direct_link.py` 可以单独提取直链。

## 🎯 功能说明

### lmm85_spider_final.py
- ✅ 分类浏览
- ✅ 搜索功能 (会检测验证码)
- ✅ 视频详情页
- ✅ 双模式播放解析:
  - Playwright提取真实直链 (可选)
  - 自动降级到基本模式

## 📊 完整分析总结

### 网站播放流程
```
播放页面 → player数据 → 云解析API → POST请求 → 真实视频地址
```

### Token生成分析
- 核心JS混淆且反调试 (`/jsplayer/a.js` 和 `/jsplayer/b.js`)
- 直接逆向难度较大
- **最佳方案**: Playwright模拟浏览器获取直链

## 📁 调试文件
之前的测试中生成了很多调试文件，可以参考：
- debug_play_page.html
- debug_player_tudou.js
- debug_api_response.html
- debug_core_1.js (反调试)
- debug_core_2.js (混淆核心)

## ⚠️ 注意事项

1. 请合理控制请求频率，避免对网站造成影响
2. 搜索功能可能触发验证码
3. 直链提取需要较长等待时间 (15-20秒)

## 🎉 总结

使用 **lmm85_spider_final.py** 就可以了！
- 不安装Playwright：稳定的基本模式
- 安装Playwright：自动尝试直链提取，失败则降级
