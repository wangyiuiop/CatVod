"""
简单的 HTTP 服务器，提供爬虫 API
"""
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 导入爬虫
from python_spider.xbiubiu import XBiubiu

# 存储已初始化的爬虫实例
spiders = {}


def get_spider(config_name):
    """获取或创建爬虫实例"""
    if config_name not in spiders:
        # 尝试从 XBiubiu 目录加载配置
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "XBiubiu", f"{config_name}.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
            spider = XBiubiu()
            spider.init(extend=config_content)
            spiders[config_name] = spider
        else:
            return None
    return spiders[config_name]


@app.route('/')
def index():
    return """
    <h1>CatVod Python 爬虫 API</h1>
    <p>可用接口：</p>
    <ul>
        <li>/api/&lt;config&gt;/home?filter=false</li>
        <li>/api/&lt;config&gt;/homeVideo</li>
        <li>/api/&lt;config&gt;/category?tid=&lt;type_id&gt;&amp;pg=1</li>
        <li>/api/&lt;config&gt;/detail?ids=&lt;vod_id&gt;</li>
        <li>/api/&lt;config&gt;/search?key=&lt;keyword&gt;</li>
    </ul>
    <p>示例：/api/在线之家/home</p>
    """


@app.route('/api/<config>/home')
def home(config):
    spider = get_spider(config)
    if not spider:
        return jsonify({"error": "Config not found"}), 404
    filter_flag = request.args.get('filter', 'false').lower() == 'true'
    result = spider.home_content(filter_flag)
    return jsonify(json.loads(result)) if result else jsonify({})


@app.route('/api/<config>/homeVideo')
def home_video(config):
    spider = get_spider(config)
    if not spider:
        return jsonify({"error": "Config not found"}), 404
    result = spider.home_video_content()
    return jsonify(json.loads(result)) if result else jsonify({})


@app.route('/api/<config>/category')
def category(config):
    spider = get_spider(config)
    if not spider:
        return jsonify({"error": "Config not found"}), 404
    tid = request.args.get('tid', '')
    pg = request.args.get('pg', '1')
    filter_flag = request.args.get('filter', 'false').lower() == 'true'
    result = spider.category_content(tid, pg, filter_flag, {})
    return jsonify(json.loads(result)) if result else jsonify({})


@app.route('/api/<config>/detail')
def detail(config):
    spider = get_spider(config)
    if not spider:
        return jsonify({"error": "Config not found"}), 404
    ids = request.args.get('ids', '').split(',')
    result = spider.detail_content(ids)
    return jsonify(json.loads(result)) if result else jsonify({})


@app.route('/api/<config>/search')
def search(config):
    spider = get_spider(config)
    if not spider:
        return jsonify({"error": "Config not found"}), 404
    key = request.args.get('key', '')
    quick = request.args.get('quick', 'false').lower() == 'true'
    result = spider.search_content(key, quick)
    return jsonify(json.loads(result)) if result else jsonify({})


if __name__ == '__main__':
    print("启动 CatVod Python 爬虫服务器...")
    app.run(host='0.0.0.0', port=8000, debug=True)
