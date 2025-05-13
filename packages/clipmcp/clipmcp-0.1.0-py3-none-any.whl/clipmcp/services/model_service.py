"""
模型服务
提供模型版本查询等功能
"""

import json
import logging
import httpx
from typing import Dict, Any, List, Optional

from ..utils.auth import AuthManager
from ..utils.config import (
    ACCESS_KEY, SECRET_KEY, API_BASE_URL, 
    API_ENDPOINTS, HTTP_TIMEOUT, RETRY_COUNT, RETRY_INTERVAL
)
from ..models.request import ModelVersionRequest
from ..models.response import ModelVersionResponse, ModelVersionInfo

# 配置日志
logger = logging.getLogger(__name__)


class ModelService:
    """模型服务类"""
    
    def __init__(self):
        """初始化模型服务"""
        self.auth_manager = AuthManager(ACCESS_KEY, SECRET_KEY)
        self.base_url = API_BASE_URL
        
    async def get_model_versions(
        self, model_type: Optional[str] = None
    ) -> ModelVersionResponse:
        """
        获取模型版本列表
        
        Args:
            model_type: 可选的模型类型筛选
            
        Returns:
            模型版本响应对象
        """
        # 准备请求参数
        uri = API_ENDPOINTS["MODEL_VERSION"]
        request_data = ModelVersionRequest(model_type=model_type).dict(exclude_none=True)
        
        # 附加认证信息
        auth_params = self.auth_manager.attach_auth_params(uri, request_data)
        
        # 构建完整URL
        url = f"{self.base_url}{uri}"
        
        logger.info(f"正在获取模型版本信息，请求URL: {url}")
        
        # 发送请求
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                for attempt in range(RETRY_COUNT):
                    try:
                        response = await client.post(url, json=auth_params)
                        response.raise_for_status()
                        break
                    except httpx.HTTPError as e:
                        if attempt == RETRY_COUNT - 1:
                            raise
                        logger.warning(f"请求失败，正在重试 ({attempt+1}/{RETRY_COUNT}): {e}")
                        import asyncio
                        await asyncio.sleep(RETRY_INTERVAL)
                        
            # 解析响应
            response_data = response.json()
            
            logger.debug(f"模型版本响应: {json.dumps(response_data, ensure_ascii=False)}")
            
            # 构建响应对象
            result = ModelVersionResponse(
                code=response_data.get("code", 0),
                message=response_data.get("message", ""),
                request_id=response_data.get("request_id"),
                data=[]
            )
            
            # 处理数据部分
            if "data" in response_data and isinstance(response_data["data"], list):
                for item in response_data["data"]:
                    model_info = ModelVersionInfo(
                        model_id=item.get("model_id", ""),
                        model_name=item.get("model_name", ""),
                        model_type=item.get("model_type", ""),
                        version=item.get("version", ""),
                        description=item.get("description"),
                        created_at=item.get("created_at"),
                        updated_at=item.get("updated_at"),
                        parameters=item.get("parameters")
                    )
                    result.data.append(model_info)
                    
            return result
            
        except Exception as e:
            logger.error(f"获取模型版本失败: {e}", exc_info=True)
            return ModelVersionResponse(
                code=-1,
                message=f"获取模型版本失败: {str(e)}",
                data=[]
            ) 