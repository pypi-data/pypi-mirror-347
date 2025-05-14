"""
MCP 服务器实现
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
from .sign_utils import WxPaySignUtils

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("wxpay-mcp")

# 加载环境变量
load_dotenv()

# 初始化 MCP 服务器
mcp = FastMCP("wxpay-mcp-server")

# 微信支付 API 配置
WXPAY_API_BASE = "https://api.mch.weixin.qq.com"
SP_MCHID = os.getenv("WXPAY_SP_MCHID")
SP_APPID = os.getenv("WXPAY_SP_APPID")
SUB_MCHID = os.getenv("WXPAY_SUB_MCHID")
SUB_APPID = os.getenv("WXPAY_SUB_APPID")
CERT_SERIAL_NO = os.getenv("WXPAY_CERT_SERIAL_NO")
PRIVATE_KEY_CONTENT = os.getenv("WXPAY_PRIVATE_KEY")
WX_PUB_KEY_CONTENT = os.getenv("WXPAY_PUBLIC_KEY")
NOTIFY_URL = os.getenv("WXPAY_NOTIFY_URL")

# 验证必要的配置
required_configs = {
    "WXPAY_SP_MCHID": SP_MCHID,
    "WXPAY_SP_APPID": SP_APPID,
    "WXPAY_CERT_SERIAL_NO": CERT_SERIAL_NO,
    "WXPAY_PRIVATE_KEY": PRIVATE_KEY_CONTENT,
    "WXPAY_NOTIFY_URL": NOTIFY_URL
}

for config_name, config_value in required_configs.items():
    if not config_value:
        logger.error(f"缺少必要的配置项: {config_name}")
        raise ValueError(f"缺少必要的配置项: {config_name}")

# 初始化签名工具
try:
    sign_utils = WxPaySignUtils(
        mchid=SP_MCHID,
        serial_no=CERT_SERIAL_NO,
        private_key_content=PRIVATE_KEY_CONTENT,
        wx_pub_key_content=WX_PUB_KEY_CONTENT
    )
    logger.info("签名工具初始化成功")
except Exception as e:
    logger.error(f"签名工具初始化失败: {str(e)}")
    raise

class WxPayAPIError(Exception):
    """微信支付 API 错误"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

@mcp.tool()
def create_jsapi_order(description: str, amount_cents: int, payer_openid: str, out_trade_no: Optional[str] = None) -> Dict[str, Any]:
    """创建微信支付 JSAPI 订单
    
    Args:
        description: 【商品描述】商品描述
        amount_cents: 【订单金额】订单总金额，单位为分
        payer_openid: 【用户标识】用户在服务商appid或子商户appid下的唯一标识
        out_trade_no: 【商户订单号】服务商系统内部订单号，要求6-32个字符内，只能是数字、大小写字母_-|* 且在同一个服务商商户号下唯一
        
    Returns:
        Dict[str, Any]: 包含以下字段的字典:
            - out_trade_no: 商户订单号
            - jsapi_params: JSAPI调起支付参数
    """
    try:
        url = f"{WXPAY_API_BASE}/v3/pay/partner/transactions/jsapi"
        
        # 生成商户订单号（如果未提供）
        final_out_trade_no = out_trade_no or sign_utils.generate_order_no()
        logger.info(f"创建支付订单 - 商户订单号: {final_out_trade_no}")
        
        # 准备请求体
        body = {
            "sp_appid": SP_APPID,
            "sp_mchid": SP_MCHID,
            "sub_appid": SUB_APPID,
            "sub_mchid": SUB_MCHID,
            "description": description,
            "out_trade_no": final_out_trade_no,
            "amount": {
                "total": amount_cents,
                "currency": "CNY"
            },
            "notify_url": NOTIFY_URL,
            "payer": {
                "sp_openid": payer_openid if not SUB_APPID else None,
                "sub_openid": payer_openid if SUB_APPID else None
            }
        }
        
        # 移除空值
        if not body["payer"].get("sp_openid"):
            del body["payer"]["sp_openid"]
        if not body["payer"].get("sub_openid"):
            del body["payer"]["sub_openid"]
        if not SUB_APPID:
            del body["sub_appid"]
        
        logger.debug(f"请求参数: {json.dumps(body, ensure_ascii=False)}")
        
        # 获取认证头
        headers = sign_utils.generate_authorization(
            method="POST",
            url_path="/v3/pay/partner/transactions/jsapi",
            body=json.dumps(body)
        )
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        
        # 发送请求
        logger.info("发送创建订单请求")
        response = requests.post(url, json=body, headers=headers)
        response_body = response.text
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f"创建订单失败 - HTTP {response.status_code}")
            logger.error(f"响应内容: {response_body}")
            raise WxPayAPIError(
                f"创建订单失败: HTTP {response.status_code}",
                status_code=response.status_code,
                response_body=response_body
            ) from e
        
        # 验证响应签名
        if not sign_utils.verify_response(response.headers, response_body):
            logger.error("响应签名验证失败")
            logger.error(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False)}")
            logger.error(f"响应体: {response_body}")
            raise WxPayAPIError("响应签名验证失败")
        
        # 解析响应
        result = response.json()
        logger.info(f"创建订单成功 - 预支付交易会话标识: {result.get('prepay_id')}")
        
        # 生成 JSAPI 调起支付参数
        jsapi_params = sign_utils.sign_jsapi_params(
            appid=SUB_APPID or SP_APPID,
            prepay_id=result["prepay_id"]
        )
        logger.debug(f"生成支付参数: {json.dumps(jsapi_params, ensure_ascii=False)}")
        
        return {
            "out_trade_no": final_out_trade_no,
            "jsapi_params": jsapi_params
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {str(e)}")
        raise WxPayAPIError(f"请求异常: {str(e)}") from e
    except json.JSONDecodeError as e:
        logger.error(f"响应解析失败: {str(e)}")
        logger.error(f"原始响应: {response_body}")
        raise WxPayAPIError("响应解析失败") from e
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        raise

@mcp.tool()
def query_order(out_trade_no: str) -> Dict[str, Any]:
    """查询订单状态
    
    Args:
        out_trade_no: 【商户订单号】商户系统内部订单号
        
    Returns:
        Dict[str, Any]: 订单信息，包含交易状态等字段
    """
    try:
        logger.info(f"查询订单 - 商户订单号: {out_trade_no}")
        url = f"{WXPAY_API_BASE}/v3/pay/partner/transactions/out-trade-no/{out_trade_no}"
        
        # 构造查询参数
        query_params = {
            "sp_mchid": SP_MCHID,
            "sub_mchid": SUB_MCHID
        }
        logger.debug(f"查询参数: {json.dumps(query_params, ensure_ascii=False)}")
        
        # 获取认证头
        headers = sign_utils.generate_authorization(
            method="GET",
            url_path=f"/v3/pay/partner/transactions/out-trade-no/{out_trade_no}?sp_mchid={SP_MCHID}&sub_mchid={SUB_MCHID}"
        )
        headers["Accept"] = "application/json"
        
        # 发送请求
        logger.info("发送查询请求")
        response = requests.get(url, params=query_params, headers=headers)
        response_body = response.text
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f"查询订单失败 - HTTP {response.status_code}")
            logger.error(f"响应内容: {response_body}")
            raise WxPayAPIError(
                f"查询订单失败: HTTP {response.status_code}",
                status_code=response.status_code,
                response_body=response_body
            ) from e
        
        # 验证响应签名
        if not sign_utils.verify_response(response.headers, response_body):
            logger.error("响应签名验证失败")
            logger.error(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False)}")
            logger.error(f"响应体: {response_body}")
            raise WxPayAPIError("响应签名验证失败")
        
        # 解析响应
        result = response.json()
        logger.info(f"查询订单成功 - 支付状态: {result.get('trade_state')}")
        logger.debug(f"订单详情: {json.dumps(result, ensure_ascii=False)}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {str(e)}")
        raise WxPayAPIError(f"请求异常: {str(e)}") from e
    except json.JSONDecodeError as e:
        logger.error(f"响应解析失败: {str(e)}")
        logger.error(f"原始响应: {response_body}")
        raise WxPayAPIError("响应解析失败") from e
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        raise

def run_server():
    """运行 MCP 服务器"""
    logger.info("启动微信支付 MCP 服务器")
    mcp.run()

if __name__ == "__main__":
    run_server()
