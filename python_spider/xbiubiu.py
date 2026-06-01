"""
XBiubiu 通用爬虫实现
"""
import json
import re
from typing import Dict, List, Optional
from .spider import Spider


class XBiubiu(Spider):
    """通用配置驱动爬虫"""

    def home_content(self, filter: bool = False) -> str:
        """首页内容 - 返回分类列表"""
        try:
            self.fetch_rule()
            result = {}
            classes = []

            fenlei_str = self.get_rule_val("fenlei", "")
            if fenlei_str:
                fenleis = fenlei_str.split("#")
                for fenlei in fenleis:
                    info = fenlei.split("$")
                    if len(info) >= 2:
                        classes.append({
                            "type_name": info[0],
                            "type_id": info[1]
                        })

            result["class"] = classes
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"Home content error: {e}")
            return ""

    def home_video_content(self) -> str:
        """首页推荐视频 - 从第一个分类获取推荐"""
        try:
            self.fetch_rule()
            if self.get_rule_val("shouye") == "1":
                videos = []
                fenlei_str = self.get_rule_val("fenlei", "")
                if fenlei_str:
                    fenleis = fenlei_str.split("#")
                    for fenlei in fenleis:
                        info = fenlei.split("$")
                        if len(info) >= 2:
                            data = self._category(info[1], "1", False, {})
                            if data and "list" in data:
                                vids = data["list"]
                                for i, vid in enumerate(vids):
                                    if i < 5:
                                        videos.append(vid)
                                    else:
                                        break
                        if len(videos) >= 30:
                            break

                result = {"list": videos}
                return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"Home video content error: {e}")
        return ""

    def _category(self, tid: str, pg: str, filter: bool = False, extend: Optional[Dict] = None) -> Optional[Dict]:
        """内部分类获取方法"""
        try:
            self.fetch_rule()
            web_url = self.get_rule_val("url") + tid + pg + self.get_rule_val("houzhui")
            html = self.fetch(web_url)
            parse_content = html

            # 是否二次截取
            shifouercijiequ = self.get_rule_val("shifouercijiequ") == "1"
            if shifouercijiequ:
                jiequqian = self.get_rule_val("jiequqian")
                jiequhou = self.get_rule_val("jiequhou")
                contents = self.sub_content(html, jiequqian, jiequhou)
                if contents:
                    parse_content = contents[0]

            jiequshuzuqian = self.get_rule_val("jiequshuzuqian")
            jiequshuzuhou = self.get_rule_val("jiequshuzuhou")
            videos = []
            jiequ_contents = self.sub_content(parse_content, jiequshuzuqian, jiequshuzuhou)

            for jiequ_content in jiequ_contents:
                try:
                    title = self.sub_content(jiequ_content, self.get_rule_val("biaotiqian"), self.get_rule_val("biaotihou"))[0]
                    pic = self.sub_content(jiequ_content, self.get_rule_val("tupianqian"), self.get_rule_val("tupianhou"))[0]
                    pic = self.fix_url(web_url, pic)
                    link = self.sub_content(jiequ_content, self.get_rule_val("lianjieqian"), self.get_rule_val("lianjiehou"))[0]

                    mark = ""
                    if self.get_rule_val("gengxinqian") and self.get_rule_val("gengxinhou"):
                        try:
                            mark_content = self.sub_content(jiequ_content, self.get_rule_val("gengxinqian"), self.get_rule_val("gengxinhou"))
                            if mark_content:
                                mark = re.sub(r"\s+", "", mark_content[0])
                                mark = re.sub(r"\&[a-zA-Z]{1,10};", "", mark)
                                mark = re.sub(r"<[^>]*>", "", mark)
                        except Exception:
                            pass

                    videos.append({
                        "vod_id": f"{title}$$$${pic}$$$${link}",
                        "vod_name": title,
                        "vod_pic": pic,
                        "vod_remarks": mark
                    })
                except Exception as e:
                    print(f"Parse video error: {e}")
                    continue

            return {
                "page": pg,
                "pagecount": 9999,
                "limit": 90,
                "total": 99999,
                "list": videos
            }
        except Exception as e:
            print(f"Category error: {e}")
        return None

    def category_content(self, tid: str, pg: str, filter: bool = False, extend: Optional[Dict] = None) -> str:
        """分类内容"""
        result = self._category(tid, pg, filter, extend)
        return json.dumps(result, ensure_ascii=False) if result else ""

    def detail_content(self, ids: List[str]) -> str:
        """详情内容"""
        try:
            self.fetch_rule()
            id_info = ids[0].split("$$$")
            web_url = self.get_rule_val("url") + id_info[2]
            html = self.fetch(web_url)
            parse_content = html

            # 播放列表二次截取
            bfshifouercijiequ = self.get_rule_val("bfshifouercijiequ") == "1"
            if bfshifouercijiequ:
                jiequqian = self.get_rule_val("bfjiequqian")
                jiequhou = self.get_rule_val("bfjiequhou")
                contents = self.sub_content(html, jiequqian, jiequhou)
                if contents:
                    parse_content = contents[0]

            play_list = []
            jiequshuzuqian = self.get_rule_val("bfjiequshuzuqian")
            jiequshuzuhou = self.get_rule_val("bfjiequshuzuhou")
            bfyshifouercijiequ = self.get_rule_val("bfyshifouercijiequ") == "1"
            jiequ_contents = self.sub_content(parse_content, jiequshuzuqian, jiequshuzuhou)

            for jiequ_content in jiequ_contents:
                try:
                    parse_jq_content = jiequ_content
                    if bfyshifouercijiequ:
                        contents = self.sub_content(jiequ_content, self.get_rule_val("bfyjiequqian"), self.get_rule_val("bfyjiequhou"))
                        if contents:
                            parse_jq_content = contents[0]

                    last_parse_contents = self.sub_content(parse_jq_content, self.get_rule_val("bfyjiequshuzuqian"), self.get_rule_val("bfyjiequshuzuhou"))
                    vod_items = []

                    for last_parse in last_parse_contents:
                        title = self.sub_content(last_parse, self.get_rule_val("bfbiaotiqian"), self.get_rule_val("bfbiaotihou"))[0]
                        link = self.sub_content(last_parse, self.get_rule_val("bflianjieqian"), self.get_rule_val("bflianjiehou"))[0]
                        vod_items.append(f"{title}${link}")

                    play_list.append("#".join(vod_items))
                except Exception as e:
                    print(f"Parse playlist error: {e}")
                    continue

            cover = id_info[1]
            title = id_info[0]
            area = ""
            director = ""
            actor = ""
            desc = ""
            remark = ""
            year = ""
            category = ""

            # 获取分类
            if self.get_rule_val("leixinqian") and self.get_rule_val("leixinhou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("leixinqian"), self.get_rule_val("leixinhou"))
                    if contents:
                        category = re.sub(r"\s+", "", contents[0])
                        category = re.sub(r"\&[a-zA-Z]{1,10};", "", category)
                        category = re.sub(r"<[^>]*>", "", category)
                except Exception:
                    pass

            # 获取年份
            if self.get_rule_val("niandaiqian") and self.get_rule_val("niandaihou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("niandaiqian"), self.get_rule_val("niandaihou"))
                    if contents:
                        year = re.sub(r"\s+", "", contents[0])
                        year = re.sub(r"\&[a-zA-Z]{1,10};", "", year)
                        year = re.sub(r"<[^>]*>", "", year)
                except Exception:
                    pass

            # 获取状态/备注
            if self.get_rule_val("zhuangtaiqian") and self.get_rule_val("zhuangtaihou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("zhuangtaiqian"), self.get_rule_val("zhuangtaihou"))
                    if contents:
                        remark = contents[0]
                except Exception:
                    pass

            # 获取主演
            if self.get_rule_val("zhuyanqian") and self.get_rule_val("zhuyanhou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("zhuyanqian"), self.get_rule_val("zhuyanhou"))
                    if contents:
                        actor = re.sub(r"\s+", "", contents[0])
                except Exception:
                    pass

            # 获取导演
            if self.get_rule_val("daoyanqian") and self.get_rule_val("daoyanhou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("daoyanqian"), self.get_rule_val("daoyanhou"))
                    if contents:
                        director = re.sub(r"\s+", "", contents[0])
                except Exception:
                    pass

            # 获取剧情
            if self.get_rule_val("juqingqian") and self.get_rule_val("juqinghou"):
                try:
                    contents = self.sub_content(html, self.get_rule_val("juqingqian"), self.get_rule_val("juqinghou"))
                    if contents:
                        desc = contents[0]
                except Exception:
                    pass

            vod = {
                "vod_id": ids[0],
                "vod_name": title,
                "vod_pic": cover,
                "type_name": category,
                "vod_year": year,
                "vod_area": area,
                "vod_remarks": remark,
                "vod_actor": actor,
                "vod_director": director,
                "vod_content": desc
            }

            play_from = [f"播放列表{i+1}" for i in range(len(play_list))]
            vod["vod_play_from"] = "$$$".join(play_from)
            vod["vod_play_url"] = "$$$".join(play_list)

            result = {"list": [vod]}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"Detail content error: {e}")
        return ""

    def player_content(self, flag: str, id: str, vip_flags: List[str]) -> str:
        """播放内容"""
        try:
            self.fetch_rule()
            web_url = self.get_rule_val("url") + id
            result = {
                "parse": 1,
                "playUrl": "",
                "url": web_url
            }
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"Player content error: {e}")
        return ""

    def search_content(self, key: str, quick: bool = False) -> str:
        """搜索内容"""
        try:
            self.fetch_rule()
            ssmoshi_json = self.get_rule_val("ssmoshi") == "0"
            web_url_tmp = self.get_rule_val("url") + self.get_rule_val("sousuoqian") + key + self.get_rule_val("sousuohou")
            web_url = web_url_tmp.split(";")[0]
            is_post = ";post" in web_url_tmp

            if is_post:
                web_content = self.fetch_post(web_url)
            else:
                web_content = self.fetch(web_url)

            videos = []

            if ssmoshi_json:
                # JSON 模式
                data = json.loads(web_content)
                vod_array = data.get("list", [])
                for vod in vod_array:
                    name = vod.get(self.get_rule_val("jsname"), "").strip()
                    vid = str(vod.get(self.get_rule_val("jsid"), "")).strip()
                    pic = vod.get(self.get_rule_val("jspic"), "").strip()
                    pic = self.fix_url(web_url, pic)

                    videos.append({
                        "vod_id": f"{name}$$$${pic}$$$${self.get_rule_val('sousuohouzhui')}{vid}",
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": ""
                    })
            else:
                # HTML 模式
                parse_content = web_content
                shifouercijiequ = self.get_rule_val("sousuoshifouercijiequ") == "1"
                if shifouercijiequ:
                    jiequqian = self.get_rule_val("ssjiequqian")
                    jiequhou = self.get_rule_val("ssjiequhou")
                    contents = self.sub_content(web_content, jiequqian, jiequhou)
                    if contents:
                        parse_content = contents[0]

                jiequshuzuqian = self.get_rule_val("ssjiequshuzuqian")
                jiequshuzuhou = self.get_rule_val("ssjiequshuzuhou")
                jiequ_contents = self.sub_content(parse_content, jiequshuzuqian, jiequshuzuhou)

                for jiequ_content in jiequ_contents:
                    try:
                        title = self.sub_content(jiequ_content, self.get_rule_val("ssbiaotiqian"), self.get_rule_val("ssbiaotihou"))[0]
                        pic = self.sub_content(jiequ_content, self.get_rule_val("sstupianqian"), self.get_rule_val("sstupianhou"))[0]
                        pic = self.fix_url(web_url, pic)
                        link = self.sub_content(jiequ_content, self.get_rule_val("sslianjieqian"), self.get_rule_val("sslianjiehou"))[0]

                        videos.append({
                            "vod_id": f"{title}$$$${pic}$$$${link}",
                            "vod_name": title,
                            "vod_pic": pic,
                            "vod_remarks": ""
                        })
                    except Exception:
                        continue

            result = {"list": videos}
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"Search content error: {e}")
        return ""
