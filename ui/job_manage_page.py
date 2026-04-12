from backend.job_parser import parse_job
from backend.database import add_job, load_jobs, save_job_profile
from backend.database import add_job, load_jobs, delete_job
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from ui.state import AppState


class JobManagePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        basic_group = QGroupBox("岗位基本信息")
        form = QFormLayout()
        self.company = QLineEdit()
        self.title = QLineEdit()
        form.addRow("公司名称：", self.company)
        form.addRow("岗位名称：", self.title)
        basic_group.setLayout(form)

        jd_group = QGroupBox("岗位描述（JD）")
        self.jd = QTextEdit()
        self.jd.setPlaceholderText("粘贴岗位JD文本...")
        jd_layout = QVBoxLayout()
        jd_layout.addWidget(self.jd)
        jd_group.setLayout(jd_layout)

        self.save_btn = QPushButton("保存岗位（后台自动解析：此处仅UI演示）")
        self.save_btn.clicked.connect(self.save_job)

        layout = QVBoxLayout()
        layout.addWidget(basic_group)
        layout.addWidget(jd_group)
        layout.addWidget(self.save_btn)

        # ===== 新增：岗位解析结果展示区 =====
        profile_group = QGroupBox("岗位解析结果")
        self.profile_display = QTextEdit()
        self.profile_display.setReadOnly(True)
        self.profile_display.setPlaceholderText("岗位解析结果将在此显示")

        profile_layout = QVBoxLayout()
        profile_layout.addWidget(self.profile_display)
        profile_group.setLayout(profile_layout)

        layout.addWidget(profile_group)

        layout.addStretch()
        self.setLayout(layout)

    def save_job(self):
        company = self.company.text().strip()
        title = self.title.text().strip()
        jd = self.jd.toPlainText().strip()

        if not company or not title or not jd:
            QMessageBox.warning(self, "提示", "公司名称、岗位名称、JD 不能为空。")
            return

        # 1️⃣ 保存原始岗位
        add_job({
            "company": company,
            "title": title,
            "jd": jd
        })

        # 2️⃣ 读取刚保存的岗位（取最后一个）
        jobs = load_jobs()
        job_id = jobs[-1]["id"]

        # 3️⃣ 岗位解析
        profile = parse_job(jd)

        # 4️⃣ 保存岗位画像
        save_job_profile(job_id, profile)

        # ===== 新增：将解析结果写入展示区 =====
        display_text = (
            "【岗位解析结果】\n"
            f"岗位类型：{profile.get('job_category', '')}\n"
            f"核心技能：{', '.join(profile.get('skills', [])) or '无'}\n"
            f"学历要求：{profile.get('education_level', '')}\n"
            f"经验要求：{profile.get('experience_years', '')}"
        )
        self.profile_display.setText(display_text)

        # （可保留）弹窗提示
        QMessageBox.information(
            self,
            "保存成功",
            "岗位已保存并完成解析，解析结果已在页面下方展示。"
        )

        self.company.clear()
        self.title.clear()
        self.jd.clear()



