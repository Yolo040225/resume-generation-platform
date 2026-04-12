from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QStackedWidget, QHBoxLayout
from ui.state import AppState

from ui.user_profile_page import UserProfilePage
from ui.resume_manage_page import ResumeManagePage
from ui.job_manage_page import JobManagePage
from ui.resume_generate_page import ResumeGeneratePage
from ui.version_manage_page import VersionManagePage



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("个性化简历生成平台")
        self.resize(1100, 700)

        self.state = AppState()

        self.nav = QListWidget()
        self.nav.addItems([
            "个人信息管理",
            "简历管理",
            "岗位定制",
            "简历生成与预览",
            "简历版本管理"
        ])

        self.stack = QStackedWidget()
        self.page_profile = UserProfilePage(self.state)
        self.page_resume = ResumeManagePage(self.state)
        self.page_job = JobManagePage(self.state)
        self.page_generate = ResumeGeneratePage(self.state)
        self.page_versions = VersionManagePage(self.state)


        self.stack.addWidget(self.page_profile)
        self.stack.addWidget(self.page_resume)
        self.stack.addWidget(self.page_job)
        self.stack.addWidget(self.page_generate)
        self.stack.addWidget(self.page_versions)

        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.nav, 2)
        layout.addWidget(self.stack, 8)
        self.setCentralWidget(container)
