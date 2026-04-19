import requests
import logging
import time

logger = logging.getLogger(__name__)


class LLMAdapter:
    """智谱 BigModel (GLM) API 封装 - 适配你的 Key"""

    def __init__(self):
        # 请确保这里填的是你最新的智谱 Key（以 9187 开头）
        self.api_key = "API_KEY"  # ←←← 确认是这个
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"  # 智谱官方推荐地址
        self.timeout = 90
        self.max_retries = 2

        logger.info("✅ LLMAdapter 初始化完成，使用智谱 BigModel (GLM-4)")

    def generate(self, prompt: str, model: str = "glm-4"):
        """调用智谱 GLM API 生成文本"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9
        }

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                    # verify=False  # 临时关闭 SSL 验证，解决常见连接问题
                )
                response.raise_for_status()

                result = response.json()
                content = result["choices"][0]["message"]["content"]

                logger.info(f"✅ GLM 调用成功 (模型: {model})")
                return content.strip()

            except Exception as e:
                logger.warning(f"LLM 请求失败 (尝试 {attempt + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(3)  # 重试间隔

        logger.error("LLM 调用多次失败，返回默认提示")
        return "LLM 分析失败，请检查 API Key 或网络连接。"
