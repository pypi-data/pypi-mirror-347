"""
配置文件
包含API访问密钥、基础URL等配置信息
"""

import os

# API访问密钥配置 - 从环境变量获取或使用默认值
ACCESS_KEY = os.environ.get("VIDEOMCP_ACCESS_KEY", "IX_xl1q9A25p3MxQw99XRw")
SECRET_KEY = os.environ.get("VIDEOMCP_SECRET_KEY", "yIAbc4G_p-eleS9wLUllO95rEp4w-bSa")

# API基础URL
API_BASE_URL = os.environ.get("VIDEOMCP_API_BASE_URL", "https://openapi.liblibai.cloud")

# HTTP请求配置
HTTP_TIMEOUT = 30  # 请求超时时间（秒）
RETRY_COUNT = 3    # 请求重试次数
RETRY_INTERVAL = 1 # 重试间隔（秒）

# 默认模型配置
DEFAULT_MODEL_UUID = "0ea388c7eb854be3ba3c6f65aac6bfd3"  # 默认图像生成模型ID

# API接口路径
API_ENDPOINTS = {
    "GET_MODELS": "/api/v1/models",             # 获取可用模型列表
    "GEN_IMAGE": "/api/generate/webui/text2img", # 文生图接口
    "GEN_STATUS": "/api/generate/webui/status",  # 生成状态查询接口
    "GEN_IMAGE_ULTRA": "/api/generate/webui/text2img/ultra", # 旗舰版文生图接口
}

# 模板UUID配置
TEMPLATE_UUIDS = {
    "STANDARD": "6f7c4652458d4802969f8d089cf5b91f",  # 标准模板
    "ULTRA": "5d7e67009b344550bc1aa6ccbfa1d7f4",    # 旗舰版模板
}

# 默认下载目录
DEFAULT_DOWNLOAD_DIR = os.environ.get("VIDEOMCP_DOWNLOAD_DIR", os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP"))

# 创建默认下载目录
os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

# 缓存设置
ENABLE_CACHE = True
CACHE_TTL = 600  # 缓存有效期（秒） 