def build_prompt(resume_text: str, job_profile: dict, job_title: str, job_jd: str) -> str:
    skills = ", ".join(job_profile.get("skills", []))

    prompt = f"""
    你是一名专业的职业发展顾问，擅长根据岗位需求优化求职简历。

    你的任务是：根据【目标岗位】和【原始简历】，对简历进行优化，使其更符合岗位要求。

    ==============================
    【目标岗位】
    {job_title}

    【岗位描述】
    {job_jd}

    【岗位画像】
    岗位类型：{job_profile.get("job_category", "")}
    核心技能：{skills}
    学历要求：{job_profile.get("education_level", "")}
    经验要求：{job_profile.get("experience_years", "")}

    ==============================
    【原始简历】
    {resume_text}

    ==============================
    【优化规则】

    1. 不得编造任何不存在的经历或技能
    2. 只能基于原始简历内容进行优化和重写
    3. 可以调整语句表达，使其更加专业和符合岗位关键词
    4. 可以调整简历结构和要点顺序
    5. 如果原始简历信息较少，请保持简洁，不要虚构内容

    ==============================
    【输出要求（极其重要）】

    你必须且只能输出一个合法的 JSON 格式字符串，不要输出任何解释、分析、建议或任何说明文字。
    绝对不要输出 Markdown 的代码块标记（如 ```json 和 ```），直接输出纯 JSON 原文即可！

    输出的 JSON 结构必须严格如下：

    {{
        "personal_info": {{
            "name": "姓名（如果原始简历没有则留空）",
            "contact": "电话/邮箱（如果原始简历没有则留空）",
            "intent": "求职意向"
        }},
        "educations": [
            {{"time": "2022-2026", "school": "XX大学", "major": "专业", "note": "补充说明"}}
        ],
        "experiences": [
            {{"time": "2024", "title": "项目/实习名称", "role": "角色", "desc": "优化后的要点1<br>优化后的要点2"}}
        ],
        "skills": ["技能1", "技能2", "技能3"]
    }}
    """
    return prompt