# 路漫漫动漫 - 完整播放算法分析报告

## 📊 分析总结

通过对网站的完整逆向分析，我们总结了整个播放流程的关键环节！

## 🔄 完整播放流程

```
1. 访问 /play/{vid}_{sid}_{nid}.html (播放页面)
   ↓
2. 提取 player_aaaa={...} (包含 url, from 等信息)
   ↓
3. 获取 /static/player/{from}.js (播放器配置)
   ↓
4. 访问云解析API: https://yun.92cj.com/acfun58.php?id={url}&referer={播放页面}
   ↓
5. API返回包含POST参数的HTML页面
   ↓
6. 使用POST参数向同一个API发送请求
   ↓
7. 获取真实的视频地址 (通常是m3u8)
```

## 🔐 关键参数分析

### 播放页面提取的参数
```json
{
  "url": "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14=&t=DU",
  "from": "tudou",
  "encrypt": 0,
  "id": "5823",
  "sid": 1,
  "nid": 1
}
```

### API页面的POST参数
```json
{
  "vid": "DU_o0Y+2nWJZPZ/xBC6YeWi5vw6b2crTApnQYiUtV+6F14=",
  "type": "okjx",
  "sing": "58f03c01251576df2f1bad8e73ab96c3",
  "token": "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==34",
  "token1": "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==349",
  "token2": "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==347",
  "token3": "ACcHO1c9UiRQMQVtUSIBbQA5WjFSbgdqUGADal85UAxdMVU3Vm0GPFFlVWdWYFplVDQNMA==348",
  "t": "241",
  "ti": 1779620271
}
```

### API页面隐藏的关键信息
```html
<input type="hidden" id="hdMd5" value="EFBFCB31D5BACE6BB5793A529254424E" />
```

## 🕵️ 逆向难点

### 1. Token/Sing算法
- 核心生成逻辑在 `/jsplayer/` 下的混淆JS中
- `/jsplayer/a.js`: 反调试代码
- `/jsplayer/b.js`: 包含 eval 混淆的核心算法
- `/jsplayer/ckplayer.js`: 播放器

### 2. hdMd5
- API页面生成的唯一值
- 很可能与 Token/Sing 有关联

### 3. 时效性
- 测试发现 Token/Sing 有较短的时效性
- 过长时间后会返回 "ID参数错误"

## ✅ 解决方案

### 方案A: Playwright捕获（推荐，最可靠）
```python
使用 playwright 直接访问播放页面
监听网络请求
自动捕获真实的视频地址
```

优点：不需要逆向算法，最稳定
缺点：需要安装 Playwright，稍慢

### 方案B: 继续逆向核心算法
需要深入分析：
1. eval 混淆的 /jsplayer/b.js
2. hdMd5 的生成
3. Token/Sing/ti/t 的关联

## 📁 已生成的关键文件

| 文件名 | 说明 |
|-------|------|
| debug_full_play_page.html | 完整播放页面 |
| algorithm_debug.html | API页面内容 |
| jsplayer_0.js | /jsplayer/a.js |
| jsplayer_1.js | /jsplayer/b.js (含eval混淆) |
| ckplayer.js | 播放器JS |
| lmm85_spider_final.py | 完整双模式爬虫 |

## 🎯 当前最佳实现

使用 **lmm85_spider_final.py** 中的双模式：
- 优先用 Playwright 捕获真实直链
- 失败则降级为返回播放页面
- 满足你的要求

---
**分析完成日期**: 2026-05-24
