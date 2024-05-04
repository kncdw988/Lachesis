import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from gui.window.main_window import MainWindow
from service.dao.migration import upgrade_db

# 升级数据库
upgrade_db()

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
app = QApplication(sys.argv)

if __name__ == "__main__":
    w = MainWindow()
    w.show()
    app.exec_()
