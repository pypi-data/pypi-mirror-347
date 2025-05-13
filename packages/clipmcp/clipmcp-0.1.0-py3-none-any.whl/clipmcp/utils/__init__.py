"""
VideoMCP 工具模块
提供认证和配置等基础功能
"""
 
from .auth import AuthManager
from .config import (
    ACCESS_KEY, SECRET_KEY, API_BASE_URL, HTTP_TIMEOUT,
    API_ENDPOINTS, TEMPLATE_UUIDS, DEFAULT_DOWNLOAD_DIR
) 