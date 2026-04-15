from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from ui.state import AppState


class HomePage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.init_ui()

    def init_ui(self):
        # 设置整个首页的浅灰色背景，让白色的卡片更凸显
        self.setStyleSheet("background-color: #F5F7FA;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 80, 60, 40)
        main_layout.setSpacing(50)

        # ==========================================
        # 1. 顶部 Hero 区（大标题与副标题）
        # ==========================================
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)

        title = QLabel("个性化简历生成平台")
        title.setFont(QFont("Microsoft YaHei", 36, QFont.Bold))
        title.setStyleSheet("color: #2C3E50; letter-spacing: 4px;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("「 基于大语言模型的智能求职引擎，打造你的专属职场名片 」")
        subtitle.setFont(QFont("Microsoft YaHei", 14))
        subtitle.setStyleSheet("color: #7F8C8D; letter-spacing: 1px;")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # ==========================================
        # 2. 核心亮点展示区（纯静态悬浮卡片）
        # ==========================================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(40)

        # 封装生成高颜值卡片的函数
        def create_feature_card(icon_text, title_text, desc_text):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid #EBEEF5;
                }
            """)
            card.setFixedSize(240, 200)

            # 给卡片添加柔和的阴影效果（提升高级感）
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(25)
            shadow.setColor(QColor(0, 0, 0, 15))
            shadow.setOffset(0, 8)
            card.setGraphicsEffect(shadow)

            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(20, 35, 20, 20)
            c_layout.setSpacing(15)

            icon = QLabel(icon_text)
            icon.setFont(QFont("Microsoft YaHei", 32))
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet("border: none; background: transparent;")

            c_title = QLabel(title_text)
            c_title.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
            c_title.setAlignment(Qt.AlignCenter)
            c_title.setStyleSheet("color: #303133; border: none; background: transparent;")

            c_desc = QLabel(desc_text)
            c_desc.setFont(QFont("Microsoft YaHei", 10))
            c_desc.setAlignment(Qt.AlignCenter)
            c_desc.setStyleSheet("color: #909399; border: none; background: transparent; line-height: 1.5;")
            c_desc.setWordWrap(True)

            c_layout.addWidget(icon)
            c_layout.addWidget(c_title)
            c_layout.addWidget(c_desc)
            c_layout.addStretch()
            return card

        cards_layout.addStretch()
        # 对应你开题报告中的三大核心流程
        cards_layout.addWidget(create_feature_card("✨", "智能解析", "深度解析目标岗位 JD\n精准提取核心能力要求"))
        cards_layout.addWidget(create_feature_card("🧠", "大模型重塑", "结合个人真实经历\nAI 深度润色与亮点挖掘"))
        cards_layout.addWidget(create_feature_card("📄", "一键排版", "精美 HTML 模板渲染\n一键导出高质量 PDF"))
        cards_layout.addStretch()

        main_layout.addLayout(cards_layout)

        # ==========================================
        # 3. 视觉引导区（用颜色块提示用户操作）
        # ==========================================
        info_layout = QHBoxLayout()
        info_text = QLabel("← 请通过左侧导航栏，依次完善信息开始您的定制之旅")
        info_text.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        # 使用了柔和的蓝色调，既醒目又不会显得突兀
        info_text.setStyleSheet("""
            color: #409EFF; 
            background-color: #ECF5FF; 
            padding: 15px 30px; 
            border-radius: 8px; 
            border: 1px solid #D9ECFF;
        """)
        info_text.setAlignment(Qt.AlignCenter)

        info_layout.addStretch()
        info_layout.addWidget(info_text)
        info_layout.addStretch()

        main_layout.addLayout(info_layout)

        main_layout.addStretch()

        # ==========================================
        # 4. 底部版权/项目信息（答辩专属）
        # ==========================================
        footer = QLabel("Shanghai Maritime University · 计算机科学与技术专业 · 郑昱恒")
        footer.setFont(QFont("Microsoft YaHei", 9))
        footer.setStyleSheet("color: #C0C4CC;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)