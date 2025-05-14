import sys
import os
import json
import logging
from venv import logger
from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("mcp-python-env-debugger")


def register(path, value):
    """注册不同类型的值作为MCP工具"""
    if isinstance(value, dict):
        for k, v in value.items():
            register(f"{path}.{k}", v)
        tool_func = lambda: {"content": [{"type": "text", "text": json.dumps(value, indent=2)}]}
        mcp.add_tool(tool_func, name=path, description=json.dumps(value))
    elif callable(value):
        value = value()
        register(f"{path}()", value)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            register(f"{path}.{i}", v)
        tool_func = lambda: {"content": [{"type": "text", "text": json.dumps(value, indent=2)}]}
        mcp.add_tool(tool_func, name=path, description=json.dumps(value))
    elif isinstance(value, (int, float)):
        tool_func = lambda: {"content": [{"type": "text", "text": str(value)}]}
        mcp.add_tool(tool_func, name=path, description=str(value))
    elif isinstance(value, str):
        tool_func = lambda: {"content": [{"type": "text", "text": str(value)}]}
        mcp.add_tool(tool_func, name=path, description=str(value))
    else:
        tool_func = lambda: {"content": [{"type": "text", "text": json.dumps(value, indent=2) if value is not None else "None"}]}
        mcp.add_tool(tool_func, name=path, description=json.dumps(value) if value is not None else "None")

 

# 注册系统信息
sys_attrs = [
    'version',
    'executable',
    'argv',
    'env',
    'path',
    'platform',
]

for attr in sys_attrs:
    if hasattr(sys, attr):
        value = getattr(sys, attr)
        logging.error(f"sys.{attr} = {value}")
        # 注册属性，区分普通属性和可调用对象
        register(f"sys.{attr}", value)

register(f"os.environ", dict(os.environ))

if __name__ == "__main__":
    logging.error("Hello from mcp-python-env-debugger!")
    mcp.run()
