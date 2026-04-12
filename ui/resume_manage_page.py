from backend.database import add_education, load_educations, delete_education
from backend.database import (
    add_education, load_educations, delete_education,
    add_experience, load_experiences, delete_experience,
    save_skills, load_skills
)
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QMessageBox, QLabel
)
from ui.state import AppState


class EducationDialog(QDialog):
    def __init__(self, init=None):
        super().__init__()
        self.setWindowTitle("教育经历")
        self.resize(520, 260)

        self.school = QLineEdit()
        self.major = QLineEdit()
        self.time = QLineEdit()
        self.note = QTextEdit()

        form = QFormLayout()
        form.addRow("学校：", self.school)
        form.addRow("专业：", self.major)
        form.addRow("起止时间：", self.time)
        form.addRow("补充说明：", self.note)

        if init:
            self.school.setText(init.get("school", ""))
            self.major.setText(init.get("major", ""))
            self.time.setText(init.get("time", ""))
            self.note.setPlainText(init.get("note", ""))

        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.ok_btn)
        btns.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btns)
        self.setLayout(layout)

    def get_data(self):
        return {
            "school": self.school.text().strip(),
            "major": self.major.text().strip(),
            "time": self.time.text().strip(),
            "note": self.note.toPlainText().strip(),
        }


class ExperienceDialog(QDialog):
    def __init__(self, init=None):
        super().__init__()
        self.setWindowTitle("项目/实习经历")
        self.resize(520, 300)

        self.title = QLineEdit()
        self.role = QLineEdit()
        self.time = QLineEdit()
        self.desc = QTextEdit()

        form = QFormLayout()
        form.addRow("名称：", self.title)
        form.addRow("角色：", self.role)
        form.addRow("起止时间：", self.time)
        form.addRow("内容描述：", self.desc)

        if init:
            self.title.setText(init.get("title", ""))
            self.role.setText(init.get("role", ""))
            self.time.setText(init.get("time", ""))
            self.desc.setPlainText(init.get("desc", ""))

        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.ok_btn)
        btns.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btns)
        self.setLayout(layout)

    def get_data(self):
        return {
            "title": self.title.text().strip(),
            "role": self.role.text().strip(),
            "time": self.time.text().strip(),
            "desc": self.desc.toPlainText().strip(),
        }


class ResumeManagePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        # ===== 教育经历 =====
        edu_group = QGroupBox("教育经历")
        self.edu_list = QListWidget()
        edu_btn_add = QPushButton("添加")
        edu_btn_edit = QPushButton("编辑")
        edu_btn_del = QPushButton("删除")

        edu_btn_add.clicked.connect(self.add_edu)
        edu_btn_edit.clicked.connect(self.edit_edu)
        edu_btn_del.clicked.connect(self.del_edu)

        edu_btns = QHBoxLayout()
        edu_btns.addWidget(edu_btn_add)
        edu_btns.addWidget(edu_btn_edit)
        edu_btns.addWidget(edu_btn_del)
        edu_btns.addStretch()

        edu_layout = QVBoxLayout()
        edu_layout.addWidget(self.edu_list)
        edu_layout.addLayout(edu_btns)
        edu_group.setLayout(edu_layout)

        # ===== 项目/实习 =====
        exp_group = QGroupBox("项目 / 实习经历")
        self.exp_list = QListWidget()
        exp_btn_add = QPushButton("添加")
        exp_btn_edit = QPushButton("编辑")
        exp_btn_del = QPushButton("删除")

        exp_btn_add.clicked.connect(self.add_exp)
        exp_btn_edit.clicked.connect(self.edit_exp)
        exp_btn_del.clicked.connect(self.del_exp)

        exp_btns = QHBoxLayout()
        exp_btns.addWidget(exp_btn_add)
        exp_btns.addWidget(exp_btn_edit)
        exp_btns.addWidget(exp_btn_del)
        exp_btns.addStretch()

        exp_layout = QVBoxLayout()
        exp_layout.addWidget(self.exp_list)
        exp_layout.addLayout(exp_btns)
        exp_group.setLayout(exp_layout)

        # ===== 技能 =====
        skill_group = QGroupBox("技能信息（用逗号分隔）")
        self.skill_input = QLineEdit()
        self.skill_input.setPlaceholderText("例如：Python, Java, PyTorch, Linux")
        skill_save = QPushButton("保存技能")
        skill_save.clicked.connect(self.save_skills)

        skill_layout = QVBoxLayout()
        skill_layout.addWidget(QLabel("技能："))
        skill_layout.addWidget(self.skill_input)
        skill_layout.addWidget(skill_save)
        skill_group.setLayout(skill_layout)

        # ===== 布局 =====
        layout = QVBoxLayout()
        layout.addWidget(edu_group)
        layout.addWidget(exp_group)
        layout.addWidget(skill_group)
        layout.addStretch()
        self.setLayout(layout)

        # 从数据库加载教育经历
        self.state.educations = load_educations()
        self.state.experiences = load_experiences()
        self.state.skills = load_skills()
        self.refresh_lists()

    def refresh_lists(self):
        self.edu_list.clear()
        for e in self.state.educations:
            line = f"{e.get('time','')}  {e.get('school','')}  {e.get('major','')}"
            self.edu_list.addItem(line)

        self.exp_list.clear()
        for x in self.state.experiences:
            line = f"{x.get('time','')}  {x.get('title','')}（{x.get('role','')}）"
            self.exp_list.addItem(line)

        self.skill_input.setText(", ".join(self.state.skills))

    def add_edu(self):
        dlg = EducationDialog()
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            if not data["school"] or not data["time"]:
                QMessageBox.warning(self, "提示", "学校与起止时间不能为空。")
                return

            # 存数据库
            add_education(data)

            # 重新从数据库读
            self.state.educations = load_educations()
            self.refresh_lists()

    def edit_edu(self):
        idx = self.edu_list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一条教育经历。")
            return
        init = self.state.educations[idx]
        dlg = EducationDialog(init=init)
        if dlg.exec_() == QDialog.Accepted:
            self.state.educations[idx] = dlg.get_data()
            self.refresh_lists()

    def del_edu(self):
        idx = self.edu_list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一条教育经历。")
            return

        edu = self.state.educations[idx]
        edu_id = edu.get("id")

        if edu_id is not None:
            delete_education(edu_id)

        self.state.educations = load_educations()
        self.refresh_lists()

    # ---- experience ----
    def add_exp(self):
        dlg = ExperienceDialog()
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            if not data["title"] or not data["time"]:
                QMessageBox.warning(self, "提示", "名称与起止时间不能为空。")
                return

            # 存数据库
            add_experience(data)

            # 重新从数据库读取
            self.state.experiences = load_experiences()
            self.refresh_lists()

    def edit_exp(self):
        idx = self.exp_list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一条项目/实习经历。")
            return
        init = self.state.experiences[idx]
        dlg = ExperienceDialog(init=init)
        if dlg.exec_() == QDialog.Accepted:
            self.state.experiences[idx] = dlg.get_data()
            self.refresh_lists()

    def del_exp(self):
        idx = self.exp_list.currentRow()
        if idx < 0:
            QMessageBox.information(self, "提示", "请先选中一条项目/实习经历。")
            return

        exp = self.state.experiences[idx]
        exp_id = exp.get("id")

        if exp_id is not None:
            delete_experience(exp_id)

        self.state.experiences = load_experiences()
        self.refresh_lists()


# ---- skills ----
    def save_skills(self):
        raw = self.skill_input.text().strip()
        if not raw:
            self.state.skills = []
        else:
            self.state.skills = [s.strip() for s in raw.split(",") if s.strip()]

        # 调用 backend 存入数据库
        save_skills(self.state.skills)

        # 修改提示信息
        QMessageBox.information(self, "保存成功", "技能信息已成功保存到数据库！")
        self.refresh_lists()