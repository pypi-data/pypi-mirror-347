"""
微信支付签名工具
"""

import os
import time
import uuid
import base64
import logging
from datetime import datetime
from typing import Dict, Optional
from cryptography.hazmat.primitives.hashes import Hash, SHA256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger("wxpay-mcp")

class WxPaySignUtils:
    """微信支付签名工具类"""
    
    def __init__(self, mchid: str, serial_no: str, private_key_content: str, wx_pub_key_content: Optional[str] = None):
        """
        初始化签名工具类
        
        Args:
            mchid: 商户号
            serial_no: 商户证书序列号
            private_key_content: 商户私钥内容（PEM格式）
            wx_pub_key_content: 微信支付平台公钥内容（PEM格式），可选
        """
        self.mchid = mchid
        self.serial_no = serial_no
        
        # 加载商户私钥
        logger.debug("正在加载商户私钥")
        # 确保私钥内容中的 \n 被正确解析为换行符
        private_key_content = private_key_content.replace('\\n', '\n')
        private_key_data = private_key_content.encode('utf-8')
        logger.debug(f"私钥内容前32字符: {private_key_data[:32]}")
        try:
            self.private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None
            )
            logger.debug("私钥加载成功")
        except Exception as e:
            logger.error(f"私钥加载失败: {str(e)}")
            raise
            
        # 加载微信支付平台公钥（如果提供）
        self.wx_pub_key = None
        if wx_pub_key_content:
            logger.debug("正在加载微信支付平台公钥")
            # 确保公钥内容中的 \n 被正确解析为换行符
            wx_pub_key_content = wx_pub_key_content.replace('\\n', '\n')
            public_key_data = wx_pub_key_content.encode('utf-8')
            logger.debug(f"公钥内容前32字符: {public_key_data[:32]}")
            try:
                self.wx_pub_key = serialization.load_pem_public_key(public_key_data)
                logger.debug("公钥加载成功")
            except Exception as e:
                logger.error(f"公钥加载失败: {str(e)}")
                raise
        else:
            logger.warning("未提供微信支付平台公钥内容，将跳过响应签名验证")

    def generate_order_no(self) -> str:
        """生成商户订单号，格式：yyyyMMddHHmmss + 10位随机数"""
        date_str = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4().int)[:10]
        return f"{date_str}{random_str}"

    def _calculate_signature(self, message: str) -> str:
        """计算签名"""
        logger.debug(f"待签名内容: {message}")
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PKCS1v15(),
            SHA256()
        )
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        logger.debug(f"生成的签名: {signature_b64}")
        return signature_b64

    def generate_authorization(self, method: str, url_path: str, body: str = '') -> Dict[str, str]:
        """
        生成请求头中的Authorization
        
        Args:
            method: HTTP请求方法
            url_path: 请求路径
            body: 请求体
            
        Returns:
            Dict[str, str]: 包含Authorization头的字典
        """
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4()).replace('-', '')
        
        # 构造签名串
        sign_str = f"{method}\n{url_path}\n{timestamp}\n{nonce}\n{body}\n"
        logger.debug("构造签名串:")
        logger.debug(f"HTTP方法: {method}")
        logger.debug(f"请求路径: {url_path}")
        logger.debug(f"时间戳: {timestamp}")
        logger.debug(f"随机串: {nonce}")
        logger.debug(f"请求体: {body}")
        logger.debug(f"完整签名串: {sign_str}")
        
        signature = self._calculate_signature(sign_str)
        
        # 构造认证信息
        auth_info = {
            'mchid': self.mchid,
            'serial_no': self.serial_no,
            'nonce_str': nonce,
            'timestamp': timestamp,
            'signature': signature
        }
        
        # 构造Authorization头
        auth_str = 'WECHATPAY2-SHA256-RSA2048 ' + ','.join([f'{k}="{v}"' for k, v in auth_info.items()])
        logger.debug(f"生成的Authorization头: {auth_str}")
        return {'Authorization': auth_str}

    def verify_response(self, headers: Dict[str, str], body: str) -> bool:
        """
        验证响应签名
        
        Args:
            headers: 响应头
            body: 响应体
            
        Returns:
            bool: 如果未提供公钥，返回True；如果提供了公钥，返回验证结果
        """
        # 如果未提供公钥，跳过验证
        if not self.wx_pub_key:
            logger.warning("未提供微信支付平台公钥，跳过响应签名验证")
            return True
            
        logger.debug("开始验证响应签名")
        timestamp = headers.get('Wechatpay-Timestamp')
        nonce = headers.get('Wechatpay-Nonce')
        signature = headers.get('Wechatpay-Signature')
        serial_no = headers.get('Wechatpay-Serial')
        
        logger.debug(f"响应头 Wechatpay-Timestamp: {timestamp}")
        logger.debug(f"响应头 Wechatpay-Nonce: {nonce}")
        logger.debug(f"响应头 Wechatpay-Signature: {signature}")
        logger.debug(f"响应头 Wechatpay-Serial: {serial_no}")
        logger.debug(f"响应体: {body}")
        
        if not all([timestamp, nonce, signature, serial_no]):
            logger.error("响应头缺少必要的签名信息")
            logger.error(f"完整响应头: {headers}")
            return False
            
        # 构造验签名串
        message = f"{timestamp}\n{nonce}\n{body}\n"
        logger.debug("构造验签名串:")
        logger.debug(f"时间戳: {timestamp}")
        logger.debug(f"随机串: {nonce}")
        logger.debug(f"响应体: {body}")
        logger.debug(f"完整验签名串: {message}")
        
        try:
            # Base64解码签名
            signature_bytes = base64.b64decode(signature)
            logger.debug(f"解码后的签名长度: {len(signature_bytes)} 字节")
            
            # 验证签名
            self.wx_pub_key.verify(
                signature_bytes,
                message.encode('utf-8'),
                padding.PKCS1v15(),
                SHA256()
            )
            logger.debug("签名验证成功")
            return True
        except InvalidSignature as e:
            logger.error("签名验证失败: 无效的签名")
            logger.error(f"异常信息: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"签名验证过程出现异常: {str(e)}")
            return False

    def sign_jsapi_params(self, appid: str, prepay_id: str) -> Dict[str, str]:
        """
        生成JSAPI调起支付参数的签名
        
        Args:
            appid: 应用ID
            prepay_id: 预支付交易会话标识
            
        Returns:
            Dict[str, str]: JSAPI调起支付参数
        """
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4()).replace('-', '')
        package = f"prepay_id={prepay_id}"
        
        # 构造签名串
        message = f"{appid}\n{timestamp}\n{nonce}\n{package}\n"
        logger.debug("构造JSAPI支付参数签名串:")
        logger.debug(f"应用ID: {appid}")
        logger.debug(f"时间戳: {timestamp}")
        logger.debug(f"随机串: {nonce}")
        logger.debug(f"订单包: {package}")
        logger.debug(f"完整签名串: {message}")
        
        signature = self._calculate_signature(message)
        
        return {
            'timeStamp': timestamp,
            'nonceStr': nonce,
            'package': package,
            'signType': 'RSA',
            'paySign': signature
        }
