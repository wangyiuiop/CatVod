# CatVod Python 爬虫

这是一个用 Python 实现的 CatVod 爬虫框架，支持与 Java 版本相同的配置格式。

## 目录结构

```
/workspace/
├── python_spider/
│   ├── __init__.py       # 包初始化
│   ├── spider.py         # 爬虫基类
│   ├── xbiubiu.py        # 通用配置爬虫（类似 Java 版 XBiubiu）
│   ├── example.py        # 示例代码
│   └── server.py         # HTTP 服务器
├── XBiubiu/              # 配置文件目录（与 Java 版本共用）
├── requirements.txt      # Python 依赖
└── PYTHON_README.md      # 本文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速使用

### 1. 作为库使用

```python
from python_spider.xbiubiu import XBiubiu

# 创建爬虫并加载配置
spider = XBiubiu()
spider.init(extend=config_json_string)  # 或使用 extend=config_url

# 首页内容
home = spider.home_content()

# 首页推荐
videos = spider.home_video_content()

# 分类内容
category = spider.category_content(type_id, "1")

# 详情内容
detail = spider.detail_content([vod_id])

# 搜索
search = spider.search_content("关键词")
```

### 2. 运行示例

```bash
python -m python_spider.example
```

### 3. 启动 HTTP 服务器

```bash
# 先安装 flask
pip install flask

# 启动服务器
python -m python_spider.server
```

服务器会在 `http://localhost:8000` 启动，提供以下 API：

- `/api/<配置名>/home` - 首页内容
- `/api/<配置名>/homeVideo` - 首页推荐
- `/api/<配置名>/category?tid=xxx&pg=1` - 分类内容
- `/api/<配置名>/detail?ids=xxx` - 详情内容
- `/api/<配置名>/search?key=xxx` - 搜索

示例：
```
http://localhost:8000/api/在线之家/home
http://localhost:8000/api/在线之家/search?key=电影
```

## 配置文件说明

配置文件格式与 Java 版完全一致，保存在 `XBiubiu/` 目录下。

主要配置项：
- `name`: 站点名称
- `url`: 站点地址
- `fenlei`: 分类配置（格式：分类名$分类路径#...）
- `shouye`: 是否显示首页推荐（1/0）
- `jiequshuzuqian`/`jiequshuzuhou`: 视频列表截取标签
- `tupianqian`/`tupianhou`: 图片截取标签
- `biaotiqian`/`biaotihou`: 标题截取标签
- `lianjieqian`/`lianjiehou`: 链接截取标签
- 等等...

详细配置说明请参考 Java 版文档或现有配置文件示例。

## 扩展开发

你可以继承 `Spider` 基类来实现自定义爬虫：

```python
from python_spider.spider import Spider

class MySpider(Spider):
    def home_content(self, filter=False):
        # 实现你的逻辑
        pass
    
    # 实现其他必需方法...
```
