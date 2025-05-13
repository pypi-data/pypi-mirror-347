import json
import requests
import importlib
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class DetectionResult:
    """
    检测结果数据类
    """
    risk_score: float = 0.0
    risk_type: str = ""
    risk_reason: str = ""
    error: Optional[str] = None


class AISec:
    """
    AI应用安全SDK，用于检测会话当中是否存在prompt注入等恶意攻击行为
    """
    
    def __init__(
        self, 
        app_uk: str,
        timeout: int = 10
    ):
        """
        初始化AISec客户端
        
        Args:
            app_uk: 公司唯一应用标识
        """
        if not app_uk:
            raise ValueError("app_uk为必须参数")
            
        self.app_uk = app_uk
        self.timeout = timeout
        
    def detect(self, messages: List[Dict[str, str]]) -> DetectionResult:
        """
        检测消息中是否存在安全风险
        
        Args:
            messages: 消息列表，格式与大模型API一致
            
        Returns:
            DetectionResult: 检测结果
        """
        if not messages:
            return DetectionResult(error="消息列表不能为空")
            
        try:
            try:
                aisec_pkg = importlib.import_module('aisec')
                sdk_version = getattr(aisec_pkg, '__version__')
            except ImportError:
                sdk_version = 'unknown'  
                
            payload = {
                "messages": messages,
                "app_uk": self.app_uk,
                "sdk_version": sdk_version  
            }
            
            headers = {
                "Content-Type": "application/json",
            }
        
            security_endpoint = f"https://aisec.17usoft.com/prompt_security/api/v1/detect"
            response = requests.post(
                security_endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                return DetectionResult(
                    error=f"API请求失败，状态码: {response.status_code}, 响应: {response.text}"
                )

            result = response.json()
            if result.get("success") != True:
                return DetectionResult(
                    error= result.get("error")
                )

            return DetectionResult(
                risk_score=result.get("risk_score", 0.0),
                risk_type=result.get("risk_type", ""),
                risk_reason=result.get("risk_reason", "")
            )
            
        except requests.RequestException as e:
            return DetectionResult(error=f"网络请求异常: {str(e)}")
        except json.JSONDecodeError:
            return DetectionResult(error="API响应格式错误")
        except Exception as e:
            return DetectionResult(error=f"未知错误: {str(e)}")