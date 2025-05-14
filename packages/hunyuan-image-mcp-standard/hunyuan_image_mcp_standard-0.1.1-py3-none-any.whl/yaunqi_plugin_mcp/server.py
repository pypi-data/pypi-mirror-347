import os
import sys
import logging
import httpx
from typing import Any

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logging.info("Starting YuanQi Plugin MCP Server")

def hunyuanText2Image(arguments: dict[str, Any]) -> str:
    hunyuanText2ImageUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"
    
    user_prompt = arguments.get("prompt", "")
    if user_prompt == "":
        raise ValueError("prompt不能为空")
    image_url = arguments.get("imageUrl", "")
    
    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"hunyuanText2Image",
            "arguments": {
                "image_url": image_url,
                "prompt": user_prompt
            }
        }
    }
    api_key = os.getenv("API_KEY", None)
    if api_key is None:
        raise ValueError("环境变量API_KEY没有设置")
    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY", "")
    }

    logging.info("start to call yuanqi plugin api:", payload)
    timeout = httpx.Timeout(90.0, connect=10.0)
    response = httpx.post(hunyuanText2ImageUrl, headers=headers, json=payload, timeout=timeout)
    response_json = response.json()
    if response.status_code == 401:
        raise SystemError("token验证失败")
    if response.status_code != 200:
        error_info = response_json.get("error", None)
        if error_info is None:
            raise SystemError(f"请求服务器失败，错误码{response.status_code}")
        else:
            err_msg = error_info.get("message", "未知错误")
            raise SystemError(f"请求服务器失败，{err_msg}")
        
    logging.info("yuanqi openapi response:", response_json)
    err_info = response_json.get("error", None)
    if err_info is not None:
        raise SystemError(err_info["message"])
    result = response_json.get("result", None)
    if result is None:
        raise SystemError(f"请求服务器失败，返回数据格式不正确。{response_json}")
    if result["isError"]:
        raise SystemError(result["content"][0]["text"])

    return result["content"][0]["text"]
    
    
async def main():
    logging.info("Starting YuanQi Plugin MCP Server.")
    
    server = Server("hunyuan-image-mcp-standard", "0.1.1", "mcp server to invoke hunyuan image")
    
    # Register handlers
    logging.debug("Registering handlers")
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="hunyuanText2Image",
                description="通过文字描述生成图片，或者根据要求修改图片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "imageUrl": {
                            "type": "string", 
                            "description": "需要修改的图片url地址"
                        },
                        "prompt": {
                            "type": "string", 
                            "description": "用于生成图片或者修改图片的提示词"
                        }
                    },
                    "required": ["prompt"],
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "hunyuanText2Image":
                results = hunyuanText2Image(arguments)
                return [types.TextContent(type="text", text=str(results))]
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            raise e # [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with stdio_server() as (read_stream, write_stream):
        logging.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hunyuan-image-mcp-standard", 
                server_version="0.1.1",
                server_instructions="mcp server to invoke hunyuan image",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

class ServerWrapper():
    """A wrapper to compat with mcp[cli]"""
    def run(self):
        import asyncio
        asyncio.run(main())


wrapper = ServerWrapper()