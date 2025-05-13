"""
VideoMCP 命令行界面
"""

import os
import sys
import asyncio
import argparse
from .services.image_service import FastMCP

def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="VideoMCP 命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 生成图像命令
    generate_parser = subparsers.add_parser("generate", help="生成图像")
    generate_parser.add_argument("prompt", type=str, help="提示词，用于生成图像")
    generate_parser.add_argument("--negative", type=str, default="ugly, deformed, disfigured, poor quality, low quality", 
                        help="负面提示词")
    generate_parser.add_argument("--width", type=int, default=768, help="图像宽度")
    generate_parser.add_argument("--height", type=int, default=1024, help="图像高度")
    generate_parser.add_argument("--count", type=int, default=1, help="生成图像数量")
    generate_parser.add_argument("--seed", type=int, default=-1, help="随机种子，-1表示随机")
    generate_parser.add_argument("--output", type=str, default="./output_images", help="输出目录")
    generate_parser.add_argument("--ultra", action="store_true", help="使用Ultra模式")
    generate_parser.add_argument("--api-key", type=str, help="API密钥")
    generate_parser.add_argument("--api-secret", type=str, help="API密钥密文")
    generate_parser.add_argument("--api-base-url", type=str, default="https://openapi.liblibai.cloud", help="API基础URL")
    
    # 查看版本命令
    version_parser = subparsers.add_parser("version", help="查看版本")
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果没有提供命令，显示帮助
    if not args.command:
        parser.print_help()
        return
    
    # 处理各个命令
    if args.command == "generate":
        asyncio.run(generate_image(args))
    elif args.command == "version":
        from . import __version__
        print(f"VideoMCP 版本 {__version__}")

async def generate_image(args):
    """生成图像命令的处理函数"""
    # 获取API密钥和密文
    access_key = args.api_key or os.environ.get("VIDEOMCP_ACCESS_KEY") or os.environ.get("LIBLIBAI_ACCESS_KEY")
    secret_key = args.api_secret or os.environ.get("VIDEOMCP_SECRET_KEY") or os.environ.get("LIBLIBAI_SECRET_KEY")
    api_base_url = args.api_base_url or os.environ.get("VIDEOMCP_API_BASE_URL") or "https://openapi.liblibai.cloud"
    
    # 检查是否提供了API密钥和密文
    if not access_key or not secret_key:
        print("错误：未提供API密钥或密文。请通过命令行参数或环境变量设置。")
        print("  环境变量: VIDEOMCP_ACCESS_KEY, VIDEOMCP_SECRET_KEY")
        print("  或: LIBLIBAI_ACCESS_KEY, LIBLIBAI_SECRET_KEY")
        print("  命令行参数: --api-key, --api-secret")
        return
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 创建FastMCP客户端
    client = FastMCP(
        access_key=access_key,
        secret_key=secret_key,
        api_base_url=api_base_url
    )
    
    # 设置默认下载目录
    client.default_download_dir = args.output
    
    print("VideoMCP 文本到图像生成")
    print(f"API基础URL: {client.api_base_url}")
    print(f"下载目录: {client.default_download_dir}")
    print(f"提示词: {args.prompt}")
    print(f"分辨率: {args.width}x{args.height}")
    print(f"生成数量: {args.count}")
    
    # 生成图像
    try:
        print("\n开始生成图像...")
        result = await client.text2img(
            prompt=args.prompt, 
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            img_count=args.count,
            seed=args.seed,
            download=True,
            use_ultra=args.ultra
        )
        
        # 输出结果
        if result:
            print("\n图像生成成功!")
            
            # 打印下载路径
            if "downloaded_files" in result:
                for i, file_path in enumerate(result["downloaded_files"]):
                    print(f"本地保存路径 {i+1}: {file_path}")
                    
            # 打印积分消耗
            if "pointsCost" in result:
                print(f"\n积分消耗: {result['pointsCost']}")
                
            # 打印剩余积分
            if "accountBalance" in result:
                print(f"剩余积分: {result['accountBalance']}")
        else:
            print("图像生成失败!")
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main() 