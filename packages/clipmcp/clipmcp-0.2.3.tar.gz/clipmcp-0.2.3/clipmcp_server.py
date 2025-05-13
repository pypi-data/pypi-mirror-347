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
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# 添加当前目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 设置日志级别
log_level = os.environ.get("LOG_LEVEL", "DEBUG")  # 默认使用DEBUG级别以获取更多信息
numeric_level = getattr(logging, log_level.upper(), logging.DEBUG)
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
    from clipmcp.services.image_service import FastMCP
    logger.info("成功导入FastMCP")
except ImportError as e:
    error_info = traceback.format_exc()
    logger.error(f"导入clipmcp包失败: {e}\n{error_info}")
    # 不直接退出，使用None表示服务不可用
    FastMCP = None
    api_keys_missing = True
    logger.warning("无法导入FastMCP，将以只读模式运行服务器")

# 导入MCP相关模块
try:
    from mcp import Tool
    from mcp.types import ServerRequest
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    logger.info("成功导入MCP模块")
except ImportError as e:
    try:
        # 尝试从fastmcp导入
        from fastmcp import Tool
        from fastmcp.types import ServerRequest
        from fastmcp.server import Server
        from fastmcp.server.stdio import stdio_server
        logger.info("成功导入FastMCP模块")
    except ImportError as e2:
        error_info = traceback.format_exc()
        logger.error(f"导入MCP/FastMCP模块失败: {e2}\n{error_info}")
        sys.exit(1)

# 初始化服务
image_service_client = None
api_keys_missing = False
last_result = None  # 保存最后一次生成结果

# 定义工具执行类
class ImageGenServer(Server):
    def __init__(self, name, version):
        super().__init__(name=name, version=version)
        self.tools = {}
    
    def add_tool(self, tool):
        self.tools[tool.name] = tool
    
    async def call_tool(self, request: ServerRequest) -> Any:
        """处理工具调用请求"""
        logger.debug(f"收到工具调用请求: {request.name}")
        
        if request.name == "generate_image":
            result = await run_generate_image(**request.parameters)
            return result
        elif request.name == "get_server_info":
            result = self.get_server_info()
            return result
        elif request.name == "get_last_result":
            return self.get_last_result()
        else:
            logger.warning(f"未知工具: {request.name}")
            return {"error": f"未知工具: {request.name}"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """返回服务器信息"""
        return {
            "name": "ClipMCP图像生成服务",
            "version": self.version,
            "status": "运行中",
            "tools": {
                "生成图像": "generate_image",
                "获取服务信息": "get_server_info",
                "获取最后一次结果": "get_last_result"
            },
            "configuration": {
                "api_keys_missing": api_keys_missing
            }
        }
    
    def get_last_result(self) -> Dict[str, Any]:
        """返回最后一次生成结果"""
        global last_result
        if last_result:
            return last_result
        else:
            return {"message": "尚无生成结果"}
    
    def list_tools(self) -> List[Tool]:
        """返回可用工具列表"""
        return list(self.tools.values())

# 定义工具
async def run_generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 768,
    height: int = 1024,
    img_count: int = 1,
    count: Optional[int] = None,  # 添加count参数，兼容不同API
    seed: int = -1,
    download: bool = True,
    use_ultra: bool = False,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    生成图像
    
    Args:
        prompt: 提示词
        negative_prompt: 负面提示词
        width: 图像宽度
        height: 图像高度
        img_count: 生成图像数量
        count: 生成图像数量的别名，与img_count相同
        seed: 随机种子
        download: 是否下载图像
        use_ultra: 是否使用旗舰版模型
        output_dir: 输出目录
        
    Returns:
        生成结果，包含图像URL和下载路径
    """
    global image_service_client, api_keys_missing, last_result
    
    # 兼容count和img_count参数
    effective_count = count if count is not None else img_count
    
    if api_keys_missing:
        return {
            "success": False, 
            "error": "未设置API密钥。请设置VIDEOMCP_ACCESS_KEY和VIDEOMCP_SECRET_KEY环境变量"
        }
    
    if not image_service_client:
        return {"success": False, "error": "图像服务客户端未初始化"}
    
    logger.info(f"收到生成图像请求: prompt='{prompt[:50]}...', count={effective_count}, ultra={use_ultra}")
    
    # 处理自定义输出目录
    original_download_dir = image_service_client.default_download_dir
    download_dir = os.environ.get("VIDEOMCP_DOWNLOAD_DIR")
    effective_download_dir = output_dir or download_dir
    
    if download and effective_download_dir:
        try:
            os.makedirs(effective_download_dir, exist_ok=True)
            image_service_client.default_download_dir = effective_download_dir
            logger.info(f"本次请求使用下载目录: {effective_download_dir}")
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(f"创建或设置下载目录失败 {effective_download_dir}: {e}\n{error_info}")
            return {"success": False, "error": f"无法访问输出目录: {effective_download_dir}"}
    
    try:
        result = await image_service_client.text2img(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            img_count=effective_count,  # 使用有效的数量参数
            seed=seed,
            download=download,
            use_ultra=use_ultra
        )
        
        if result:
            logger.info(f"图像生成成功")
            
            # 构建返回结果
            response = {
                "success": True,
                "images": result.get("images", []),
                "downloaded_files": result.get("downloaded_files", []),
                "pointsCost": result.get("pointsCost"),
                "accountBalance": result.get("accountBalance"),
                "generateUuid": result.get("generateUuid")
            }
            
            # 确保下载文件路径使用正确的目录
            if download and "downloaded_files" in result and effective_download_dir:
                response["downloaded_files"] = [
                    os.path.normpath(path) for path in result["downloaded_files"]
                ]
            
            # 保存最后一次结果
            last_result = response
            
            return response
        else:
            error_msg = "未知错误"
            logger.error(f"图像生成失败: {error_msg}")
            return {"success": False, "error": f"图像生成失败: {error_msg}"}
    except Exception as e:
        error_info = traceback.format_exc()
        logger.error(f"生成图像时发生异常: {e}\n{error_info}")
        return {"success": False, "error": f"服务器内部错误: {str(e)}"}
    finally:
        # 恢复原始下载目录
        if download and effective_download_dir:
            image_service_client.default_download_dir = original_download_dir

def main():
    """主函数"""
    global image_service_client, api_keys_missing
    
    logger.info("ClipMCP服务器启动")
    
    # 获取环境变量
    access_key = os.environ.get("VIDEOMCP_ACCESS_KEY")
    secret_key = os.environ.get("VIDEOMCP_SECRET_KEY")
    api_base_url = os.environ.get("VIDEOMCP_API_BASE_URL", "https://openapi.liblibai.cloud")
    download_dir = os.environ.get("VIDEOMCP_DOWNLOAD_DIR", 
                             os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP"))
    
    # 检查必要的环境变量
    if not access_key:
        logger.warning("VIDEOMCP_ACCESS_KEY环境变量未设置")
        api_keys_missing = True
    if not secret_key:
        logger.warning("VIDEOMCP_SECRET_KEY环境变量未设置")
        api_keys_missing = True
    
    if api_keys_missing:
        logger.warning("API密钥缺失。服务器将启动，但无法生成图像，直到设置API密钥")
    
    # 创建下载目录
    try:
        os.makedirs(download_dir, exist_ok=True)
        logger.info(f"已创建下载目录: {download_dir}")
    except Exception as e:
        error_info = traceback.format_exc()
        logger.error(f"创建下载目录失败: {e}\n{error_info}")
    
    logger.info(f"API基础URL: {api_base_url}")
    logger.info(f"下载目录: {download_dir}")
    
    # 初始化图像服务客户端
    if not api_keys_missing and FastMCP is not None:
        try:
            logger.info("初始化图像服务客户端")
            image_service_client = FastMCP(
                access_key=access_key,
                secret_key=secret_key,
                api_base_url=api_base_url,
                download_dir=download_dir
            )
            logger.info("图像服务客户端初始化成功")
        except Exception as e:
            error_info = traceback.format_exc()
            logger.error(f"初始化图像服务客户端失败: {e}\n{error_info}")
            api_keys_missing = True
            logger.warning("将以无API密钥模式继续运行")
    
    # 创建工具
    try:
        logger.info("创建MCP工具")
        inputSchema = {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "提示词，用于生成图像"
                },
                "negative_prompt": {
                    "type": "string",
                    "description": "负面提示词，指定不希望在图像中出现的内容"
                },
                "width": {
                    "type": "integer",
                    "description": "图像宽度，像素单位",
                    "default": 768
                },
                "height": {
                    "type": "integer",
                    "description": "图像高度，像素单位",
                    "default": 1024
                },
                "img_count": {
                    "type": "integer",
                    "description": "生成图像数量",
                    "default": 1
                },
                "count": {
                    "type": "integer",
                    "description": "生成图像数量（与img_count相同，兼容不同客户端）",
                    "default": 1
                },
                "seed": {
                    "type": "integer",
                    "description": "随机种子，-1表示随机",
                    "default": -1
                },
                "download": {
                    "type": "boolean",
                    "description": "是否下载图像",
                    "default": True
                },
                "use_ultra": {
                    "type": "boolean",
                    "description": "是否使用旗舰版模型",
                    "default": False
                },
                "output_dir": {
                    "type": "string",
                    "description": "输出目录，不提供则使用默认目录"
                }
            },
            "required": ["prompt"]
        }
        
        generate_tool = Tool(
            name="generate_image",
            description="使用AI模型生成图像",
            inputSchema=inputSchema
        )
        logger.info("MCP工具创建成功")
        
        # 创建获取服务器信息工具
        server_info_tool = Tool(
            name="get_server_info",
            description="获取服务器相关信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "random_string": {
                        "type": "string",
                        "description": "Dummy parameter for no-parameter tools"
                    }
                },
                "required": ["random_string"]
            }
        )
        
        # 创建获取最后一次结果工具
        last_result_tool = Tool(
            name="get_last_result",
            description="获取最后一次生成结果",
            inputSchema={
                "type": "object",
                "properties": {
                    "random_string": {
                        "type": "string",
                        "description": "Dummy parameter for no-parameter tools"
                    }
                },
                "required": ["random_string"]
            }
        )
        
        # 创建自定义服务器
        server = ImageGenServer(
            name="clipmcp-server",
            version="0.2.2"
        )
        
        # 添加工具
        server.add_tool(generate_tool)
        server.add_tool(server_info_tool)
        server.add_tool(last_result_tool)
        logger.info("已添加工具到服务器")
    except Exception as e:
        error_info = traceback.format_exc()
        logger.error(f"创建MCP工具或服务器失败: {e}\n{error_info}")
        sys.exit(1)
    
    # 启动MCP服务器
    try:
        logger.info("启动MCP服务器")
        # 使用asyncio运行服务器
        asyncio.run(stdio_server(server))
    except Exception as e:
        error_info = traceback.format_exc()
        logger.error(f"服务器启动失败: {e}\n{error_info}")
        sys.exit(1)

# 用于导出的主函数
def run_server():
    try:
        main()
    except Exception as e:
        error_info = traceback.format_exc()
        logger.error(f"主程序异常: {e}\n{error_info}")
        sys.exit(1)

if __name__ == "__main__":
    run_server()