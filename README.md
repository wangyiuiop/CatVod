# ylys.tv 视频网站 JavaScript API 文档

## 概述

本项目分析了 ylys.tv 网站的视频生成和解密逻辑，并提供了完整的 JavaScript API 接口。

## 核心模块

### 1. CatAPI - API 接口模块

提供所有与后端交互的功能：

```javascript
// 获取首页推荐
CatAPI.getHomePage(page, limit)
CatAPI.getRecommendVideos(limit)

// 获取分类列表
CatAPI.getCategories()

// 获取分类视频
CatAPI.getCategoryVideos(typeId, page, limit, params)

// 获取视频详情
CatAPI.getVideoDetail(vodId)

// 获取播放器信息
CatAPI.getVideoPlayer(id, sid, nid)

// 搜索视频
CatAPI.search(keyword, page, limit)

// 热门视频
CatAPI.getHotVideos(limit)

// 最新视频
CatAPI.getLatestVideos(limit)
```

### 2. CatUI - UI 组件模块

提供常用的 UI 组件：

```javascript
// 创建视频卡片
CatUI.createVideoCard(video, options)

// 创建分类列表
CatUI.createCategoryList(categories)

// 创建视频网格
CatUI.createVideoGrid(videos, options)

// 创建分页
CatUI.createPagination(currentPage, totalPages)

// 创建搜索栏
CatUI.createSearchBar(containerId, options)

// 创建首页
CatUI.createHomePage(containerId, options)

// 创建分类页
CatUI.createCategoryPage(containerId, typeId, options)

// 创建搜索页
CatUI.createSearchPage(containerId, keyword, options)
```

### 3. CatPlayer - 视频播放器模块

处理视频加密和解密逻辑：

```javascript
// 解密视频 URL
CatPlayer.decryptUrl(encryptedUrl, encryptType)

// 加密视频 URL
CatPlayer.encryptUrl(url, encryptType)

// 解析播放器数据
CatPlayer.parsePlayerData(playerData)

// 创建 HTML5 视频播放器
CatPlayer.createVideoPlayer(containerId, videoUrl, options)

// 创建 iframe 播放器
CatPlayer.createIframePlayer(containerId, playerUrl, options)

// 初始化播放器
CatPlayer.init(playerData, containerId, options)
```

### 4. CatRouter - 路由模块

简单的客户端路由系统：

```javascript
// 初始化路由
CatRouter.init()

// 添加路由
CatRouter.addRoute('/video/:id', function(id) {
    // 处理逻辑
})

// 导航到指定路径
CatRouter.navigate('/video/123')
```

## 加密模式

网站支持三种加密模式：

- **encrypt = '0'**: 无加密，直接使用原始 URL
- **encrypt = '1'**: 使用 `unescape()` 解码
- **encrypt = '2'**: 使用 Base64 解码 + `unescape()` 解码

## 使用示例

### 基本使用

```html
<!DOCTYPE html>
<html>
<head>
    <title>ylys.tv 示例</title>
</head>
<body>
    <div id="app"></div>
    <script src="cat.js"></script>
    <script>
        // 显示首页
        CatUI.createHomePage('app', {
            limit: 12,
            gridOptions: {
                columnWidth: '250px',
                gap: '20px'
            },
            onVideoClick: function(video) {
                console.log('点击视频:', video);
                showDetail(video.vod_id);
            }
        });
    </script>
</body>
</html>
```

### 搜索功能

```javascript
// 初始化搜索栏
CatUI.createSearchBar('searchContainer', {
    placeholder: '搜索视频...',
    onSearch: function(keyword) {
        CatUI.createSearchPage('contentContainer', keyword, {
            onVideoClick: function(video) {
                // 处理视频点击
            }
        });
    }
});
```

### 分类页面

```javascript
// 显示分类页面
CatUI.createCategoryPage('contentContainer', 1, {
    title: '电影',
    limit: 20,
    params: {
        area: '',
        year: '',
        order: 'time'
    },
    onVideoClick: function(video) {
        // 处理视频点击
    }
});
```

### 视频播放

```javascript
// 获取播放器信息并初始化
CatAPI.getVideoPlayer(vodId, sid, nid).then(function(response) {
    var playerData = {
        encrypt: response.encrypt,
        url: response.url,
        from: response.from
    };
    
    CatPlayer.init(playerData, 'playerContainer', {
        width: '100%',
        height: '500px'
    });
});
```

## API 响应格式

### 视频列表响应

```json
{
    "page": 1,
    "pagecount": 10,
    "limit": 20,
    "total": 200,
    "list": [
        {
            "vod_id": 123575,
            "vod_name": "地狱占星师",
            "vod_sub": "第9集完结",
            "vod_pic": "https://example.com/pic.jpg",
            "vod_remarks": "HD",
            "vod_year": "2026",
            "type_name": "剧情",
            "vod_area": "日本",
            "vod_director": "泷本智行",
            "vod_actor": "户田惠梨香"
        }
    ]
}
```

### 视频详情响应

```json
{
    "info": {
        "vod_id": 123575,
        "vod_name": "地狱占星师",
        "vod_pic": "https://example.com/pic.jpg",
        "vod_content": "详细描述...",
        "vod_play_list": {
            "1": [
                {"title": "第1集", "url": "..."},
                {"title": "第2集", "url": "..."}
            ]
        }
    }
}
```

### 播放器响应

```json
{
    "encrypt": "2",
    "url": "base64编码的URL",
    "from": "dplayer",
    "server": "no"
}
```

## URL 构建

```javascript
// 构建分类 URL
CatAPI.buildCategoryUrl(1, {area: '日本', year: '2026'})

// 构建详情页 URL
CatAPI.buildDetailUrl(123575)

// 构建播放页 URL
CatAPI.buildPlayUrl(123575, 1, 1)

// 构建搜索页 URL
CatAPI.buildSearchUrl('地狱占星师')
```

## 注意事项

1. 所有 API 请求都使用 CORS，请确保在支持的浏览器环境中运行
2. 部分 API 可能需要认证或特殊权限
3. 视频 URL 可能有有效期限制，请及时使用
4. 请遵守网站的使用条款和版权规定

## 文件结构

```
/workspace/
├── cat.js        # 核心 JavaScript API
├── index.html    # 示例页面
└── README.md     # 本文档
```

## 技术栈

- JavaScript ES6+
- XMLHttpRequest / Fetch API
- Promise 异步编程
- HTML5 Video Player
- Responsive Grid Layout

## 许可证

本项目仅供学习和研究使用，请勿用于商业目的。
