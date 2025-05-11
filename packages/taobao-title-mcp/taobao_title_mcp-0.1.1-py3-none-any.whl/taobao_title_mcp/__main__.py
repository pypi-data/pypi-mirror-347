"""淘宝标题生成MCP服务器入口模块。"""

import sys
import logging
from .server import mcp, startup_handler, shutdown_handler

# 导入所有组件以确保它们被注册
from . import tools  # noqa
from . import resources  # noqa
# 暂时移除提示模块
# from . import prompts  # noqa

def main():
    """服务器启动入口。"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    
    # 执行启动处理
    startup_handler()
    
    print("启动淘宝标题生成MCP服务器...", file=sys.stderr)
    try:
        # 启动服务器
        mcp.run()
    except KeyboardInterrupt:
        print("\n收到中断信号，正在关闭服务器...", file=sys.stderr)
    except Exception as e:
        print(f"服务器运行时出错: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # 执行关闭处理
        shutdown_handler()
        print("服务器已停止。", file=sys.stderr)

if __name__ == "__main__":
    main() 