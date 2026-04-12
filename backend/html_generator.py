# project/backend/html_generator.py
import json

def generate_html_from_json(json_str: str) -> str:
    try:
        # 解析大模型返回的 JSON
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return "<h1>JSON 解析失败，请检查大模型输出格式</h1>"

    # 提取数据
    info = data.get("personal_info", {})
    educations = data.get("educations", [])
    experiences = data.get("experiences", [])
    skills = data.get("skills", [])

    # 生成教育经历 HTML 片段
    edu_html = ""
    for edu in educations:
        edu_html += f"""
        <div class="item">
            <div class="item-header">
                <span class="item-title">{edu.get('school')} - {edu.get('major')}</span>
                <span class="item-time">{edu.get('time')}</span>
            </div>
            <p>{edu.get('note')}</p>
        </div>
        """

    # 生成项目经历 HTML 片段
    exp_html = ""
    for exp in experiences:
        exp_html += f"""
        <div class="item">
            <div class="item-header">
                <span class="item-title">{exp.get('title')} ({exp.get('role')})</span>
                <span class="item-time">{exp.get('time')}</span>
            </div>
            <p>{exp.get('desc')}</p>
        </div>
        """

    # 拼接完整的 HTML（内嵌 CSS 控制排版）
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: "Microsoft YaHei", sans-serif; color: #333; line-height: 1.6; margin: 40px; }}
            .header {{ text-align: center; border-bottom: 2px solid #2c3e50; padding-bottom: 20px; margin-bottom: 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; color: #2c3e50; }}
            .header p {{ margin: 5px 0 0 0; font-size: 14px; color: #666; }}
            .section-title {{ font-size: 18px; color: #2c3e50; border-left: 4px solid #3498db; padding-left: 10px; margin-top: 30px; }}
            .item {{ margin-bottom: 15px; }}
            .item-header {{ display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 5px; }}
            .item-time {{ color: #7f8c8d; font-weight: normal; font-size: 14px; float: right; }} /* 为了兼容更简单的 PDF 渲染引擎使用 float */
            .item-title {{ display: inline-block; }}
            .skills {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{info.get('name', '姓名未填写')}</h1>
            <p>意向：{info.get('intent', '未填写')} | 联系方式：{info.get('contact', '未填写')}</p>
        </div>

        <h2 class="section-title">教育经历</h2>
        {edu_html}

        <h2 class="section-title">项目/实习经历</h2>
        {exp_html}

        <h2 class="section-title">专业技能</h2>
        <div class="skills">
            {", ".join(skills)}
        </div>
    </body>
    </html>
    """
    return html_template