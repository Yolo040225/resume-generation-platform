from backend.database import save_user_profile, load_user_profile

from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QLabel
)
from ui.state import AppState

class UserProfilePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.is_editing = False
        self._snapshot = dict(self.state.profile)

        group = QGroupBox("账户信息")
        form = QFormLayout()

        self.username = QLineEdit()
        self.user_id = QLineEdit()
        self.gender = QLineEdit()
        self.contact = QLineEdit()

        form.addRow("用户名：", self.username)
        form.addRow("用户ID：", self.user_id)
        form.addRow("性别：", self.gender)
        form.addRow("联系方式：", self.contact)
        group.setLayout(form)

        # buttons
        self.btn_edit = QPushButton("修改个人信息")
        self.btn_save = QPushButton("保存")
        self.btn_cancel = QPushButton("取消")

        self.btn_edit.clicked.connect(self.on_edit)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.on_cancel)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_edit)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(group)
        layout.addLayout(btn_row)
        layout.addStretch()
        self.setLayout(layout)

        # 从数据库加载个人信息
        db_profile = load_user_profile()
        if db_profile:
            self.state.profile.update(db_profile)
        self.load_from_state()

        self.set_editing(False)

    def load_from_state(self):
        p = self.state.profile
        self.username.setText(p.get("username", ""))
        self.user_id.setText(p.get("user_id", ""))
        self.gender.setText(p.get("gender", ""))
        self.contact.setText(p.get("contact", ""))

    def set_editing(self, editing: bool):
        self.is_editing = editing
        for w in [self.username, self.user_id, self.gender, self.contact]:
            w.setEnabled(editing)

        self.btn_save.setVisible(editing)
        self.btn_cancel.setVisible(editing)
        self.btn_edit.setVisible(not editing)

    def on_edit(self):
        self._snapshot = dict(self.state.profile)
        self.set_editing(True)

    def on_save(self):
        self.state.profile["username"] = self.username.text().strip()
        self.state.profile["user_id"] = self.user_id.text().strip()
        self.state.profile["gender"] = self.gender.text().strip()
        self.state.profile["contact"] = self.contact.text().strip()

        # 保存到数据库
        save_user_profile(self.state.profile)

        QMessageBox.information(self, "保存成功", "个人信息已保存到数据库。")
        self.set_editing(False)

    def on_cancel(self):
        self.state.profile = dict(self._snapshot)
        self.load_from_state()
        self.set_editing(False)