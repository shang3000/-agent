import requests
import json

class LLMAdapter:
    """GLM API封装"""
    
    def __init__(self):
        """初始化LLM适配器"""
        # 这里需要配置GLM API的访问信息
        self.api_key = "YOUR_API_KEY"
        self.api_url = "https://api.zhipuai.com/v1/chat/completions"
    
    def generate(self, prompt, model="glm-4"):
        """调用GLM API生成文本
        
        Args:
            prompt: 提示文本
            model: 模型名称
            
        Returns:
            str: 生成的文本
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"调用GLM API失败: {str(e)}")
            return "LLM分析失败"
