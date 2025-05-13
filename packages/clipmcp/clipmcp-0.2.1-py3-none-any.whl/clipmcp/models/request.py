"""
请求模型定义
定义各种API请求的数据模型
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ModelVersionRequest(BaseModel):
    """模型版本获取请求"""
    model_type: Optional[str] = Field(None, description="模型类型")


class ImageGenerationRequest(BaseModel):
    """图像生成请求"""
    model_id: str = Field(..., description="模型ID")
    prompt: str = Field(..., description="生成提示词")
    negative_prompt: Optional[str] = Field(None, description="负面提示词")
    width: int = Field(512, description="图像宽度")
    height: int = Field(512, description="图像高度")
    steps: int = Field(20, description="采样步数")
    sampler: Optional[str] = Field("euler_a", description="采样器")
    seed: Optional[int] = Field(None, description="随机种子")
    batch_size: int = Field(1, description="生成数量")
    guidance_scale: float = Field(7.0, description="提示词引导系数")
    
    # 额外参数字段，用于扩展特定模型的参数
    extra_params: Optional[Dict[str, Any]] = Field(None, description="额外参数")
    
    class Config:
        arbitrary_types_allowed = True 