"""
API路由
定义对外提供的API接口
"""

import logging
from typing import Dict, Any, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException

from ..services.model_service import ModelService
from ..services.image_service import ImageService
from ..models.request import ModelVersionRequest, ImageGenerationRequest
from ..models.response import ModelVersionResponse, ImageGenerationResponse

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter(prefix="/api", tags=["image-generation"])


# 依赖注入
def get_model_service():
    return ModelService()


def get_image_service():
    return ImageService()


@router.post("/model/versions", response_model=ModelVersionResponse)
async def get_model_versions(
    request: ModelVersionRequest = None,
    model_service: ModelService = Depends(get_model_service)
):
    """获取可用的模型版本列表"""
    model_type = None
    if request:
        model_type = request.model_type
        
    result = await model_service.get_model_versions(model_type)
    
    if result.code != 0:
        raise HTTPException(status_code=400, detail=result.message)
        
    return result


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    image_service: ImageService = Depends(get_image_service)
):
    """生成图像"""
    result = await image_service.generate_image(request)
    
    if result.code != 0:
        raise HTTPException(status_code=400, detail=result.message)
        
    return result 