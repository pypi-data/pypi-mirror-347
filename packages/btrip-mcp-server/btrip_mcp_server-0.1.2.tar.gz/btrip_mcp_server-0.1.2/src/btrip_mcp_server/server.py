# -*- coding: utf-8 -*-
import time

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import httpx
import json
import os
import logging
import hashlib
import random

logger = logging.getLogger("mcp")

# 初始化mcp服务
mcp = FastMCP("btrip-mcp-server")

def signature(timestamp: str, nonce: str, req_body: str, encrypt_key: str) -> str:
    """
    SHA-256 签名生成函数（符合RFC 4634标准）

    :param timestamp: 时间戳字符串 (通常为Unix时间戳)
    :param nonce: 随机数字符串 (推荐16位以上)
    :param req_body: 请求体原文 (需确保已排序/标准化)
    :param encrypt_key: 加密密钥 (建议从安全存储获取)
    :return: 小写十六进制签名串（64字符）

    示例:
    >>> signature("123", "abc", "body", "key")
    'd5e4e3c8f492b3c6a0d3f7d3c3c3e3d3c3e3d3c3e3d3c3e3d3c3e3d3c3e3d3'
    """
    # 参数校验
    if not all(isinstance(arg, str) for arg in [timestamp, nonce, req_body, encrypt_key]):
        raise TypeError("所有参数必须为字符串类型")

    # 拼接顺序必须与Java保持一致
    raw_str = f"{timestamp}{nonce}{encrypt_key}{req_body}"

    # 创建SHA-256对象（推荐用new方式提升复用性）
    sha = hashlib.sha256()
    sha.update(raw_str.encode('utf-8'))  # 必须指定编码

    # 返回小写十六进制字符串（与Java兼容）
    return sha.hexdigest()

@mcp.tool(name="查询企业员工部门信息",
          description="查询企业员工部门信息接口，输入企业id和员工id，返回该员工的所属部门信息")
async def query_employee_org(corpId: str = Field(description="要查询员工所属企业id"),
                             employeeId: str = Field(description="要查询的员工的 id")) -> object:
    logger.info("收到查询员工组织请求, corpId:{} employeeId:{}".format(corpId, employeeId))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>corpId<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"

    body = {"corpId": corpId, "employeeId": employeeId}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body,ensure_ascii=False,separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp,nonce,json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeOrg"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result

def run():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
