# 旺旺影视 (wwgz.cn) 网站结构分析

## 网站基本信息
- **网站地址**: https://vip.wwgz.cn:5200
- **User-Agent**: `Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1`
- **注意**: 必须使用手机UA访问，否则会返回404错误

## 分类结构

网站包含以下8个主要分类：

| ID | 分类名称 | URL格式 |
|----|---------|---------|
| 1 | 电影 | `/index.php?m=vod-list-id-1-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 2 | 连续剧 | `/index.php?m=vod-list-id-2-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 3 | 综艺 | `/index.php?m=vod-list-id-3-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 4 | 动漫 | `/index.php?m=vod-list-id-4-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 26 | 短剧 | `/index.php?m=vod-list-id-26-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 20 | 小姐姐 | `/index.php?m=vod-list-id-20-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |
| 31 | 音乐 | `/index.php?m=vod-list-id-31-pg-{page}-order--by-{order}-class-0-year-0-letter--area--lang-.html` |

### 排序方式 (order参数)
- `time`: 按时间排序
- `hits`: 按人气排序
- `score`: 按评分排序

### 筛选功能

#### 年代筛选
URL中添加 `year-{年份}` 参数，例如：
- `year-2026`: 筛选2026年
- `year-2025`: 筛选2025年
- `year-0`: 不限年代

#### 地区筛选
URL中添加 `area-{地区}` 参数（中文URL编码），例如：
- `area-大陆`: 筛选大陆地区
- `area-香港`: 筛选香港地区
- `area-台湾`: 筛选台湾地区

#### 类型筛选
URL中添加 `class-{类型ID}` 参数（需要查看具体类型ID）

#### 字母筛选
URL中添加 `letter-{字母}` 参数，用于按首字母筛选

## 搜索功能

### 搜索URL格式
```
/index.php?m=vod-search&wd={关键词}
```

### 搜索示例
搜索"郑战才"：
```
/index.php?m=vod-search&wd=%E9%83%91%E6%88%98%E6%89%8D
```

## 详情页结构

### 详情页URL格式
```
/vod-detail-id-{资源ID}.html
```

### 详情页包含信息
- 标题（title）
- 封面图片（pic）
- 主演（actor）
- 导演（director）
- 年代（year）
- 更新日期（update_time）
- 简介（content）
- 播放列表（play_list）

## 播放页结构

### 播放页URL格式
```
/vod-play-id-{资源ID}-src-{线路号}-num-{集数}.html
```

### 示例
```
/vod-play-id-90063-src-1-num-1.html
```

## 列表页HTML结构

```html
<li><a href="/vod-detail-id-{ID}.html" title="{标题}">
  <div class="pic">
    <img data-echo="{图片URL}" src="{图片URL}">
    <span class="sBg"></span>
    <span class="sBottom">
      <span><em>{评分}</em></span>
    </span>
  </div>
  <span class="sTit">{标题}</span>
  <span class="sDes">主演：{主演信息}</span>
</a></li>
```

## 详情页HTML关键元素

### 影片信息
- 状态: `<div class="desc_item"><span>状态:&nbsp;</span>{内容}</div>`
- 主演: `<div class="desc_item"><span>主演:&nbsp;</span>{内容}</div>`
- 导演: `<div class="desc_item"><span>导演:&nbsp;</span>{内容}</div>`
- 年代: `<div class="desc_item"><span>年代:&nbsp;</span>{内容}</div>`

### 简介
```html
<article class="detail-con">
  <span>简&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;介：{简介内容}</span>
</article>
```

### 播放列表
```html
<div id="uvw" class="numList">
  <ul>
    <li><a href="/vod-play-id-{ID}-src-1-num-1.html" target="_self">第01集</a></li>
    <li><a href="/vod-play-id-{ID}-src-1-num-2.html" target="_self">第02集</a></li>
  </ul>
</div>
```

## 分页信息

列表页底部包含分页信息：
```html
<div class="page">
  共20722条数据 当前:1/691页
  <a href="/vod-list-id-1-pg-2-order--by-time-class-0-year-0-letter--area--lang-.html">2</a>
  <a href="/vod-list-id-1-pg-3-order--by-time-class-0-year-0-letter--area--lang-.html">3</a>
  ...
</div>
```

## 爬虫文件说明

### wwgz.json
适用于TVBox等播放器的JSON格式配置文件，包含所有解析规则。

### wwgz.js
Node.js版本的爬虫模块，提供以下功能：
- `fetchPage(url, callback)`: 获取页面内容
- `parseList(html)`: 解析列表页
- `parseDetail(html)`: 解析详情页
- `getCategories()`: 获取分类列表
- `getCategoryUrl(typeId, page, order)`: 生成分类URL
- `getDetailUrl(id)`: 生成详情页URL
- `getPlayUrl(id, src, num)`: 生成播放页URL
- `getSearchUrl(keyword)`: 生成搜索URL

## 使用示例

### Node.js使用示例

```javascript
const wwgz = require('./wwgz.js');

// 获取电影分类第一页
wwgz.fetchPage(wwgz.getCategoryUrl('1', 1), (err, html) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  
  const items = wwgz.parseList(html);
  console.log('电影列表：', items);
});

// 获取资源详情
wwgz.fetchPage(wwgz.getDetailUrl('90063'), (err, html) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  
  const detail = wwgz.parseDetail(html);
  console.log('详情：', detail);
});

// 搜索资源
wwgz.fetchPage(wwgz.getSearchUrl('东北往事'), (err, html) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  
  const items = wwgz.parseList(html);
  console.log('搜索结果：', items);
});
```

## 注意事项

1. **必须使用手机UA**: 网站会检测User-Agent，非手机UA会返回404
2. **编码问题**: 搜索关键词需要使用URL编码
3. **HTTPS**: 网站使用HTTPS协议
4. **数据量**: 电影分类有20722条数据，691页
5. **图片懒加载**: 网站使用data-echo属性存储真实图片URL

## 更新日志

- 2026-05-23: 完成网站结构分析和爬虫创建
