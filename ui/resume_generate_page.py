from backend.database import load_job_profile
from backend.resume_builder import build_resume_text
from backend.prompt_builder import build_prompt
from backend.llm_service import call_deepseek_chat
from backend.database import add_resume_version
from backend.database import load_jobs
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QTextEdit, QMessageBox, QApplication
)
from ui.state import AppState
from datetime import datetime

class ResumeGeneratePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        param_group = QGroupBox("生成参数")
        param_layout = QVBoxLayout()

        self.job_select = QComboBox()

        self.btn_refresh_jobs = QPushButton("刷新岗位列表")
        self.btn_generate = QPushButton("生成 / 优化简历")
        self.btn_save_version = QPushButton("保存为一个版本")

        self.btn_refresh_jobs.clicked.connect(self.refresh_jobs)
        self.btn_generate.clicked.connect(self.generate_resume)
        self.btn_save_version.clicked.connect(self.save_version)

        param_layout.addWidget(QLabel("目标岗位："))
        param_layout.addWidget(self.job_select)
        param_layout.addWidget(self.btn_refresh_jobs)
        param_layout.addWidget(self.btn_generate)
        param_layout.addWidget(self.btn_save_version)
        param_layout.addStretch()

        param_group.setLayout(param_layout)

        preview_group = QGroupBox("简历生成结果对比")

        self.original_resume = QTextEdit()
        self.original_resume.setReadOnly(True)
        self.original_resume.setPlaceholderText("这里显示原始简历（未优化）")
        self.original_resume.setStyleSheet("background-color:#f5f5f5;")

        self.optimized_resume = QTextEdit()
        self.optimized_resume.setPlaceholderText(
            "点击“生成/优化简历”后，这里会显示AI生成的简历内容。"
        )

        preview_layout = QHBoxLayout()

        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("原始简历"))
        left_box.addWidget(self.original_resume)

        right_box = QVBoxLayout()
        right_box.addWidget(QLabel("优化后简历（可编辑）"))
        right_box.addWidget(self.optimized_resume)

        preview_layout.addLayout(left_box)
        preview_layout.addLayout(right_box)

        preview_layout.setStretch(0, 3)
        preview_layout.setStretch(1, 7)

        preview_group.setLayout(preview_layout)

        layout = QHBoxLayout()

        # 1. 强制设定左侧参数区的宽度（200像素通常比较合适，你也可以根据喜好改成250或180）
        param_group.setFixedWidth(200)

        # 2. 将参数区加入布局，不要加比例参数
        layout.addWidget(param_group)

        # 3. 将预览区加入布局，并给它加上拉伸因子 1，这样它就会自动霸占所有剩下的屏幕空间
        layout.addWidget(preview_group, 1)

        self.setLayout(layout)

        self.refresh_jobs()

    def refresh_jobs(self):
        self.job_select.clear()

        # 从数据库读取岗位
        self.state.jobs = load_jobs()

        if not self.state.jobs:
            self.job_select.addItem("暂无岗位（请先去“岗位定制”保存）")
            self.job_select.setEnabled(False)
        else:
            self.job_select.setEnabled(True)
            for j in self.state.jobs:
                self.job_select.addItem(f"{j['company']} - {j['title']}")

    def generate_resume(self):  # 名字暂时不改，保持按钮连接不动
        if not self.state.jobs:
            QMessageBox.information(self, "提示", "请先保存至少一个岗位。")
            return

        self.btn_generate.setEnabled(False)
        self.btn_generate.setText("正在生成，请稍候...")
        self.optimized_resume.setPlainText("正在调用大模型生成简历，请稍候...")
        QApplication.processEvents()
        idx = self.job_select.currentIndex()
        job = self.state.jobs[idx]

        # 1️⃣ 构建结构化简历文本
        resume_text = build_resume_text(self.state)
        self.original_resume.setPlainText(resume_text)

        # 2️⃣ 读取岗位画像（如果你已有 profile 表，可改成数据库读取）
        job_profile = load_job_profile(job["id"])

        # 3️⃣ 构建 Prompt
        prompt = build_prompt(resume_text, job_profile, job['title'], job["jd"])
        print("\n===== PROMPT START =====")
        print(prompt)
        print("===== PROMPT END =====\n")
        try:
            # 4️⃣ 调用 DeepSeek
            result_json = call_deepseek_chat(prompt, temperature=0.4)

            # 将原始 JSON 存入实例变量，供后续保存版本时使用
            self.current_result_json = result_json

            # 5️⃣ 转换为 HTML 并显示结果
            from backend.html_generator import generate_html_from_json
            preview_html = generate_html_from_json(result_json)

            # 使用 setHtml 而不是 setPlainText 渲染富文本
            self.optimized_resume.setHtml(preview_html)
            QMessageBox.information(self, "生成成功", "简历已生成完毕！")

        except Exception as e:
            QMessageBox.critical(self, "生成失败", str(e))
        self.btn_generate.setEnabled(True)
        self.btn_generate.setText("生成 / 优化简历")

    def save_version(self):
        # 获取刚刚生成并保存在实例中的 JSON 字符串
        content = getattr(self, "current_result_json", "").strip()

        if not content:
            QMessageBox.warning(self, "提示", "请先生成简历后再保存版本。")
            return

        job_label = self.job_select.currentText()
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_resume_version({
            "job_label": job_label,
            "template": save_time,
            "content": content  # 这里完美存入了 JSON
        })

        QMessageBox.information(self, "保存成功", "简历版本已保存到数据库。")
