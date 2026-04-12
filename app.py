import sys
from PyQt5.QtWidgets import QApplication
from backend.database import init_db
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_db()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
