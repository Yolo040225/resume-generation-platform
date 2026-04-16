import json
import re
from backend.llm_service import call_deepseek_chat


def parse_job(jd_text: str) -> dict:
    """利用大模型从岗位 JD 文本中深度解析岗位画像"""

    # 构造专门用于信息抽取的 Prompt
    prompt = f"""
    你是一个资深的HR和算法专家。请从以下非结构化的岗位描述(JD)中提取结构化信息。

    【岗位描述】：
    {jd_text}

    请严格输出一个合法的 JSON 格式字符串，不要包含任何其他解释性文字，不要使用 Markdown 代码块。格式必须严格遵守如下结构：
    {{
        "skills": ["技能1", "技能2", "技能3"], 
        "education_level": "学历要求", 
        "experience_years": "经验年限要求", 
        "job_category": "岗位类别" 
    }}

    提取规则：
    1. skills：提取核心专业技能关键词，如果没有则为空列表 []。
    2. education_level：提取如 专科、本科、硕士、博士、不限 等。
    3. experience_years：提取如 1-3年、3-5年、不限 等。
    4. job_category：归纳岗位的大类，如 算法、后端、前端、数据、测试、产品 等。
    """

    try:
        # 这里的 temperature 设低一点 (比如 0.1)，保证抽取任务的确定性和格式的稳定性
        response_text = call_deepseek_chat(prompt, temperature=0.1)

        # 容错处理：清洗大模型可能返回的 Markdown 标记 (如 ```json ... ```)
        clean_text = re.sub(r"```json", "", response_text)
        clean_text = re.sub(r"```", "", clean_text).strip()

        # 将文本转化为 Python 字典
        profile = json.loads(clean_text)

        # 补齐可能缺失的字段，保证下游程序不报错
        return {
            "skills": profile.get("skills", []),
            "education_level": profile.get("education_level", "不限"),
            "experience_years": profile.get("experience_years", "不限"),
            "job_category": profile.get("job_category", "其他")
        }

    except Exception as e:
        print(f"JD 解析发生异常: {str(e)}")
        # 兜底返回值，防止程序崩溃
        return {
            "skills": [],
            "education_level": "解析失败",
            "experience_years": "解析失败",
            "job_category": "解析失败"
        }