"""
VideoMCP 主模块
提供命令行入口和主要功能
"""

import os
import sys
import asyncio
import argparse
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

from fastmcp import FastMCP

from .services.image_service import ImageService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clipmcp")

class ClipMcpServer:
    def __init__(self):
        # 创建MCP服务
        self.mcp = FastMCP("clipmcp")
        self.image_service = ImageService()
        self.last_result = None
        
        # 注册工具
        self._register_tools()
    
    def _register_tools(self):
        # 注册所有MCP工具
        self.mcp.tool()(self.generate_image)
        self.mcp.tool()(self.get_server_info)
        self.mcp.tool()(self.get_last_result)
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 768,
        height: int = 1024,
        count: int = 1,
        seed: int = -1,
        output_dir: Optional[str] = None,
        use_ultra: bool = False
    ) -> Dict[str, Any]:
        """生成图像
        
        Args:
            prompt: 提示词
            negative_prompt: 负面提示词
            width: 图像宽度
            height: 图像高度
            count: 生成图像数量
            seed: 随机种子
            output_dir: 输出目录
            use_ultra: 是否使用旗舰版API
            
        Returns:
            包含生成图像信息的字典
        """
        try:
            logger.info(f"通过MCP生成图像: {prompt}")
            
            # 设置输出目录（如果提供）
            if output_dir:
                self.image_service.default_download_dir = output_dir
                os.makedirs(output_dir, exist_ok=True)
            
            # 生成图像
            result = await self.image_service.text2img(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                img_count=count,
                seed=seed,
                download=True,
                use_ultra=use_ultra
            )
            
            # 保存结果
            self.last_result = result
            
            return result
        except Exception as e:
            error_msg = f"生成图像时出错: {str(e)}"
            logger.error(error_msg)
            error_result = {
                "success": False,
                "error": error_msg,
                "prompt": prompt
            }
            self.last_result = error_result
            return error_result
    
    async def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息"""
        try:
            from . import __version__
            return {
                "name": "ClipMCP 图像生成服务",
                "version": __version__,
                "status": "运行中",
                "tools": {
                    "生成图像": "generate_image",
                    "获取服务信息": "get_server_info",
                    "获取最后一次结果": "get_last_result"
                },
                "configuration": {
                    "api_base_url": os.environ.get("VIDEOMCP_API_BASE_URL", "https://openapi.liblibai.cloud"),
                    "download_dir": os.environ.get("VIDEOMCP_DOWNLOAD_DIR", "")
                }
            }
        except Exception as e:
            return {
                "status": "错误",
                "error": f"获取服务器信息时出错: {str(e)}"
            }
    
    async def get_last_result(self) -> Dict[str, Any]:
        """获取最后一次生成结果"""
        try:
            if self.last_result:
                return self.last_result
            else:
                return {
                    "success": False,
                    "error": "没有可用的生成结果"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取最后结果时出错: {str(e)}"
            }
    
    def run(self, transport='stdio'):
        """运行MCP服务器"""
        logger.info(f"启动ClipMCP服务")
        self.mcp.run(transport=transport)


async def generate_image_cli(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 768,
    height: int = 1024,
    count: int = 1,
    seed: int = -1,
    output_dir: Optional[str] = None,
    use_ultra: bool = False
):
    """命令行图像生成入口"""
    # 创建服务
    service = ImageService()
    
    # 设置输出目录（如果提供）
    if output_dir:
        service.default_download_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    # 生成图像
    result = await service.text2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        img_count=count,
        seed=seed,
        download=True,
        use_ultra=use_ultra
    )
    
    # 输出结果
    if result:
        print("\n图像生成成功!")
        
        # 打印图像URL
        if "images" in result:
            for i, image in enumerate(result["images"]):
                print(f"图像 {i+1} URL: {image.get('imageUrl')}")
        
        # 打印下载路径
        if "downloaded_files" in result:
            for i, file_path in enumerate(result["downloaded_files"]):
                print(f"本地保存路径 {i+1}: {file_path}")
    else:
        print("图像生成失败!")


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description="VideoMCP - 文本到图像生成工具")
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 图像生成子命令
    gen_parser = subparsers.add_parser("generate", help="生成图像")
    gen_parser.add_argument("prompt", help="提示词")
    gen_parser.add_argument("--negative", help="负面提示词")
    gen_parser.add_argument("--width", type=int, default=768, help="图像宽度")
    gen_parser.add_argument("--height", type=int, default=1024, help="图像高度")
    gen_parser.add_argument("--count", type=int, default=1, help="生成图像数量")
    gen_parser.add_argument("--seed", type=int, default=-1, help="随机种子")
    gen_parser.add_argument("--output", help="输出目录")
    gen_parser.add_argument("--ultra", action="store_true", help="使用旗舰版API")
    
    # MCP服务器模式
    server_parser = subparsers.add_parser("server", help="启动MCP服务器")
    server_parser.add_argument("--transport", choices=["stdio", "tcp", "websocket"], default="stdio",
                             help="MCP通信方式 (默认: stdio)")
    server_parser.add_argument("--host", type=str, help="TCP/WebSocket服务器主机")
    server_parser.add_argument("--port", type=int, help="TCP/WebSocket服务器端口")
    server_parser.add_argument("--debug", action="store_true", help="启用调试模式")
    
    # 版本信息
    parser.add_argument("--version", action="store_true", help="显示版本信息")
    
    # 解析参数
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        from . import __version__
        print(f"VideoMCP 版本: {__version__}")
        return
    
    # 处理子命令
    if args.command == "generate":
        asyncio.run(generate_image_cli(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            count=args.count,
            seed=args.seed,
            output_dir=args.output,
            use_ultra=args.ultra
        ))
    elif args.command == "server":
        # 如果启用了调试模式，设置日志级别
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logger.debug("调试模式已启用")
        
        # 创建并运行MCP服务器
        server = ClipMcpServer()
        server.run(transport=args.transport)
    else:
        parser.print_help()


def run_mcp():
    """命令行入口点，用于uvx命令"""
    parser = argparse.ArgumentParser(description="ClipMCP服务器")
    parser.add_argument("--transport", choices=["stdio", "tcp", "websocket"], default="stdio",
                      help="MCP通信方式 (默认: stdio)")
    parser.add_argument("--host", type=str, help="TCP/WebSocket服务器主机")
    parser.add_argument("--port", type=int, help="TCP/WebSocket服务器端口")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    
    args = parser.parse_args()
    
    # 如果启用了调试模式，设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 创建并运行MCP服务器
    server = ClipMcpServer()
    server.run(transport=args.transport)


if __name__ == "__main__":
    main() 