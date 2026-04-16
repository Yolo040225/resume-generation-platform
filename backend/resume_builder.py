def build_resume_text(state):
    lines = []

    if state.profile:
        lines.append("【基本信息】")
        name = state.profile.get("username", "")
        contact = state.profile.get("contact", "")

        if name:
            lines.append(f"姓名: {name}")
        if contact:
            lines.append(f"联系方式: {contact}")
        lines.append("")  # 加一个空行分隔

    if state.educations:
        lines.append("【教育经历】")
        for e in state.educations:
            line = f"{e.get('time','')} {e.get('school','')} {e.get('major','')}"
            if e.get("note"):
                line += f"\n  - {e.get('note')}"
            lines.append(line)

    if state.experiences:
        lines.append("\n【项目/实习经历】")
        for x in state.experiences:
            line = f"{x.get('time','')} {x.get('title','')}（{x.get('role','')}）"
            if x.get("desc"):
                line += f"\n  - {x.get('desc')}"
            lines.append(line)

    if state.skills:
        lines.append("\n【技能】")
        lines.append(", ".join(state.skills))

    return "\n".join(lines)

