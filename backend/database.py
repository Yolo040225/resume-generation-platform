import sqlite3
from pathlib import Path

# 数据库文件路径
DB_PATH = Path(__file__).parent.parent / "app.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    """初始化数据库与表结构"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        user_id TEXT,
        gender TEXT,
        contact TEXT,
        photo TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school TEXT,
        major TEXT,
        time TEXT,
        note TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        role TEXT,
        time TEXT,
        desc TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        title TEXT,
        jd TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        skills TEXT,
        education_level TEXT,
        experience_years TEXT,
        job_category TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resume_version (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_label TEXT,
        template TEXT,
        content TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_skill(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_user_profile(profile: dict):
    """保存用户个人信息（只保留一条，重复则更新）"""
    conn = get_connection()
    cur = conn.cursor()
    # 先清空，再插入（简单稳妥）
    cur.execute("DELETE FROM user_profile")
    cur.execute("""
        INSERT INTO user_profile (username, user_id, gender, contact, photo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        profile.get("username", ""),
        profile.get("user_id", ""),
        profile.get("gender", ""),
        profile.get("contact", ""),
        profile.get("photo", "")
    ))

    conn.commit()
    conn.close()


def load_user_profile() -> dict:
    """读取用户个人信息"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, user_id, gender, contact, photo
        FROM user_profile
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "username": row[0],
        "user_id": row[1],
        "gender": row[2],
        "contact": row[3],
        "photo": row[4] if len(row) > 4 else ""
    }
def add_education(edu: dict):
    """新增一条教育经历"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO education (school, major, time, note)
        VALUES (?, ?, ?, ?)
    """, (
        edu.get("school", ""),
        edu.get("major", ""),
        edu.get("time", ""),
        edu.get("note", "")
    ))

    conn.commit()
    conn.close()


def load_educations():
    """读取所有教育经历"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, school, major, time, note
        FROM education
        ORDER BY id ASC
    """)
    rows = cur.fetchall()
    conn.close()

    educations = []
    for r in rows:
        educations.append({
            "id": r[0],
            "school": r[1],
            "major": r[2],
            "time": r[3],
            "note": r[4],
        })
    return educations


def delete_education(edu_id: int):
    """删除一条教育经历"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM education WHERE id = ?", (edu_id,))
    conn.commit()
    conn.close()
def add_experience(exp: dict):
    """新增一条项目/实习经历"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO experience (title, role, time, desc)
        VALUES (?, ?, ?, ?)
    """, (
        exp.get("title", ""),
        exp.get("role", ""),
        exp.get("time", ""),
        exp.get("desc", "")
    ))

    conn.commit()
    conn.close()


def load_experiences():
    """读取所有项目/实习经历"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, role, time, desc
        FROM experience
        ORDER BY id ASC
    """)
    rows = cur.fetchall()
    conn.close()

    exps = []
    for r in rows:
        exps.append({
            "id": r[0],
            "title": r[1],
            "role": r[2],
            "time": r[3],
            "desc": r[4],
        })
    return exps


def delete_experience(exp_id: int):
    """删除一条项目/实习经历"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM experience WHERE id = ?", (exp_id,))
    conn.commit()
    conn.close()
def add_job(job: dict):
    """新增岗位"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO job (company, title, jd)
        VALUES (?, ?, ?)
    """, (
        job.get("company", ""),
        job.get("title", ""),
        job.get("jd", "")
    ))

    conn.commit()
    conn.close()


def load_jobs():
    """读取所有岗位"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, company, title, jd
        FROM job
        ORDER BY id ASC
    """)
    rows = cur.fetchall()
    conn.close()

    jobs = []
    for r in rows:
        jobs.append({
            "id": r[0],
            "company": r[1],
            "title": r[2],
            "jd": r[3],
        })
    return jobs


def delete_job(job_id: int):
    """删除岗位"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM job WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
def add_resume_version(version: dict):
    """保存一条简历生成版本"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resume_version (job_label, template, content)
        VALUES (?, ?, ?)
    """, (
        version.get("job_label", ""),
        version.get("template", ""),
        version.get("content", "")
    ))

    conn.commit()
    conn.close()


def load_resume_versions():
    """读取所有简历版本"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, job_label, template, content
        FROM resume_version
        ORDER BY id ASC
    """)
    rows = cur.fetchall()
    conn.close()

    versions = []
    for r in rows:
        versions.append({
            "id": r[0],
            "job_label": r[1],
            "template": r[2],
            "content": r[3],
        })
    return versions


def delete_resume_version(version_id: int):
    """删除简历版本"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM resume_version WHERE id = ?", (version_id,))
    conn.commit()
    conn.close()
def save_job_profile(job_id: int, profile: dict):
    """保存岗位解析结果"""
    conn = get_connection()
    cur = conn.cursor()

    # 先删旧的
    cur.execute("DELETE FROM job_profile WHERE job_id = ?", (job_id,))

    cur.execute("""
        INSERT INTO job_profile (
            job_id, skills, education_level, experience_years, job_category
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        job_id,
        ", ".join(profile.get("skills", [])),
        profile.get("education_level", ""),
        profile.get("experience_years", ""),
        profile.get("job_category", "")
    ))

    conn.commit()
    conn.close()

def load_job_profile(job_id: int):
    """读取岗位解析结果"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT skills, education_level, experience_years, job_category
        FROM job_profile
        WHERE job_id = ?
    """, (job_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "skills": row[0].split(", ") if row[0] else [],
        "education_level": row[1],
        "experience_years": row[2],
        "job_category": row[3]
    }


def save_skills(skills: list):
    """保存全部技能（先清空后全量插入）"""
    conn = get_connection()
    cur = conn.cursor()

    # 先清空旧的技能记录
    cur.execute("DELETE FROM user_skill")

    # 逐条插入新技能
    for skill in skills:
        cur.execute("INSERT INTO user_skill (skill_name) VALUES (?)", (skill,))

    conn.commit()
    conn.close()


def load_skills() -> list:
    """读取所有技能"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT skill_name FROM user_skill ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    # 将查询结果按列表形式返回
    return [r[0] for r in rows]