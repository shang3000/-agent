"""
单独测试 LLM (GLM-4) 调用
用于验证 API 是否正常工作
"""

from agent.llm_adapter import LLMAdapter


def test_llm():
    print("开始测试 GLM-4 API 调用...\n")

    llm = LLMAdapter()

    # 测试用的简单 Prompt
    test_prompt = """你好，请用一句话介绍自己是什么模型，以及今天是2026年4月。"""

    print("发送测试请求...")
    try:
        response = llm.generate(test_prompt, model="glm-4")

        print("\n" + "=" * 60)
        print("✅ LLM 调用成功！")
        print("=" * 60)
        print("模型回复：")
        print(response)
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ LLM 调用失败")
        print(f"错误信息: {e}")
        print("=" * 60)


if __name__ == "__main__":
    test_llm()