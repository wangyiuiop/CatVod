"""
示例：使用 Python 爬虫
"""
import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_spider.xbiubiu import XBiubiu


def test_zxzj():
    """测试在线之家"""
    print("=" * 60)
    print("测试在线之家爬虫")
    print("=" * 60)

    # 配置文件路径
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "XBiubiu", "在线之家.json")

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return

    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()

    # 创建爬虫
    spider = XBiubiu()
    spider.init(extend=config_content)

    # 1. 测试首页内容
    print("\n[1] 测试首页内容...")
    home_result = spider.home_content()
    print("首页内容:")
    print(json.dumps(json.loads(home_result), ensure_ascii=False, indent=2) if home_result else "无结果")

    # 2. 测试首页推荐视频
    print("\n[2] 测试首页推荐视频...")
    video_result = spider.home_video_content()
    if video_result:
        data = json.loads(video_result)
        print(f"推荐视频数量: {len(data.get('list', []))}")
        if data.get('list'):
            print("第一个视频:")
            print(json.dumps(data['list'][0], ensure_ascii=False, indent=2))

    # 3. 测试分类内容
    print("\n[3] 测试分类内容...")
    # 获取第一个分类
    if home_result:
        home_data = json.loads(home_result)
        classes = home_data.get('class', [])
        if classes:
            first_tid = classes[0]['type_id']
            print(f"使用分类: {classes[0]['type_name']} ({first_tid})")
            category_result = spider.category_content(first_tid, "1")
            if category_result:
                cat_data = json.loads(category_result)
                print(f"分类视频数量: {len(cat_data.get('list', []))}")
                if cat_data.get('list'):
                    print("第一个视频:")
                    print(json.dumps(cat_data['list'][0], ensure_ascii=False, indent=2))

                    # 4. 测试详情内容
                    print("\n[4] 测试详情内容...")
                    first_vod_id = cat_data['list'][0]['vod_id']
                    detail_result = spider.detail_content([first_vod_id])
                    if detail_result:
                        detail_data = json.loads(detail_result)
                        print("详情内容:")
                        print(json.dumps(detail_data, ensure_ascii=False, indent=2))

    # 5. 测试搜索
    print("\n[5] 测试搜索...")
    search_result = spider.search_content("电影")
    if search_result:
        search_data = json.loads(search_result)
        print(f"搜索结果数量: {len(search_data.get('list', []))}")
        if search_data.get('list'):
            print("第一个搜索结果:")
            print(json.dumps(search_data['list'][0], ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_zxzj()
