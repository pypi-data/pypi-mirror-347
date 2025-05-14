from typing import Any, Dict, List
import httpx
from mcp.server.fastmcp import FastMCP
from loguru import logger

# Initialize FastMCP server
mcp = FastMCP("xhs_spider")

# Constants
NWS_API_BASE = "http://127.0.0.1:8001"


async def make_nws_request(url: str, data: dict) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, params=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(note: dict) -> str:
    #     """Format an alert feature into a readable string."""
    return f"""
用户: {note.get('note_type', '')}
帖子链接: {note.get('url', '')}
帖子类型: {note.get('severity', '暂无')}
帖子标题: {note.get('display_title', '暂无')}
帖子信息列表: {note.get('note_info_list', '暂无')}
"""

@mcp.tool()
async def spider_note(note_url: str, cookies: str) -> str | dict[str, Any] | None:
    """获取小红书一篇帖子内容

    Args:
        :param cookies: 小红书Cookies
        :param note_url: 小红书帖子链接
    """
    if not cookies or len(cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的小红书cookies")
    url = f"{NWS_API_BASE}/notes/item"
    data = {'note_url': note_url, 'cookies_str': cookies}
    result = await make_nws_request(url, data)
    if not result or "info" not in result:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"

    if not result["info"]:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"
    return result
    #
    # alerts = [format_alert(feature) for feature in data["features"]]
    # return "\n---\n".join(alerts)

@mcp.tool()
async def spider_user_notes(user_url: str, cookies: str) -> str | list[str]:
    """获取用户下的所有帖子

    Args:
        :param user_url: 用户主页链接
        :param cookies: 小红书Cookies
    """
    if not cookies or len(cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的小红书cookies")
    url = f"{NWS_API_BASE}/user/item"
    data = {'user_url': user_url, 'cookies_str': cookies}
    result = await make_nws_request(url, data)
    if not result or "list" not in result:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"

    if not result["list"]:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"
    return [format_alert(note) for note in result['list']]

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()