import re

# 常见技能关键词表（可不断扩展）
SKILL_KEYWORDS = [
    "Python", "Java", "C++", "SQL", "Linux",
    "机器学习", "深度学习", "推荐系统",
    "数据挖掘", "大模型", "NLP", "CV",
    "PyTorch", "TensorFlow"
]

def parse_job(jd_text: str) -> dict:
    """从岗位 JD 文本中解析岗位画像"""

    text = jd_text.lower()

    # ---------- 技能解析 ----------
    skills = []
    for s in SKILL_KEYWORDS:
        if s.lower() in text:
            skills.append(s)

    # ---------- 学历解析 ----------
    if "博士" in text:
        education = "博士"
    elif "硕士" in text or "研究生" in text:
        education = "硕士"
    elif "本科" in text:
        education = "本科"
    else:
        education = "不限"

    # ---------- 年限解析 ----------
    exp_match = re.search(r"(\d+)\s*年", text)
    if exp_match:
        experience = f"{exp_match.group(1)}年"
    else:
        experience = "不限"

    # ---------- 岗位方向解析 ----------
    if "算法" in text or "模型" in text:
        category = "算法"
    elif "后端" in text or "服务端" in text:
        category = "后端"
    elif "测试" in text:
        category = "测试"
    elif "数据" in text:
        category = "数据"
    else:
        category = "其他"

    return {
        "skills": skills,
        "education_level": education,
        "experience_years": experience,
        "job_category": category
    }
