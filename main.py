# info: made by YangHu in 2022/06/11

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from window import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QIcon('image/a1hpw-zs1zg-001.ico'))
    dialog = Ui_MainWindow()
    dialog.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())






