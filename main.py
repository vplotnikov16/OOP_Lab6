from windows.scripts.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
import faulthandler
import sys


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    faulthandler.enable()

    app = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()

    sys.exit(app.exec())
