"""
CatVod Python 爬虫基础模块
提供爬虫基类和通用功能
"""
import abc
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urljoin, urlencode
import requests


class Spider(abc.ABC):
    """爬虫基类"""

    def __init__(self):
        self.session = requests.Session()
        self.ext = None
        self.rule = None

    def init(self, context: Optional[Any] = None, extend: Optional[str] = None):
        """初始化爬虫"""
        if extend:
            self.ext = extend
            self.fetch_rule()

    def fetch_rule(self):
        """获取配置规则"""
        if self.rule is None and self.ext:
            try:
                if self.ext.startswith('http'):
                    resp = self.session.get(self.ext, timeout=10)
                    resp.raise_for_status()
                    self.rule = resp.json()
                else:
                    self.rule = json.loads(self.ext)
            except Exception as e:
                print(f"Fetch rule error: {e}")
                self.rule = {}

    def get_rule_val(self, key: str, default_val: str = "") -> str:
        """获取配置值"""
        if self.rule:
            val = self.rule.get(key, default_val)
            if val == "空" or val is None:
                return default_val
            return str(val)
        return default_val

    def get_headers(self, url: str) -> Dict[str, str]:
        """获取请求头"""
        ua = self.get_rule_val("UserW", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        if not ua or ua == "空":
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        return {"User-Agent": ua}

    def fetch(self, web_url: str, params: Optional[Dict] = None) -> str:
        """获取网页内容"""
        try:
            headers = self.get_headers(web_url)
            resp = self.session.get(web_url, headers=headers, params=params, timeout=15)
            resp.raise_for_status()
            return resp.text.replace("\r", "").replace("\n", "")
        except Exception as e:
            print(f"Fetch error: {e}")
            return ""

    def fetch_post(self, web_url: str, data: Optional[Dict] = None) -> str:
        """POST 请求"""
        try:
            headers = self.get_headers(web_url)
            resp = self.session.post(web_url, headers=headers, data=data, timeout=15)
            resp.raise_for_status()
            return resp.text.replace("\r", "").replace("\n", "")
        except Exception as e:
            print(f"Fetch post error: {e}")
            return ""

    @staticmethod
    def sub_content(content: str, start_flag: str, end_flag: str) -> List[str]:
        """截取内容"""
        result = []
        try:
            if not start_flag or not end_flag:
                return result
            pattern = re.compile(re.escape(start_flag) + r"(.*?)" + re.escape(end_flag))
            for match in pattern.finditer(content):
                result.append(match.group(1))
        except Exception as e:
            print(f"Sub content error: {e}")
        return result

    @staticmethod
    def fix_url(base_url: str, url: str) -> str:
        """修复 URL"""
        if not url:
            return ""
        if url.startswith("http"):
            return url
        return urljoin(base_url, url)

    @abc.abstractmethod
    def home_content(self, filter: bool = False) -> str:
        """首页内容"""
        pass

    @abc.abstractmethod
    def home_video_content(self) -> str:
        """首页推荐视频"""
        pass

    @abc.abstractmethod
    def category_content(self, tid: str, pg: str, filter: bool = False, extend: Optional[Dict] = None) -> str:
        """分类内容"""
        pass

    @abc.abstractmethod
    def detail_content(self, ids: List[str]) -> str:
        """详情内容"""
        pass

    @abc.abstractmethod
    def player_content(self, flag: str, id: str, vip_flags: List[str]) -> str:
        """播放内容"""
        pass

    @abc.abstractmethod
    def search_content(self, key: str, quick: bool = False) -> str:
        """搜索内容"""
        pass
