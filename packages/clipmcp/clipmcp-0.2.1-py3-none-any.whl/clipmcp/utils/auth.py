"""
认证管理模块
提供API认证参数生成功能
"""

import time
import hmac
import uuid
import hashlib
import base64
import logging
from typing import Dict, Any

# 调试控制
DEBUG = False

def debug_log(message):
    """记录调试日志"""
    if DEBUG:
        print(f"[Auth Debug] {message}")
    # 同时写入日志文件
    logging.debug(message)

class AuthManager:
    """认证管理器"""
    
    def __init__(self, access_key: str, secret_key: str):
        """
        初始化认证管理器
        
        Args:
            access_key: API接入密钥
            secret_key: API密钥
        """
        if not access_key or not secret_key:
            raise ValueError("Access key and secret key are required")
        
        self.access_key = access_key
        self.secret_key = secret_key
        debug_log(f"初始化认证管理器: access_key={access_key}")
    
    def make_sign(self, uri: str) -> Dict[str, str]:
        """
        基于URI生成签名（使用旧的签名方法：HMAC-SHA1 + Base64URL）
        
        Args:
            uri: API URI路径，例如 "/api/generate/webui/text2img"
            
        Returns:
            包含签名信息的字典
        """
        # 生成当前毫秒时间戳
        timestamp = str(int(time.time() * 1000))
        # 生成随机字符串
        signature_nonce = str(uuid.uuid4())
        # 拼接请求数据
        content = '&'.join((uri, timestamp, signature_nonce))
        
        # 使用HMAC-SHA1生成签名
        digest = hmac.new(self.secret_key.encode(), content.encode(), 'sha1').digest()
        # 移除为了补全base64位数而填充的尾部等号
        signature = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
        
        debug_log(f"旧式签名生成: URI={uri}, 时间戳={timestamp}, 随机字符串={signature_nonce}")
        debug_log(f"生成的签名: {signature}")
        
        return {
            "timestamp": timestamp,
            "signature": signature,
            "signature_nonce": signature_nonce
        }
    
    def generate_signature(self, params: Dict[str, Any], timestamp: str = None, nonce: str = None) -> str:
        """
        生成签名（使用新的签名方法：HMAC-SHA256 + hexdigest）
        
        Args:
            params: 请求参数
            timestamp: 时间戳，不提供则自动生成
            nonce: 随机字符串，不提供则自动生成
            
        Returns:
            签名字符串
        """
        # 使用提供的timestamp或生成新的
        if not timestamp:
            timestamp = str(int(time.time()))
        
        # 使用提供的nonce或生成新的
        if not nonce:
            nonce = str(uuid.uuid4())[:8]
        
        # 构建签名字符串 (按照参数名称字母顺序排序)
        signature_parts = [f"accessKey={self.access_key}", f"timestamp={timestamp}", f"nonce={nonce}"]
        
        # 添加其他参数
        for key in sorted(params.keys()):
            signature_parts.append(f"{key}={params[key]}")
        
        # 拼接签名字符串
        signature_str = "&".join(signature_parts)
        
        # 使用HMAC-SHA256计算签名
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            signature_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        debug_log(f"新式签名生成: 签名字符串={signature_str}")
        debug_log(f"生成的签名: {signature}")
        
        return signature
    
    def get_auth_params(self, params: Dict[str, Any] = None) -> Dict[str, str]:
        """
        获取认证参数
        
        Args:
            params: 请求参数，会被包含在签名中
            
        Returns:
            包含认证信息的参数字典
        """
        if params is None:
            params = {}
        
        # 生成当前时间戳和随机字符串
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())[:8]
        
        # 生成签名
        signature = self.generate_signature(params, timestamp, nonce)
        
        # 构建认证参数
        auth_params = {
            "accessKey": self.access_key,
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }
        
        debug_log(f"生成鉴权参数: {auth_params}")
        return auth_params
    
    def get_old_auth_params(self, uri: str) -> Dict[str, str]:
        """
        获取旧式认证参数 (使用HMAC-SHA1 + Base64URL)
        
        Args:
            uri: API URI路径
            
        Returns:
            包含鉴权信息的字典
        """
        # 获取签名信息
        sign_info = self.make_sign(uri)
        
        # 构建认证参数
        auth_params = {
            "AccessKey": self.access_key,
            "Signature": sign_info["signature"],
            "Timestamp": sign_info["timestamp"],
            "SignatureNonce": sign_info["signature_nonce"]
        }
        
        debug_log(f"生成旧式鉴权参数: {auth_params}")
        return auth_params
    
    def attach_auth_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        向现有参数中添加认证参数
        
        Args:
            params: 现有参数
            
        Returns:
            包含认证信息的参数字典
        """
        auth_params = self.get_auth_params()
        return {**params, **auth_params}
    
    def verify_signature(self, params: Dict[str, Any], signature: str) -> bool:
        """
        验证签名
        
        Args:
            params: 请求参数（不包含signature）
            signature: 收到的签名
            
        Returns:
            签名是否有效
        """
        # 从参数中提取时间戳和随机字符串
        timestamp = params.get('timestamp', '')
        nonce = params.get('nonce', '')
        
        # 移除认证相关参数
        verification_params = params.copy()
        verification_params.pop('accessKey', None)
        verification_params.pop('timestamp', None)
        verification_params.pop('nonce', None)
        verification_params.pop('signature', None)
        
        # 生成用于验证的签名
        expected_signature = self.generate_signature(verification_params, timestamp, nonce)
        
        # 比较签名
        return expected_signature == signature 