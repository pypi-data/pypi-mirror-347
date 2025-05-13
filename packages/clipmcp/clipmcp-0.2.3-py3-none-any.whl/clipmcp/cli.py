#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行接口
提供clipmcp命令的入口点
"""

import os
import sys
import click
import asyncio
from pathlib import Path

# 尝试导入图像生成服务
try:
    from clipmcp.services.image_service import ImageService
except ImportError:
    # 添加项目根目录到sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from clipmcp.services.image_service import ImageService

# 获取环境变量
def get_env():
    """获取环境变量"""
    return {
        'access_key': os.environ.get('VIDEOMCP_ACCESS_KEY'),
        'secret_key': os.environ.get('VIDEOMCP_SECRET_KEY'),
        'api_base_url': os.environ.get('VIDEOMCP_API_BASE_URL', 'https://openapi.liblibai.cloud'),
        'download_dir': os.environ.get('VIDEOMCP_DOWNLOAD_DIR', 
                                        os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP"))
    }

@click.group()
def cli():
    """VideoMCP命令行工具 - 提供图像生成等功能"""
    pass

@cli.command()
@click.argument('prompt')
@click.option('--negative', '-n', help='负面提示词')
@click.option('--width', '-w', type=int, default=768, help='图像宽度')
@click.option('--height', '-h', type=int, default=1024, help='图像高度')
@click.option('--count', '-c', type=int, default=1, help='生成图像数量')
@click.option('--seed', '-s', type=int, default=-1, help='随机种子，-1为随机')
@click.option('--ultra/--no-ultra', default=False, help='是否使用旗舰版API')
@click.option('--output', '-o', help='输出目录')
def generate(prompt, negative, width, height, count, seed, ultra, output):
    """生成图像"""
    click.echo(f"正在生成图像: '{prompt}'")
    
    # 获取环境变量
    env = get_env()
    
    # 验证API密钥
    if not env['access_key'] or not env['secret_key']:
        click.echo("错误: 未设置API密钥！请设置VIDEOMCP_ACCESS_KEY和VIDEOMCP_SECRET_KEY环境变量。")
        sys.exit(1)
    
    # 设置输出目录
    output_dir = output or env['download_dir']
    
    # 创建客户端
    client = ImageService(
        access_key=env['access_key'],
        secret_key=env['secret_key'],
        api_base_url=env['api_base_url'],
        download_dir=output_dir
    )
    
    # 运行异步函数
    result = asyncio.run(client.text2img(
        prompt=prompt,
        negative_prompt=negative,
        width=width,
        height=height,
        img_count=count,
        seed=seed,
        download=True,
        use_ultra=ultra
    ))
    
    # 处理结果
    if result:
        # 检查是否有图像和下载文件
        has_images = 'images' in result and len(result.get('images', [])) > 0
        has_downloads = 'downloaded_files' in result and len(result.get('downloaded_files', [])) > 0
        
        if has_images or has_downloads:
            click.echo(f"\n✅ 成功生成{len(result.get('images', []))}张图像！")
            
            # 显示下载路径
            if has_downloads:
                click.echo("\n下载文件:")
                for path in result.get('downloaded_files'):
                    click.echo(f"- {path}")
            
            # 显示积分消耗
            if 'pointsCost' in result:
                click.echo(f"\n积分消耗: {result['pointsCost']}")
                click.echo(f"账户余额: {result.get('accountBalance', '未知')}")
            
            return
        
    # 失败处理
    error_msg = result.get('error', '未知错误') if result else '请求失败'
    click.echo(f"\n❌ 生成失败: {error_msg}")
    sys.exit(1)

def main():
    """命令行工具主函数"""
    cli()

if __name__ == "__main__":
    main()