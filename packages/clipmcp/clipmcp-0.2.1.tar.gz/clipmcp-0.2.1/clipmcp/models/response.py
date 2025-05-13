"""
响应模型定义
定义各种API响应的数据模型
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ApiBaseResponse(BaseModel):
    """API基础响应结构"""
    code: int = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    request_id: Optional[str] = Field(None, description="请求ID")


class ModelVersionInfo(BaseModel):
    """模型版本信息"""
    model_id: str = Field(..., description="模型ID")
    model_name: str = Field(..., description="模型名称")
    model_type: str = Field(..., description="模型类型")
    version: str = Field(..., description="版本号")
    description: Optional[str] = Field(None, description="描述信息")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")
    parameters: Optional[Dict[str, Any]] = Field(None, description="参数信息")


class ModelVersionResponse(ApiBaseResponse):
    """模型版本获取响应"""
    data: List[ModelVersionInfo] = Field([], description="模型版本列表")


class GeneratedImage(BaseModel):
    """生成的图像信息"""
    image_id: str = Field(..., description="图像ID")
    image_url: str = Field(..., description="图像URL")
    width: int = Field(..., description="图像宽度")
    height: int = Field(..., description="图像高度")
    seed: int = Field(..., description="使用的随机种子")
    meta: Optional[Dict[str, Any]] = Field(None, description="元数据")


class ImageGenerationResponse(ApiBaseResponse):
    """图像生成响应"""
    data: List[GeneratedImage] = Field([], description="生成的图像列表")
    task_id: Optional[str] = Field(None, description="任务ID，用于异步任务查询")
    status: Optional[str] = Field(None, description="任务状态") 