from backend.job_parser import parse_job
from backend.database import add_job, load_jobs, save_job_profile
from backend.database import add_job, load_jobs, delete_job
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from ui.state import AppState
from PyQt5.QtCore import QThread, pyqtSignal


class JobParserWorker(QThread):
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, jd_text):
        super().__init__()
        self.jd_text = jd_text

    def run(self):
        try:
            profile = parse_job(self.jd_text)
            self.finished_signal.emit(profile)
        except Exception as e:
            self.error_signal.emit(str(e))
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

        self.save_btn = QPushButton("保存岗位（后台自动解析）")
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

        self.save_btn.setEnabled(False)
        self.save_btn.setText("大模型正在深度解析中，请稍候...")
        self.profile_display.setText("正在调用 DeepSeek 进行 JD 特征抽取...")

        try:
            # 先保存原始岗位到数据库
            add_job({"company": company, "title": title, "jd": jd})
            jobs = load_jobs()
            self.current_job_id = jobs[-1]["id"]  # 存入实例变量供子线程回调使用

            # 启动真实的异步线程
            self.worker = JobParserWorker(jd)
            self.worker.finished_signal.connect(self.on_parse_success)
            self.worker.error_signal.connect(self.on_parse_error)
            self.worker.start()

        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"保存岗位发生错误: {str(e)}")
            self.save_btn.setEnabled(True)
            self.save_btn.setText("保存岗位（后台自动解析）")

    # 成功的回调函数
    def on_parse_success(self, profile):
        save_job_profile(self.current_job_id, profile)
        display_text = (
            "【大模型解析结果】\n"
            f"岗位类型：{profile.get('job_category', '')}\n"
            f"核心技能：{', '.join(profile.get('skills', [])) or '无'}\n"
            f"学历要求：{profile.get('education_level', '')}\n"
            f"经验要求：{profile.get('experience_years', '')}"
        )
        self.profile_display.setText(display_text)
        QMessageBox.information(self, "保存成功", "岗位已保存并由大模型完成解析！")
        self.company.clear()
        self.title.clear()
        self.jd.clear()

        self.save_btn.setEnabled(True)
        self.save_btn.setText("保存岗位（后台自动解析）")

    # 失败的回调函数
    def on_parse_error(self, err_msg):
        QMessageBox.critical(self, "解析错误", f"大模型解析失败: {err_msg}")
        self.profile_display.setText("解析失败，请检查网络或大模型 API Key。")
        self.save_btn.setEnabled(True)
        self.save_btn.setText("保存岗位（后台自动解析）")



