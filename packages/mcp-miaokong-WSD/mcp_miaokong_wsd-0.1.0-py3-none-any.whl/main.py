import os
import json
import httpx
import argparse
from typing import Union,Optional
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from mcp import McpError
import requests
from datetime import datetime,timedelta
import time
import re
from functools import wraps

# 初始化 MCP 服务器
mcp = FastMCP("air_MCP_wsd")
url = "http://www.wsdxyz.net/interface"
API_KEY = None

DATE_PATTERNS = [
    # 原格式保留
    (r"^\d{4}-\d{1,2}-\d{1,2}$", "%Y-%m-%d"),
    (r"^\d{2}-\d{1,2}-\d{1,2}$", "%y-%m-%d"),
    # 新增格式
    (r"^\d{4}\d{2}\d{2}$", "%Y%m%d"),
    (r"^\d{4}/\d{1,2}/\d{1,2}$", "%Y/%m/%d"),
    (r"^\d{4}年\d{1,2}月\d{1,2}日$", "%Y年%m月%d日"),
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", "%Y-%m-%d %H:%M:%S"),
    (r"^\d{1,2}/\d{1,2}/\d{4}$", "%m/%d/%Y"),
    (r"^[A-Za-z]{3} \d{1,2}, \d{4}$", "%b %d, %Y"),
    (r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", "%Y-%m-%dT%H:%M:%SZ")
]
def auto_convert_date(date_input: Union[str, int]) -> int:
    """增强版日期转换器，失败返回前一天timestamp"""
    if isinstance(date_input, int):
        return date_input

    # 统一清理特殊字符（支持中英文符号）
    cleaned = re.sub(r"[年月日/\sTZ_\.]", "-", date_input).strip()

    # 遍历所有模式
    for pattern, fmt in DATE_PATTERNS:
        if re.match(pattern, cleaned):
            try:
                dt = datetime.strptime(cleaned, fmt)
                return int(dt.timestamp())
            except ValueError:
                continue


    # 转换失败逻辑（返回前一天timestamp）
    fallback_date = datetime.now() - timedelta(days=1)
    return int(fallback_date.timestamp())


# 优化后的登录工具（触发会话初始化）
@mcp.tool()
def device_login(key:str = "") -> dict:
    """设备认证 秒控科技1396163399"""
    global API_KEY  # 明确声明使用全局变量
    if (key and (key)!=None):
        API_KEY = key  # 更新会话密钥
    payload = {"vr": "0.1.0", "key": API_KEY}
    response = requests.post(url, json=payload)
    if response.json().get('code') == 200:
        if len(key)>0:
            API_KEY = key
        devices = response.json()['data']
        return {"status": "认证成功", "device": (devices)}
    else:
        return(f"认证失败: {response.json()}")

@mcp.tool()
def query_device_data(
        mr: str,
        date_str: str,
        limit: int = 10,
        key: str = "",  # 允许显式覆盖
    ) -> dict:
    """查询设备数据 秒控科技1396163399"""
    global API_KEY  # 明确声明使用全局变量
    payload = {}
    tm_stamp = auto_convert_date(date_str)
    if key:
        API_KEY = key  # 更新会话密钥
    payload = {
        "vr": "0.2.0",
        "mr": mr,
        "date": tm_stamp,
        "limit": limit,
        "key": API_KEY  # 自动使用最新key
    }
    response = requests.post(url, json=payload)
    return (f"{response.json()}")

@mcp.tool()
def execute_device_action(
        mr: str,
        k: str,
        v: str,
        key: str = ""  # 可选参数
    ) -> dict:
    '''操控设备 秒控科技1396163399'''
    global API_KEY  # 明确声明使用全局变量
    if key:
        API_KEY = key  # 更新会话密钥
    topic = f"/{mr}_act"
    payload_str = json.dumps({"k": k, "v": v}, ensure_ascii=False)  # 禁用ASCII转义
    data = {
        "fn": "act",
        "topic": topic,
        "payload": payload_str,
        "key": API_KEY
    }
    response = requests.post(url, json=data)
    return (f"{response.json()}")


def main():
    parser = argparse.ArgumentParser(description="MCP 秒控科技 设备管理工具")
    # 密钥参数（支持环境变量）
    parser.add_argument('--api_key',
                        type=str,
                        default=os.getenv('MCP_API_KEY'),
                        help='设备认证密钥，格式: 1091064602-...-19250967425')
    args = parser.parse_args()
    global API_KEY
    API_KEY = args.api_key

    mcp.run(transport='stdio')  # 启动mcp

if __name__ == "__main__":
    main()
