from backend.database import save_user_profile, load_user_profile

from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QLabel
)
from ui.state import AppState


class ResetPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("重置密码（示例）")
        self.resize(420, 160)

        self.p1 = QLineEdit()
        self.p1.setEchoMode(QLineEdit.Password)
        self.p2 = QLineEdit()
        self.p2.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("新密码：", self.p1)
        form.addRow("确认密码：", self.p2)

        self.ok_btn = QPushButton("确认")
        self.cancel_btn = QPushButton("取消")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.ok_btn)
        btns.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("说明：这里只做UI演示，不做真实密码保存。"))
        layout.addLayout(form)
        layout.addLayout(btns)
        self.setLayout(layout)

    def get_passwords(self):
        return self.p1.text(), self.p2.text()


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
        self.btn_reset_pwd = QPushButton("重置密码")

        self.btn_edit.clicked.connect(self.on_edit)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.on_cancel)
        self.btn_reset_pwd.clicked.connect(self.on_reset_pwd)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_edit)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_reset_pwd)

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

    def on_reset_pwd(self):
        dlg = ResetPasswordDialog()
        if dlg.exec_() == QDialog.Accepted:
            p1, p2 = dlg.get_passwords()
            if not p1 or not p2:
                QMessageBox.warning(self, "提示", "密码不能为空。")
                return
            if p1 != p2:
                QMessageBox.warning(self, "提示", "两次输入不一致。")
                return
            QMessageBox.information(self, "完成", "密码重置UI演示完成（未落库）。")
