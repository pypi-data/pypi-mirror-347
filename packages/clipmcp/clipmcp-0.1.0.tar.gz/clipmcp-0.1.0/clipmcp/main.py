"""
VideoMCP 主模块
提供命令行入口和主要功能
"""

import os
import sys
import asyncio
import argparse
from typing import Optional

from .services.image_service import FastMCP


async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 768,
    height: int = 1024,
    count: int = 1,
    seed: int = -1,
    output_dir: Optional[str] = None,
    use_ultra: bool = False
):
    """生成图像"""
    # 创建FastMCP客户端
    client = FastMCP()
    
    # 设置输出目录（如果提供）
    if output_dir:
        client.default_download_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    # 生成图像
    result = await client.text2img(
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
        asyncio.run(generate_image(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            count=args.count,
            seed=args.seed,
            output_dir=args.output,
            use_ultra=args.ultra
        ))
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 