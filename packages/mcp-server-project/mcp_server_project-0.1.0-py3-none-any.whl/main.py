from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os
from bs4 import BeautifulSoup
import json

load_dotenv()
# 初始化服务器
mcp = FastMCP("tech_news")

USER_AGENT = "news-app/1.0"

NEWS_SITES = {
    "arstechnica": "https://arstechnica.com"
}


async def fetch_news(url: str):
    """从指定的新闻网站抓取并总结最新新闻。"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs[:5]])
            return text
        except httpx.TimeoutException:
            return "Timeout error"


@mcp.tool()
async def get_tech_news(source: str):
    """
    从特定的科技新闻源获取最新新闻。
    参数：
    source：新闻源名称（例如，"arstechnica"或"techcrunch"）。
    返回：
    最新新闻的简要摘要。
    """
    if source not in NEWS_SITES:
        raise ValueError(f"Source {source} is not supported.")

    news_text = await fetch_news(NEWS_SITES[source])
    return news_text


if __name__ == "__main__":
    mcp.run(transport="stdio")