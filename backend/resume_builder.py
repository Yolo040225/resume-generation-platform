def build_resume_text(state):
    lines = []

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

