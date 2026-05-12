import json
import re


def generate_html_from_json(json_str: str) -> str:
    try:
        # 容错提取：使用正则精准抓取大括号及内部的所有内容
        match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if not match:
            raise ValueError("未找到有效的 JSON 结构")

        clean_json = match.group(0)
        data = json.loads(clean_json)

    except (json.JSONDecodeError, ValueError) as e:
        return f"""
        <div style="font-family: 'Microsoft YaHei'; padding: 40px; color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px;">
            <h2 style="margin-top: 0;">⚠️ AI 简历生成格式异常</h2>
            <p>大语言模型返回的数据格式不符合规范，无法渲染。请重新点击生成。</p>
            <p><strong>错误信息：</strong> {str(e)}</p>
        </div>
        """

    # 提取数据
    info = data.get("personal_info", {})
    educations = data.get("educations", [])
    experiences = data.get("experiences", [])
    skills = data.get("skills", [])

    # ==========================================
    # 核心优化 1：生成教育经历 HTML (使用 Table 布局，保证绝对对齐)
    # ==========================================
    edu_html = ""
    for edu in educations:
        edu_html += f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 5px;">
            <tr>
                <td align="left" style="font-weight: bold; font-size: 15px; color: #333;">{edu.get('school')}</td>
                <td align="right" style="color: #666; font-size: 14px;">{edu.get('time')}</td>
            </tr>
            <tr>
                <td align="left" style="font-style: italic; color: #555; padding-top: 3px;">{edu.get('major')}</td>
                <td align="right"></td>
            </tr>
        </table>
        <div style="color: #444; font-size: 14px; margin-bottom: 15px; line-height: 1.5;">{edu.get('note')}</div>
        """

    # ==========================================
    # 核心优化 2：生成项目经历 HTML (使用 Table 布局)
    # ==========================================
    exp_html = ""
    for exp in experiences:
        exp_html += f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 5px; margin-top: 10px;">
            <tr>
                <td align="left" style="font-weight: bold; font-size: 15px; color: #333;">{exp.get('title')} &nbsp;|&nbsp; <span style="font-weight: normal; color: #666;">{exp.get('role')}</span></td>
                <td align="right" style="color: #666; font-size: 14px;">{exp.get('time')}</td>
            </tr>
        </table>
        <div style="color: #444; font-size: 14px; margin-bottom: 15px; line-height: 1.6;">{exp.get('desc')}</div>
        """

    # ==========================================
    # 核心优化 3：拼接完整的 HTML（专为 QTextDocument 优化的安全 CSS）
    # ==========================================
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: "Microsoft YaHei", "SimHei", sans-serif; padding: 20px 30px; background-color: #ffffff; }}
            .resume-header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #2C3E50; padding-bottom: 15px; }}
            .name {{ font-size: 24pt; font-weight: bold; color: #2C3E50; margin: 0 0 10px 0; letter-spacing: 2px; }}
            .contact {{ font-size: 10.5pt; color: #555; margin: 0; }}
            .section-title {{ font-size: 14pt; font-weight: bold; color: #2C3E50; background-color: #ECF0F1; padding: 6px 12px; margin-top: 25px; margin-bottom: 15px; border-left: 4px solid #3498DB; }}
            .skills-box {{ font-size: 10pt; color: #444; line-height: 1.8; }}
        </style>
    </head>
    <body>
        <div class="resume-header">
            <h1 class="name">{info.get('name', '未提供')}</h1>
            <p class="contact">意向岗位：{info.get('intent', '未提供')} &nbsp;|&nbsp; 联系方式：{info.get('contact', '未提供')}</p>
        </div>

        <div class="section-title">教育背景</div>
        {edu_html}

        <div class="section-title">核心经历</div>
        {exp_html}

        <div class="section-title">专业技能</div>
        <div class="skills-box">
            {", ".join(skills)}
        </div>
    </body>
    </html>
    """
    return html_template