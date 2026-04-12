from backend.llm_service import call_deepseek_chat
from backend.prompt_builder import build_prompt
from backend.resume_builder import build_resume_text
from ui.state import AppState

if __name__ == "__main__":
    state = AppState()

    # 模拟测试数据（等会改成真实数据）
    state.educations = [
        {"time": "2022-2026", "school": "XX大学", "major": "计算机科学", "note": "GPA 3.8"}
    ]

    state.experiences = [
        {"time": "2024", "title": "推荐系统项目", "role": "算法开发", "desc": "实现CTR预测模型"}
    ]

    state.skills = ["Python", "PyTorch", "机器学习"]

    resume_text = build_resume_text(state)

    job_profile = {
        "skills": ["Python", "推荐系统", "机器学习"],
        "education_level": "本科",
        "experience_years": "不限",
        "job_category": "算法工程师"
    }

    prompt = build_prompt(resume_text, job_profile, "推荐算法工程师")

    result = call_deepseek_chat(prompt, temperature=0.4)

    print("====== 优化结果 ======")
    print(result)
