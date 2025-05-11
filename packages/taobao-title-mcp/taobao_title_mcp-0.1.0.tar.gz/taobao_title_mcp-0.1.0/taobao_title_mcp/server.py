"""淘宝标题生成MCP服务器主模块。"""

import sys
from mcp.server.fastmcp import FastMCP

# 创建服务器实例
mcp = FastMCP(
    "淘宝标题生成服务",
    instructions="此服务器提供淘宝商品标题生成功能，可以根据商品图片URL生成优化的淘宝商品标题。",
    version="0.1.0",
    warn_on_duplicate_tools=True,
)

# 服务器启动和停止事件处理
def startup_handler():
    """服务器启动时的处理逻辑"""
    print("淘宝标题生成服务器正在启动...", file=sys.stderr)

def shutdown_handler():
    """服务器关闭时的处理逻辑"""
    print("淘宝标题生成服务器正在关闭...", file=sys.stderr) 