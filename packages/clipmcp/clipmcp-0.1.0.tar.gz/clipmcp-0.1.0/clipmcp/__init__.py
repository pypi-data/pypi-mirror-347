"""
VideoMCP - 文本到图像生成API客户端和服务

提供基于fastmcp方式的图像生成相关功能和API服务
"""

__version__ = "0.1.0"
__author__ = "VideoMCP Team"
__email__ = "example@example.com"
__license__ = "MIT"

# 导入主要组件，方便用户直接从videomcp包导入
try:
    from .services.image_service import FastMCP
except ImportError:
    pass 