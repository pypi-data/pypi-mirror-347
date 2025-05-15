import re
import urllib.parse

import aiohttp

from ..constant import COMMON_HEADER
from ..exception import ParseException
from .data import ParseResult
from .utils import get_redirect_url


class KuaishouParser:
    """快手解析器"""

    def __init__(self):
        self.headers = COMMON_HEADER
        # 通用第三方解析API
        self.api_url = "http://47.99.158.118/video-crack/v2/parse?content={}"

    async def parse_url(self, url: str) -> ParseResult:
        """解析快手链接获取视频信息

        Args:
            url: 快手视频链接

        Returns:
            ParseResult: 快手视频信息
        """
        raise NotImplementedError

    async def parse_url_by_api(self, url: str) -> ParseResult:
        """解析快手链接获取视频信息

        Args:
            url: 快手视频链接

        Returns:
            ParseResult: 快手视频信息
        """
        video_id = await self._extract_video_id(url)
        if not video_id:
            raise ParseException("无法从链接中提取视频ID")

        # 构造标准链接格式，用于API解析
        standard_url = f"https://www.kuaishou.com/short-video/{video_id}"
        # URL编码content参数避免查询字符串无效
        encoded_url = urllib.parse.quote(standard_url)
        api_url = self.api_url.format(encoded_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=self.headers) as resp:
                if resp.status != 200:
                    raise ParseException(f"解析API返回错误状态码: {resp.status}")

                result = await resp.json()

            # 根据API返回示例，成功时code应为0
            if result.get("code") != 0 or not result.get("data"):
                raise ParseException(f"解析API返回错误: {result.get('msg', '未知错误')}")

            data = result["data"]
            video_url = data.get("url")
            if not video_url:
                raise ParseException("未获取到视频直链")

            return ParseResult(
                # 字段名称与回退值
                title=data.get("title", "未知标题"),
                cover_url=data.get("imageUrl", ""),
                video_url=video_url,
                # API可能不提供作者信息
                author=data.get("name", "无名"),
            )

    async def _extract_video_id(self, url: str) -> str:
        """提取视频ID

        Args:
            url: 快手视频链接

        Returns:
            str: 视频ID
        """
        # 处理可能的短链接
        if "v.kuaishou.com" in url:
            url = await get_redirect_url(url)

        # 提取视频ID - 使用walrus operator和索引替代group()
        if "/fw/photo/" in url and (matched := re.search(r"/fw/photo/([^/?]+)", url)):
            return matched.group(1)
        elif "short-video" in url and (matched := re.search(r"short-video/([^/?]+)", url)):
            return matched.group(1)

        raise ParseException("无法从链接中提取视频ID")
