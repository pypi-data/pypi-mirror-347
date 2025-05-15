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

logging.info("Starting YuanQi Agent MCP Server")

def yuanqi_chat(arguments: dict[str, Any]) -> str:
    yuanqi_openapi_url = "http://120.232.196.205/openapi/v1/agent/chat/completions"
    
    user_id = arguments.get("userID", "mcp_user")
    user_prompt = arguments.get("userPrompt", "")
    if user_prompt == "":
        raise ValueError("userPrompt不能为空")
    user_contents = []
    user_contents.append({
                        "type":"text", 
                        "text": user_prompt
                        })
    file_urls = arguments.get("fileUrls", None)
    try:
        if file_urls is not None:
            for url in file_urls:
                user_contents.append({
                    "type":"file_url",
                    "file_url": {
                        "type": "resource",
                        "url": url
                    }
                })
    except Exception:
        raise TypeError("chatHistory结构不正确")
    message_list = []
    try:
        msgs = arguments.get("chatHistory", None)
        if msgs is not None:
            for msg in msgs:
                message_list.append({
                    "role": msg["role"],
                    "content":[
                        {
                        "type":"text", 
                        "text": msg["content"]
                        }
                    ]
                })
    except Exception:
        raise TypeError("chatHistory结构不正确")
    if len(message_list) == 0:
        message_list.append({
            "role": "user",
            "content": user_contents
        })
    else:
        if message_list[-1]["role"] == "user":
            message_list[-1]["content"] = user_contents
        else:
            message_list.append({
                "role": "user",
                "content": user_contents
            })
    assistant_id = os.getenv("ASSISTANT_ID", None)
    if assistant_id is None:
        raise ValueError("环境变量ASSISTANT_ID没有设置")
    version = 0
    version_str = os.getenv("ASSISTANT_VERSION", None)
    if version_str is not None:
        try:
            version = int(version_str)
        except ValueError:
            version = 0
    payload = {
        "assistant_id": assistant_id,
        "version": version,
        "user_id": user_id,
        "stream": False,
        "messages": message_list
    }
    api_key = os.getenv("API_KEY", None)
    if api_key is None:
        raise ValueError("环境变量API_KEY没有设置")
    headers = {
        "X-Source": "mcp-server",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY", "")
    }

    logging.info("start to call yuanqi openapi:", payload)
    timeout = httpx.Timeout(300.0, connect=10.0)
    response = httpx.post(yuanqi_openapi_url, headers=headers, json=payload, timeout=timeout)
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

    return response_json["choices"][0]["message"]["content"]
    
    
async def main(tool_name: str, tool_desc: str):
    logging.info(f"Starting YuanQi Agent MCP Server MCP Server with tool: {tool_name}")
    
    server = Server("yuanqi-agent-test-mcp", "0.1.1", "mcp server to invoke yuanqi agent")
    
    # Register handlers
    logging.debug("Registering handlers")
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name=tool_name,
                description=tool_desc,
                inputSchema={
                    "type": "object",
                    "properties": {
                        "userPrompt": {
                            "type": "string", 
                            "description": "用户当前问题"
                        },
                        "fileUrls": {
                            "type": "array", 
                            "description": "用户当前问题相关的URL列表",
                            "items": {
                                "type": "string",
                                "description": "用户当前问题相关的URL"
                            }
                        },
                        "chatHistory": {
                            "type": "array", 
                            "description": "用户历史对话记录列表，不包含用户当前问题",
                            "items": {
                                "type": "object",
                                "description": "对话内容",
                                "properties": {
                                    "role": {
                                        "type": "string", 
                                        "description": "对话角色类型，只能是user/assistant",
                                        "enum": [
                                            "user",
                                            "assistant"
                                        ]
                                    },
                                    "content": {
                                        "type": "string", 
                                        "description": "对话内容"
                                    }
                                }
                            }
                        },
                        "userID": {
                            "type": "string", 
                            "description": "用户身份标识"
                        }
                    },
                    "required": ["userPrompt"],
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == tool_name:
                results = yuanqi_chat(arguments)
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
                server_name="yuanqi-agent-test-mcp", 
                server_version="0.1.1",
                server_instructions="mcp server to invoke yuanqi agent",
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
        asyncio.run(main("chat", "调用元器智能体进行对话"))


wrapper = ServerWrapper()