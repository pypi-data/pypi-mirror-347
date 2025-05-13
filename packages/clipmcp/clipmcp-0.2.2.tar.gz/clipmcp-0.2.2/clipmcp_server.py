#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ClipMCP服务器入口点
用于MCP协议与Cursor集成
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path

# 添加当前目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 设置日志级别
log_level = os.environ.get("LOG_LEVEL", "INFO")
numeric_level = getattr(logging, log_level.upper(), logging.INFO)
logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(current_dir, "clipmcp_server.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("clipmcp-server")

# 导入服务器模块
try:
    from clipmcp.server import main as server_main
except ImportError as e:
    logger.error(f"导入clipmcp包失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    logger.info("ClipMCP服务器启动")
    
    # 设置环境变量（如果未设置）
    if not os.environ.get("VIDEOMCP_ACCESS_KEY"):
        logger.warning("VIDEOMCP_ACCESS_KEY环境变量未设置")
    if not os.environ.get("VIDEOMCP_SECRET_KEY"):
        logger.warning("VIDEOMCP_SECRET_KEY环境变量未设置")
    
    # 创建下载目录
    download_dir = os.environ.get("VIDEOMCP_DOWNLOAD_DIR", 
                             os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP"))
    os.makedirs(download_dir, exist_ok=True)
    
    logger.info(f"API基础URL: {os.environ.get('VIDEOMCP_API_BASE_URL', 'https://openapi.liblibai.cloud')}")
    logger.info(f"下载目录: {download_dir}")
    
    # 启动服务器
    try:
        server_main()
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 