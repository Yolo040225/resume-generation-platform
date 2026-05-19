from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AppState:
    # 个人信息（账户信息）
    profile: Dict[str, str] = field(default_factory=lambda: {
        "username": "",
        "user_id": "",
        "gender": "",
        "contact": "",
        "photo": ""
    })

    # 简历结构化信息
    educations: List[Dict[str, str]] = field(default_factory=list)
    experiences: List[Dict[str, str]] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)

    # 岗位信息
    jobs: List[Dict[str, str]] = field(default_factory=list)  # {company, title, jd}

    # 生成版本
    versions: List[Dict[str, Any]] = field(default_factory=list)  # {job_label, template, content}
