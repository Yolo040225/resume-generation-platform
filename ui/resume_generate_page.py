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
from PyQt5.QtCore import QThread, pyqtSignal

class ResumeGenerateWorker(QThread):
    # 定义两个信号：成功返回 JSON 文本，失败返回错误字符串
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, prompt, temperature=0.4):
        super().__init__()
        self.prompt = prompt
        self.temperature = temperature

    def run(self):
        try:
            # 在子线程中执行耗时的 API 调用
            from backend.llm_service import call_deepseek_chat
            result_json = call_deepseek_chat(self.prompt, temperature=self.temperature)
            self.finished_signal.emit(result_json)
        except Exception as e:
            self.error_signal.emit(str(e))
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

    def generate_resume(self):
        if not self.state.jobs:
            QMessageBox.information(self, "提示", "请先保存至少一个岗位。")
            return

        # 1. 准备数据（这些是本地内存操作，非常快，留在主线程）
        idx = self.job_select.currentIndex()
        job = self.state.jobs[idx]

        # 构建结构化简历文本并同步显示到左侧预览
        resume_text = build_resume_text(self.state)
        self.original_resume.setPlainText(resume_text)

        # 读取岗位画像并构建 Prompt
        job_profile = load_job_profile(job["id"])
        prompt = build_prompt(resume_text, job_profile, job['title'], job["jd"])

        # 2. UI 状态切换（禁用按钮，显示等待文字）
        self.btn_generate.setEnabled(False)
        self.btn_generate.setText("正在生成，请稍候...")
        self.optimized_resume.setPlainText("正在调用大模型进行简历深度重塑，此过程预计耗时 5-15 秒，主界面可正常拖动...")

        # 3. 启动真实的异步线程
        self.worker = ResumeGenerateWorker(prompt, temperature=0.4)
        self.worker.finished_signal.connect(self.on_generate_success)
        self.worker.error_signal.connect(self.on_generate_error)
        self.worker.start()

    # 4. 成功回调：渲染 HTML
    def on_generate_success(self, result_json):
        try:
            self.current_result_json = result_json  # 保存供“保存版本”功能使用

            from backend.html_generator import generate_html_from_json
            preview_html = generate_html_from_json(result_json)

            self.optimized_resume.setHtml(preview_html)  # 渲染富文本
            QMessageBox.information(self, "生成成功", "简历已根据目标岗位完成定制化重塑！")
        except Exception as e:
            self.on_generate_error(f"解析渲染失败: {str(e)}")
        finally:
            self.btn_generate.setEnabled(True)
            self.btn_generate.setText("生成 / 优化简历")

    # 5. 失败回调：提示用户
    def on_generate_error(self, err_msg):
        QMessageBox.critical(self, "生成失败", f"大模型服务异常: {err_msg}")
        self.optimized_resume.setPlainText(f"生成失败，错误信息：\n{err_msg}")
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
