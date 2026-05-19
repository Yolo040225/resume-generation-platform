from backend.database import save_user_profile, load_user_profile

from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QLabel
)
from ui.state import AppState

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

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

        # 1. 隐藏文本框（用于存路径）
        self.photo = QLineEdit()
        self.photo.setVisible(False)

        # 2. 创建照片预览区域
        self.photo_preview = QLabel("暂无照片")
        self.photo_preview.setFixedSize(100, 140)
        self.photo_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")
        self.photo_preview.setScaledContents(True)

        # 3. 创建上传按钮
        self.btn_upload = QPushButton("上传照片")
        self.btn_upload.clicked.connect(self.on_upload_photo)

        # 让按钮在垂直方向上稍微靠上对齐，看起来更协调
        btn_v_layout = QVBoxLayout()
        btn_v_layout.addStretch()
        btn_v_layout.addWidget(self.btn_upload)
        btn_v_layout.addStretch()

        # 将预览框和按钮水平组合在一起
        photo_h_layout = QHBoxLayout()
        photo_h_layout.addWidget(self.photo_preview)
        photo_h_layout.addLayout(btn_v_layout)
        photo_h_layout.addStretch()  # 让多余的空间留在右侧，防止图片被拉伸变形

        # 作为新的一行，顺延加在"联系方式"下面
        form.addRow("免冠照：", photo_h_layout)

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

        photo_path = p.get("photo", "")
        self.photo.setText(photo_path)
        if photo_path:
            self.photo_preview.setPixmap(QPixmap(photo_path))

    def set_editing(self, editing: bool):
        self.is_editing = editing
        for w in [self.username, self.user_id, self.gender, self.contact]:
            w.setEnabled(editing)

        self.btn_save.setVisible(editing)
        self.btn_cancel.setVisible(editing)
        self.btn_edit.setVisible(not editing)
        self.btn_upload.setVisible(editing)

    def on_edit(self):
        self._snapshot = dict(self.state.profile)
        self.set_editing(True)

    def on_save(self):
        try:
            # 尝试获取界面数据
            self.state.profile["username"] = self.username.text().strip()
            self.state.profile["user_id"] = self.user_id.text().strip()
            self.state.profile["gender"] = self.gender.text().strip()
            self.state.profile["contact"] = self.contact.text().strip()

            # 看看是不是这里找不到 self.photo 属性
            self.state.profile["photo"] = self.photo.text().strip()

            # 调用数据库保存
            save_user_profile(self.state.profile)

            QMessageBox.information(self, "保存成功", "个人信息已保存到数据库。")
            self.set_editing(False)

        except Exception as e:
            # 如果中间任何一行报错，拦截下来，打印出具体是哪一行错在哪里，并弹出提示框而不闪退
            import traceback
            error_details = traceback.format_exc()
            print("\n" + "=" * 50 + "\n【保存功能报错详情】\n" + error_details + "=" * 50 + "\n")
            QMessageBox.critical(self, "保存失败", f"程序内部发生错误，原因：\n{str(e)}")

    def on_cancel(self):
        self.state.profile = dict(self._snapshot)
        self.load_from_state()
        self.set_editing(False)

    def on_upload_photo(self):
        # 弹出文件选择框，只允许选择图片格式
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择免冠照", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            # 记录路径并在预览框中显示图片
            self.photo.setText(file_path)
            self.photo_preview.setPixmap(QPixmap(file_path))