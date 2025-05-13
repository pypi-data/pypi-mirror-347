"""
VideoMCP - 文本到图像生成API客户端和服务

提供基于fastmcp方式的图像生成相关功能和API服务
"""

__version__ = "0.2.3"
__author__ = "VideoMCP Team"
__email__ = "example@example.com"
__license__ = "MIT"

# 导出版本号
__version__ = "0.2.2"

# 导出主要的公共API
try:
    from clipmcp.services.image_service import generate_image, ImageService
except ImportError:
    import sys
    import os
    # 添加项目根目录到sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    # 重试导入
    from clipmcp.services.image_service import generate_image, ImageService

# 导出命令行入口点
from clipmcp.cli import main as cli_main

# 主程序入口点
def main():
    """主程序入口点"""
    from clipmcp.cli import main
    main() 