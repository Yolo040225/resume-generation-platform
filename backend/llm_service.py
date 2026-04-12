# backend/llm_service.py
import os
from openai import OpenAI

def call_deepseek_chat(user_prompt: str, temperature: float = 0.4) -> str:
    """
    调用 DeepSeek（OpenAI兼容接口）并返回模型输出文本
    依赖环境变量：DEEPSEEK_API_KEY
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未检测到环境变量 DEEPSEEK_API_KEY，请先设置它。")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    resp = client.chat.completions.create(
        model="deepseek-chat",
        temperature=temperature,
        messages=[
            {"role": "system", "content": "你是一名严谨的职业发展顾问，必须遵守“不得虚构”的约束。"},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.choices[0].message.content
