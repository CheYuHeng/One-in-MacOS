import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from no_3_window import Ui_MainWindow

class W3(QMainWindow, Ui_MainWindow):
    # 初始化函数，目的是初始化窗口3中的各个控件
    def __init__(self, parent = None):
        super(W3, self).__init__(parent)
        self.setupUi(self)

# 让窗口能够正常展示、运行、关闭的主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w3 = W3()
    w3.show()
    sys.exit(app.exec_())