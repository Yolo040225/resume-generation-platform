import os
from PyQt5.QtWidgets import QFileDialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyQt5.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from backend.database import load_resume_versions, delete_resume_version
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QListWidget,
    QTextEdit, QPushButton, QMessageBox, QLabel
)
from ui.state import AppState
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from backend.html_generator import generate_html_from_json

class VersionManagePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        left_group = QGroupBox("版本列表")
        self.list = QListWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list)
        left_group.setLayout(left_layout)

        right_group = QGroupBox("版本预览（只读）")
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.preview)
        right_group.setLayout(right_layout)

        self.btn_refresh = QPushButton("刷新列表")
        self.btn_delete = QPushButton("删除版本")
        self.btn_export = QPushButton("导出PDF（入口）")

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.delete_version)
        self.btn_export.clicked.connect(self.export_pdf_stub)

        self.list.currentRowChanged.connect(self.show_preview)

        btns = QHBoxLayout()
        btns.addWidget(self.btn_refresh)
        btns.addWidget(self.btn_delete)
        btns.addStretch()
        btns.addWidget(self.btn_export)

        hint = QLabel("提示：先在“简历生成与预览”里保存版本，再到这里查看/导出。")

        layout = QVBoxLayout()
        top = QHBoxLayout()
        top.addWidget(left_group, 3)
        top.addWidget(right_group, 7)
        layout.addLayout(top)
        layout.addWidget(hint)
        layout.addLayout(btns)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        self.list.clear()
        self.state.versions = load_resume_versions()
        for v in self.state.versions:
            self.list.addItem(f"{v['job_label']} | {v['template']}")
        self.preview.clear()

    def show_preview(self, idx: int):
        if idx < 0 or idx >= len(self.state.versions):
            self.preview.clear()
            return

        # 1. 获取数据库里的 JSON 字符串内容
        json_content = self.state.versions[idx]["content"]

        try:
            # 2. 调用我们强大的 HTML 生成器，将 JSON 转为精美的 HTML
            html_preview = generate_html_from_json(json_content)

            # 3. 使用 setHtml 而不是 setPlainText，让 QTextEdit 渲染富文本样式
            self.preview.setHtml(html_preview)

        except Exception as e:
            # 如果解析出错，显示一个友好的错误提示
            self.preview.setPlainText(f"预览生成失败：{str(e)}\n原始数据：\n{json_content}")

    def delete_version(self):
        idx = self.list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一个版本。")
            return

        version = self.state.versions[idx]
        delete_resume_version(version["id"])

        QMessageBox.information(self, "完成", "已删除该简历版本。")
        self.refresh()

    def export_pdf_stub(self):
        idx = self.list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一个版本。")
            return

        version = self.state.versions[idx]
        json_content = version["content"]  # 这里现在存的是大模型返回的 JSON 字符串

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存为PDF",
            "resume.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            # 1. JSON 转换成 HTML
            html_content = generate_html_from_json(json_content)

            # 2. 使用 PyQt5 的 QTextDocument 渲染 HTML
            doc = QTextDocument()
            doc.setHtml(html_content)

            # 3. 设置 PDF 打印机参数
            printer = QPrinter(QPrinter.ScreenResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)

            # 设置 A4 纸张大小和页边距
            printer.setPageSize(QPrinter.A4)
            printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter)

            # 4. 导出！
            doc.print_(printer)

            QMessageBox.information(self, "成功", "精美 HTML 排版的 PDF 导出成功！")

        except Exception as e:
            QMessageBox.warning(self, "失败", f"导出失败：{str(e)}")
