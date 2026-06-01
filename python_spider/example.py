"""
示例：使用 Python 爬虫（测试分类筛选和推荐）
"""
import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_spider.xbiubiu import XBiubiu


def test_filters():
    """测试分类筛选功能"""
    print("=" * 60)
    print("测试分类筛选和推荐功能")
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

    # 1. 测试首页内容（包含筛选配置）
    print("\n[1] 测试首页内容（包含筛选配置）...")
    home_result = spider.home_content(filter=True)
    if home_result:
        home_data = json.loads(home_result)
        print("分类列表:")
        for cls in home_data.get('class', []):
            print(f"  - {cls['type_name']}: {cls['type_id']}")
        
        print("\n筛选配置:")
        filters = home_data.get('filters', {})
        for type_id, filter_items in filters.items():
            print(f"  分类 {type_id} 的筛选器:")
            for item in filter_items:
                values = [v['n'] for v in item['value'][:5]]
                print(f"    - {item['name']}: {values}...")

    # 2. 测试首页推荐视频
    print("\n[2] 测试首页推荐视频...")
    video_result = spider.home_video_content()
    if video_result:
        data = json.loads(video_result)
        print(f"推荐视频数量: {len(data.get('list', []))}")
        for i, vid in enumerate(data.get('list', [])[:3]):
            print(f"  [{i+1}] {vid.get('vod_name')}")

    # 3. 测试基础分类
    print("\n[3] 测试基础分类内容...")
    if home_result:
        home_data = json.loads(home_result)
        classes = home_data.get('class', [])
        if classes:
            # 测试第一个分类
            first_class = classes[0]
            print(f"使用分类: {first_class['type_name']} ({first_class['type_id']})")
            
            category_result = spider.category_content(first_class['type_id'], "1")
            if category_result:
                cat_data = json.loads(category_result)
                print(f"视频数量: {len(cat_data.get('list', []))}")
                for i, vid in enumerate(cat_data.get('list', [])[:3]):
                    print(f"  [{i+1}] {vid.get('vod_name')} - {vid.get('vod_remarks')}")

    # 4. 测试带筛选的分类
    print("\n[4] 测试带筛选条件的分类内容...")
    if home_result:
        home_data = json.loads(home_result)
        classes = home_data.get('class', [])
        if classes:
            # 找到有筛选配置的分类
            filters = home_data.get('filters', {})
            for cls in classes:
                type_id = cls['type_id']
                if type_id in filters:
                    print(f"测试分类: {cls['type_name']} ({type_id})")
                    
                    # 测试筛选条件：喜剧片
                    extend = {'class': '喜剧'}
                    print(f"  筛选条件: class=喜剧")
                    
                    filtered_result = spider.category_content(type_id, "1", filter=True, extend=extend)
                    if filtered_result:
                        filtered_data = json.loads(filtered_result)
                        print(f"  筛选后视频数量: {len(filtered_data.get('list', []))}")
                        for i, vid in enumerate(filtered_data.get('list', [])[:3]):
                            print(f"    [{i+1}] {vid.get('vod_name')}")
                    break

    # 5. 测试搜索
    print("\n[5] 测试搜索...")
    search_result = spider.search_content("电影")
    if search_result:
        search_data = json.loads(search_result)
        print(f"搜索结果数量: {len(search_data.get('list', []))}")
        for i, vid in enumerate(search_data.get('list', [])[:3]):
            print(f"  [{i+1}] {vid.get('vod_name')}")

    # 6. 测试详情
    print("\n[6] 测试详情页面...")
    if home_result:
        home_data = json.loads(home_result)
        classes = home_data.get('class', [])
        if classes:
            category_result = spider.category_content(classes[0]['type_id'], "1")
            if category_result:
                cat_data = json.loads(category_result)
                if cat_data.get('list'):
                    first_vod = cat_data['list'][0]
                    print(f"获取视频: {first_vod.get('vod_name')} 的详情")
                    
                    detail_result = spider.detail_content([first_vod['vod_id']])
                    if detail_result:
                        detail_data = json.loads(detail_result)
                        vod = detail_data['list'][0]
                        print(f"  名称: {vod.get('vod_name')}")
                        print(f"  导演: {vod.get('vod_director')}")
                        print(f"  主演: {vod.get('vod_actor')}")
                        print(f"  年份: {vod.get('vod_year')}")
                        print(f"  备注: {vod.get('vod_remarks')}")
                        print(f"  播放源: {vod.get('vod_play_from')}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_filters()
