"""
图像生成服务
提供基于fastmcp方式的图像生成相关功能
"""

import os
import json
import traceback
import time
import uuid
import aiohttp
import aiofiles
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import hmac
import base64

# 导入路径修正
from videomcp.utils.auth import AuthManager
from videomcp.utils.config import (
    ACCESS_KEY, SECRET_KEY, API_BASE_URL, HTTP_TIMEOUT
)

# API路径
TEXT2IMG_API = "/api/generate/webui/text2img"
TEXT2IMG_ULTRA_API = "/api/generate/webui/text2img/ultra"  # 旗舰版API
STATUS_API = "/api/generate/webui/status"  # 状态查询API路径

# 模板UUID
TEMPLATE_UUID = "6f7c4652458d4802969f8d089cf5b91f"
ULTRA_TEMPLATE_UUID = "5d7e67009b344550bc1aa6ccbfa1d7f4"  # 旗舰版模板UUID

# 模型UUID (checkPointId)
MODEL_UUID = "0ea388c7eb854be3ba3c6f65aac6bfd3"

# 默认下载路径
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP")


class FastMCP:
    """
    FastMCP客户端类
    提供更接近client.fastmcp的接口封装
    """
    
    def __init__(self, access_key=ACCESS_KEY, secret_key=SECRET_KEY, api_base_url=API_BASE_URL):
        """初始化FastMCP客户端"""
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_base_url = api_base_url
        self.default_download_dir = DEFAULT_DOWNLOAD_DIR
        
        # 创建下载目录
        os.makedirs(self.default_download_dir, exist_ok=True)
    
        # 创建auth实例
        self.auth = AuthManager(access_key, secret_key)
    
    async def download_image(self, image_url, filename=None):
        """
        下载图像
        
        Args:
            image_url: 图像URL
            filename: 自定义文件名，不提供则使用当前时间+随机数
            
        Returns:
            本地文件路径
        """
        if not filename:
            # 使用时间戳和随机数生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = str(uuid.uuid4())[:8]
            filename = f"image_{timestamp}_{random_suffix}.png"
        
        # 确保文件扩展名正确
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filename += '.png'
        
        # 构建完整文件路径
        file_path = os.path.join(self.default_download_dir, filename)
        
        # 下载图像
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        # 创建目录（如果不存在）
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        
                        # 保存文件
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(await response.read())
                        
                        print(f"图像已下载到: {file_path}")
                        return file_path
                    else:
                        print(f"下载失败，状态码: {response.status}")
                        return None
        except Exception as e:
            print(f"下载图像时出错: {e}")
            print(traceback.format_exc())
            return None
    
    async def text2img(self, prompt, negative_prompt=None, width=768, height=1024, 
                      img_count=1, seed=-1, download=True, use_ultra=False):
        """
        文本到图像生成
        
        Args:
            prompt: 提示词
            negative_prompt: 负面提示词
            width: 图像宽度
            height: 图像高度
            img_count: 生成图像数量
            seed: 随机种子，-1表示随机
            download: 是否下载生成的图像
            use_ultra: 是否使用旗舰版API
            
        Returns:
            图像生成结果，包含生成的图像URL列表和其他信息
        """
        # 选择API路径和模板UUID
        if use_ultra:
            uri = TEXT2IMG_ULTRA_API
            template_uuid = ULTRA_TEMPLATE_UUID
            
            # 旗舰版API使用简化参数
            request_data = {
                "templateUuid": template_uuid,
                "generateParams": {
                    "prompt": prompt,
                    "aspectRatio": "portrait" if height > width else "landscape",
                    "imgCount": img_count,
                }
            }
        else:
            uri = TEXT2IMG_API
            template_uuid = TEMPLATE_UUID
            
            # 标准API使用完整参数
            request_data = {
                "templateUuid": template_uuid,
                "generateParams": {
                    "checkPointId": MODEL_UUID,
                    "prompt": prompt,
                    "negativePrompt": negative_prompt or "ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),",
                    "sampler": 15,
                    "steps": 20,
                    "cfgScale": 7,
                    "width": width,
                    "height": height,
                    "imgCount": img_count,
                    "randnSource": 0,
                    "seed": seed,
                    "restoreFaces": 0,
                    "clipSkip": 2
                }
            }
        
        # 构建完整URL
        url = f"{self.api_base_url}{uri}"
        
        # 获取认证参数 (使用旧版签名)
        auth_params = self.auth.get_old_auth_params(uri)
        
        print(f"正在生成图像，请求URL: {url}")
        print(f"认证参数: {auth_params}")
        print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        # 发送请求
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=request_data, params=auth_params, timeout=HTTP_TIMEOUT) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    
                    print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
                    
                    if response_data.get("code") == 0 and "data" in response_data:
                        generate_uuid = response_data["data"].get("generateUuid")
                        print(f"\n生成请求已接受，任务ID: {generate_uuid}")
                        
                        # 等待生成完成
                        result = await self.wait_for_generation(generate_uuid)
                        
                        # 下载图像（如果需要）
                        if download and result and result.get("images"):
                            downloaded_files = []
                            for i, image in enumerate(result["images"]):
                                if image_url := image.get("imageUrl"):
                                    filename = f"{prompt[:20].replace(' ', '_')}_{i+1}.png"
                                    file_path = await self.download_image(image_url, filename)
                                    if file_path:
                                        downloaded_files.append(file_path)
                            
                            # 添加下载文件路径到结果
                            result["downloaded_files"] = downloaded_files
                        
                        return result
                    else:
                        print(f"\n生成图像请求失败: {response_data.get('msg', '未知错误')}")
                        return None
        except Exception as e:
            print(f"生成图像失败: {e}")
            print(f"错误详情: {traceback.format_exc()}")
            return None
    
    async def wait_for_generation(self, generate_uuid, polling_interval=5, timeout=120):
        """
        等待图像生成完成
        
        Args:
            generate_uuid: 生成任务UUID
            polling_interval: 轮询间隔（秒）
            timeout: 超时时间（秒）
            
        Returns:
            生成结果，包含图像URL等信息
        """
        print("\n等待图像生成完成...")
        
        start_time = time.time()
        
        # 构建URL和认证参数 (使用旧版签名)
        url = f"{self.api_base_url}{STATUS_API}"
        auth_params = self.auth.get_old_auth_params(STATUS_API)
        
        # 请求数据
        request_data = {
            "generateUuid": generate_uuid
        }
        
        # 轮询查询状态
        async with aiohttp.ClientSession() as session:
            while True:
                # 检查是否超时
                if time.time() - start_time > timeout:
                    print(f"任务超时，已经等待超过{timeout}秒")
                    return None
                
                try:
                    # 发送带认证参数的请求
                    async with session.post(url, json=request_data, params=auth_params) as response:
                        response.raise_for_status()
                        status_result = await response.json()
                        
                        if status_result.get("code") == 0:
                            data = status_result.get("data", {})
                            
                            # 打印生成状态和完成百分比
                            status = data.get('generateStatus', '未知')
                            percent = data.get('percentCompleted', 0) * 100
                            print(f"图像生成状态: {status}, 完成度: {percent:.2f}%")
                            
                            # 检查是否有图像数据
                            if data.get("images") and any(image for image in data["images"] if image is not None):
                                print("\n生成图像成功!")
                                
                                # 构建结果
                                result = {
                                    "images": data.get("images", []),
                                    "pointsCost": data.get("pointsCost"),
                                    "accountBalance": data.get("accountBalance"),
                                    "generateUuid": data.get("generateUuid")
                                }
                                
                                # 打印信息
                                print(f"点数消耗: {data.get('pointsCost')}")
                                print(f"账户余额: {data.get('accountBalance')}")
                                
                                return result
                        else:
                            print(f"查询失败: {status_result.get('msg', '未知错误')}")
                except Exception as e:
                    print(f"查询状态时出错: {e}")
                
                # 等待指定的时间后再次查询
                await asyncio.sleep(polling_interval)
    
    async def add_lora(self, request_data, lora_models):
        """
        添加LoRA模型到请求数据
        
        Args:
            request_data: 请求数据字典
            lora_models: LoRA模型信息列表
            
        Returns:
            更新后的请求数据
        """
        if not lora_models:
            return request_data
        
        if "generateParams" not in request_data:
            request_data["generateParams"] = {}
        
        request_data["generateParams"]["additionalNetwork"] = lora_models
        return request_data

    async def add_controlnet(self, request_data, controlnet_config):
        """
        添加ControlNet配置到请求数据
        
        Args:
            request_data: 请求数据字典
            controlnet_config: ControlNet配置列表
            
        Returns:
            更新后的请求数据
        """
        if not controlnet_config:
            return request_data
        
        if "generateParams" not in request_data:
            request_data["generateParams"] = {}
        
        request_data["generateParams"]["controlNet"] = controlnet_config
        return request_data
    
    async def add_hires_fix(self, request_data, hires_fix_config):
        """
        添加高分辨率修复配置到请求数据
        
        Args:
            request_data: 请求数据字典
            hires_fix_config: 高分辨率修复配置
            
        Returns:
            更新后的请求数据
        """
        if not hires_fix_config:
            return request_data
        
        if "generateParams" not in request_data:
            request_data["generateParams"] = {}
        
        request_data["generateParams"]["hiResFixInfo"] = hires_fix_config
        return request_data 

    async def test_connection(self) -> Dict[str, Any]:
        """
        测试API连接和密钥是否有效
        
        Returns:
            API响应，如果连接有效应该返回code=0的结果
        """
        # 使用轻量级请求测试API连接
        # 获取用户信息API通常消耗最少（不会实际生成内容）
        uri = "/api/getUserInfo"
        
        try:
            # 使用旧版签名方式生成签名（只针对测试连接）
            # 当前毫秒时间戳
            timestamp = str(int(time.time() * 1000))
            # 随机字符串
            signature_nonce = str(uuid.uuid4())
            # 拼接请求数据
            content = '&'.join((uri, timestamp, signature_nonce))
            
            # 生成HMAC-SHA1签名
            digest = hmac.new(self.secret_key.encode(), content.encode(), 'sha1').digest()
            # 移除为了补全base64位数而填充的尾部等号
            signature = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
            
            # 构建查询参数
            query_params = {
                "AccessKey": self.access_key,
                "Signature": signature,
                "Timestamp": timestamp,
                "SignatureNonce": signature_nonce
            }
            
            # 构建查询字符串并构造完整URL
            query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
            url = f"{self.api_base_url}{uri}?{query_string}"
            
            # 调试信息
            print(f"测试连接: {url}")
            print(f"认证参数: {query_params}")
            
            # 发送请求 - 注意：直接使用构造好的URL，不额外添加query参数
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            response_text = await response.text()
                            try:
                                result = json.loads(response_text)
                                return result
                            except json.JSONDecodeError:
                                return {
                                    "code": -1,
                                    "msg": f"无法解析响应JSON: {response_text[:100]}..."
                                }
                        else:
                            response_text = await response.text()
                            return {
                                "code": response.status,
                                "msg": f"HTTP错误: {response.status}, {response_text[:200]}"
                            }
                except asyncio.TimeoutError:
                    return {
                        "code": 408,
                        "msg": "请求超时，API服务器未响应"
                    }
                except Exception as e:
                    return {
                        "code": 500,
                        "msg": f"连接API服务器失败: {str(e)}"
                    }
        except Exception as e:
            # 认证过程中出错
            return {
                "code": 500,
                "msg": f"生成认证参数失败: {str(e)}"
            }

    async def query_template_list(self) -> Dict[str, Any]:
        """
        查询可用的模板列表
        
        Returns:
            API响应，包含可用模板列表
        """
        uri = "/api/model/queryModelTemplateList"
        
        try:
            # 使用旧版签名方式生成签名
            # 当前毫秒时间戳
            timestamp = str(int(time.time() * 1000))
            # 随机字符串
            signature_nonce = str(uuid.uuid4())
            # 拼接请求数据
            content = '&'.join((uri, timestamp, signature_nonce))
            
            # 生成HMAC-SHA1签名
            digest = hmac.new(self.secret_key.encode(), content.encode(), 'sha1').digest()
            # 移除为了补全base64位数而填充的尾部等号
            signature = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
            
            # 构建查询参数
            query_params = {
                "AccessKey": self.access_key,
                "Signature": signature,
                "Timestamp": timestamp,
                "SignatureNonce": signature_nonce
            }
            
            # 构建查询字符串并构造完整URL
            query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
            url = f"{self.api_base_url}{uri}?{query_string}"
            
            # 调试信息
            print(f"查询模板: {url}")
            print(f"认证参数: {query_params}")
            
            # 发送请求 - 注意：直接使用构造好的URL，不额外添加query参数
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            response_text = await response.text()
                            try:
                                result = json.loads(response_text)
                                return result
                            except json.JSONDecodeError:
                                return {
                                    "code": -1,
                                    "msg": f"无法解析响应JSON: {response_text[:100]}..."
                                }
                        else:
                            response_text = await response.text()
                            return {
                                "code": response.status,
                                "msg": f"HTTP错误: {response.status}, {response_text[:200]}"
                            }
                except asyncio.TimeoutError:
                    return {
                        "code": 408,
                        "msg": "请求超时，API服务器未响应"
                    }
                except Exception as e:
                    return {
                        "code": 500,
                        "msg": f"连接API服务器失败: {str(e)}"
                    }
        except Exception as e:
            # 认证过程中出错
            return {
                "code": 500,
                "msg": f"生成认证参数失败: {str(e)}"
            }

    async def generate_image(
        self,
        prompt: str,
        model: str = None,
        steps: int = 20,
        cfg_scale: float = 7.0,
        seed: int = -1,
        width: int = 512,
        height: int = 512,
        prompt_negative: str = None,
        output_format: str = "jpg",
        save_path: str = None,
        aspect_ratio: str = None,
        template_model: str = None,
        n: int = 1,
        samplers: str = "Euler a"
    ) -> Dict:
        """
        生成图像
        
        Args:
            prompt: 提示词
            model: 模型名称，对应checkPointId
            steps: 采样步数
            cfg_scale: CFG比例
            seed: 随机种子，-1表示随机
            width: 宽度
            height: 高度
            prompt_negative: 负面提示词
            output_format: 输出格式，jpg或png
            save_path: 保存路径，不提供则使用默认下载路径
            aspect_ratio: 长宽比，优先于width和height
            template_model: 模板模型UUID，对应templateUuid
            n: 生成图像数量
            samplers: 采样器名称
            
        Returns:
            生成结果字典
        """
        try:
            # 设置API端点
            uri = "/api/generate/webui/text2img"
            api_url = f"{self.api_base_url}{uri}"
            
            # 检查模板是否提供
            if not template_model:
                template_model = "6f7c4652458d4802969f8d089cf5b91f"  # 默认模板
            
            # 获取采样器ID
            sampler_id = self._get_sampler_id(samplers)
            
            # 构建请求数据
            request_data = {
                "templateUuid": template_model,
                "generateParams": {
                    "checkPointId": model if model else "0ea388c7eb854be3ba3c6f65aac6bfd3",  # 默认模型
                    "prompt": prompt,
                    "negativePrompt": prompt_negative if prompt_negative else "",
                    "sampler": sampler_id,
                    "steps": steps,
                    "cfgScale": cfg_scale,
                    "width": width,
                    "height": height,
                    "imgCount": n,
                    "randnSource": 0,
                    "seed": seed,
                    "restoreFaces": 0,
                    "clipSkip": 2
                }
            }
            
            # 如果有长宽比设置，应用长宽比
            if aspect_ratio:
                width, height = self._get_dimensions_from_ratio(aspect_ratio)
                request_data["generateParams"]["width"] = width
                request_data["generateParams"]["height"] = height
            
            # 获取旧式认证参数（使用HMAC-SHA1 + Base64URL）
            auth_params = self.auth.get_old_auth_params(uri)
            
            # 打印请求URL和认证参数
            print(f"正在生成图像，请求URL: {api_url}")
            print(f"认证参数: {auth_params}")
            
            # 打印请求数据
            print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
            
            # 发送POST请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url,
                    params=auth_params,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    # 解析响应
                    response_data = await response.json()
                    print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
                    
                    # 检查响应状态
                    if response_data.get("code") != 0:
                        error_msg = response_data.get("msg", "未知错误")
                        print(f"生成图像请求失败: {error_msg}")
                        return {"error": error_msg, "raw_response": response_data}
                    
                    # 提取结果
                    result_data = response_data.get("data", {})
                    images = result_data.get("outputList", [])
                    
                    # 保存图像
                    saved_images = []
                    if images:
                        for i, img_info in enumerate(images):
                            img_url = img_info.get("url")
                            if img_url:
                                # 保存图像
                                filename = f"{int(time.time())}_{i}.{output_format}"
                                img_path = await self._save_image(img_url, filename, save_path)
                                saved_images.append({"url": img_url, "local_path": img_path})
                    
                    # 构建返回结果
                    return {
                        "status": "success",
                        "images": saved_images,
                        "raw_response": response_data
                    }
                    
        except Exception as e:
            print(f"生成图像时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}

    def _get_sampler_id(self, sampler_name: str) -> int:
        """
        根据采样器名称获取采样器ID
        
        Args:
            sampler_name: 采样器名称
            
        Returns:
            采样器ID
        """
        samplers = {
            "Euler a": 15,
            "Euler": 5,
            "LMS": 2,
            "Heun": 7,
            "DPM2": 8,
            "DPM2 a": 9,
            "DPM++ 2S a": 11,
            "DPM++ 2M": 12,
            "DPM++ SDE": 14,
            "DPM Fast": 3,
            "DPM Adaptive": 4,
            "LMS Karras": 21,
            "DPM2 Karras": 23,
            "DPM2 a Karras": 24,
            "DPM++ 2S a Karras": 26,
            "DPM++ 2M Karras": 27,
            "DPM++ SDE Karras": 29,
            "DDIM": 0,
            "PLMS": 1
        }
        
        # 返回匹配的ID，如果找不到则默认使用Euler a (15)
        return samplers.get(sampler_name, 15)
    
    def _get_dimensions_from_ratio(self, ratio: str) -> tuple:
        """
        根据长宽比获取图像尺寸
        
        Args:
            ratio: 长宽比字符串，例如"1:1"
            
        Returns:
            (宽度, 高度)的元组
        """
        # 默认尺寸
        default_width, default_height = 512, 512
        
        # 常用长宽比预设
        ratio_presets = {
            "1:1": (512, 512),
            "4:3": (640, 480),
            "3:2": (768, 512),
            "16:9": (768, 432),
            "9:16": (432, 768),
            "2:3": (512, 768),
            "3:4": (480, 640)
        }
        
        # 如果是预设比例，直接返回
        if ratio in ratio_presets:
            return ratio_presets[ratio]
        
        # 尝试解析自定义比例
        try:
            width_ratio, height_ratio = map(int, ratio.split(':'))
            # 保持总像素数约为512*512
            scale = (512 * 512 / (width_ratio * height_ratio)) ** 0.5
            width = int(width_ratio * scale)
            height = int(height_ratio * scale)
            # 确保宽度和高度是8的倍数
            width = (width // 8) * 8
            height = (height // 8) * 8
            return width, height
        except Exception:
            # 解析失败，返回默认尺寸
            return default_width, default_height
    
    async def _save_image(self, image_url: str, filename: str, custom_path: str = None) -> str:
        """
        下载并保存图像
        
        Args:
            image_url: 图像URL
            filename: 文件名
            custom_path: 自定义保存路径，不提供则使用默认下载目录
            
        Returns:
            保存的本地文件路径
        """
        # 确定保存目录
        save_dir = custom_path if custom_path else self.default_download_dir
        os.makedirs(save_dir, exist_ok=True)
        
        # 构建完整文件路径
        file_path = os.path.join(save_dir, filename)
        
        # 下载图像
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        # 保存文件
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(await response.read())
                        print(f"图像已保存到: {file_path}")
                        return file_path
                    else:
                        print(f"下载图像失败，HTTP状态码: {response.status}")
                        return None
        except Exception as e:
            print(f"保存图像时发生错误: {e}")
            traceback.print_exc()
            return None 