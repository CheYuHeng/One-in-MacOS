import os
import sys
import codecs
import jieba
from importlib import reload
from textrank_keyword import TextRankKeyword
from textrank_sentence import TextRankSentence
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow

from func_2_window import W2
from func_3_window import W3
from func_4_window import W4
from func_5_window import W5
from func_6_window import W6
from func_7_window import W7

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

wk_dir = '/Users/cheyuheng/Desktop/python-project/textrank-0806'

# wk_dir = 'E:\python小项目\\textrank-0508'
jieba.load_userdict(os.path.join(wk_dir, 'newDict.txt'))
# text变量中存储获取到的指定txt文件中的具体文本信息
text = ''

trw = TextRankKeyword()
trw2 = TextRankKeyword()
trs = TextRankSentence()

class W1(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(W1, self).__init__(parent)

        self.setupUi(self)

        # 实例化窗口2——7对象，从而实现主窗口中通过点击按钮能直接弹出任一窗口
        self.w2 = W2()
        self.w3 = W3()
        self.w4 = W4()
        self.w5 = W5()
        self.w6 = W6()
        self.w7 = W7()

        # 对主窗口中的“确定”按钮添加各种函数，通过点击“确认”按钮实现多个功能
        self.pushButton.clicked.connect(self.display_input)
        self.pushButton.clicked.connect(self.clear_all)

        # 让各个子窗口的对应显示框显示相应的运行输出结果
        self.pushButton.clicked.connect(self.first_Browser_result)
        self.pushButton.clicked.connect(self.window_2_Browser_1_result)
        self.pushButton.clicked.connect(self.window_2_Browser_2_result)
        self.pushButton.clicked.connect(self.window_3_Browser_result)
        self.pushButton.clicked.connect(self.window_4_Browser_result)
        self.pushButton.clicked.connect(self.window_5_Browser_1_result)
        self.pushButton.clicked.connect(self.window_5_Browser_2_result)
        self.pushButton.clicked.connect(self.window_6_Browser_result)
        self.pushButton.clicked.connect(self.window_7_Browser_result)

        # 对其余的多个按钮添加“打开”功能，从而在主窗口中点击任一按钮能够打开对应编号的子窗口
        self.pushButton_2.clicked.connect(self.open_window_2)
        self.pushButton_3.clicked.connect(self.open_window_3)
        self.pushButton_4.clicked.connect(self.open_window_4)
        self.pushButton_5.clicked.connect(self.open_window_5)
        self.pushButton_6.clicked.connect(self.open_window_6)
        self.pushButton_7.clicked.connect(self.open_window_7)

    # 打开窗口2
    def open_window_2(self):
        self.w2.show()

    # 打开窗口3
    def open_window_3(self):
        self.w3.show()

    # 打开窗口4
    def open_window_4(self):
        self.w4.show()

    # 打开窗口5
    def open_window_5(self):
        self.w5.show()

    # 打开窗口6
    def open_window_6(self):
        self.w6.show()

    # 打开窗口7
    def open_window_7(self):
        self.w7.show()

    # 接收用户输入的函数，接收由输入框所传进来的文本输入路径
    def display_input(self):
        input_content = self.lineEdit.text()
        print('在控制台上显示输入的内容：' + input_content)
        # 全局变量file_path存储由用户输入的待查文本的绝对路径
        global file_path
        file_path = self.lineEdit.text()
        print('要查找的文件路径：' + file_path)

        self.analyze_file(file_path)

    # 分析用户输入的函数，对于用户输入的内容进行多种判断，判断输入路径是否合法
    def analyze_file(self, file_path):
        from PyQt5.QtWidgets import QMessageBox
        # 输入路径合法时开始尝试解析文本
        if os.path.exists(file_path):
            # 使用切片判断路径的最后四位，即文件的格式，如果是txt文件则读取其内容
            if file_path[-4:] == '.txt':
                text_02 = codecs.open(file_path, 'r', 'utf-8').read()
                global text
                text = text_02
                print('文本的整体内容：' + text_02)
            # 如果文件确实存在但不是txt格式，则给出无法解析的弹窗提示
            else:
                QMessageBox.critical(None, '错误', '无法解析该类型的文本', QMessageBox.Ok)
                text = ''
                text_02 = ''

        # 输入路径为空时给出错误弹窗提示，提示输入内容不能为空
        elif file_path == '':
            QMessageBox.critical(None, '错误', '输入内容不能为空', QMessageBox.Ok)
            print('刚才输入为空，打印在控制台上！')
            file_path = '123'
            text = ''
            text_02 = ''
        # 输入路径错误时再给错误弹窗提示，提示路径错误
        else:
            print('刚才输入的路径有误，打印在控制台上！')
            text = ''
            text_02 = ''
            QMessageBox.critical(None, '错误', '文件不存在!', QMessageBox.Ok)

        trw.analyze(text=text_02, lower=True, window=2, need_special_words=True)
        trw2.analyze(text=text_02, lower=True, window=2, need_special_words=False)
        trs.analyze(text=text_02, lower=True, source='all_filters')

    # 清空函数，清除掉界面内各个文本框的既有显示内容
    def clear_all(self):
        self.textBrowser.setPlainText('')
        self.w2.textBrowser.setPlainText('')
        self.w2.textBrowser_2.setPlainText('')
        self.w3.textBrowser.setPlainText('')
        self.w4.textBrowser.setPlainText('')
        self.w5.textBrowser.setPlainText('')
        self.w5.textBrowser_2.setPlainText('')
        self.w6.textBrowser.setPlainText('')
        self.w7.textBrowser.setPlainText('')

    # 让显示框1显示文本中的全部内容
    def first_Browser_result(self):
        # global text
        self.print_result(text)
        print('看看text的结果：' + text)

    # 让窗口2的显示框1显示文本分句的结果
    def window_2_Browser_1_result(self):
        for item in trw.sentences:
            self.print_result_21(str(item))

    # 让窗口2的显示框2显示文本分词的结果
    def window_2_Browser_2_result(self):
        for item in trw.words_no_filter:
            self.print_result_22(str(item))

    # 让窗口3的显示框显示过滤掉停用词后的结果
    def window_3_Browser_result(self):
        for item in trw.words_no_stop_words:
            self.print_result_3(str(item))

    # 让窗口4的显示框显示过滤掉指定词汇后的结果
    def window_4_Browser_result(self):
        for item in trw.words_all_filters:
            self.print_result_4(str(item))

    # 让窗口5的显示框1显示关键词统计结果（含有语气词）
    def window_5_Browser_1_result(self):
        for item in trw.get_keywords(num=self.spinBox.value(), word_min_len=self.spinBox_2.value()):
            self.print_result_51(str(item.word) + ' ' + str(round(item.weight, 6)))


    # 让窗口5的显示框2显示关键词统计结果（不含语气词）
    def window_5_Browser_2_result(self):
        for item in trw2.get_keywords(num=self.spinBox.value(), word_min_len=self.spinBox_2.value()):
            self.print_result_52(str(item.word) + ' ' + str(round(item.weight, 6)))


    # 让窗口6的显示框显示关键短语统计结果
    def window_6_Browser_result(self):
        # 让关键短语的结果不受到程度副词的影响，只获取不考虑程度副词情况下的结果
        for item in trw2.get_keyphrases(key_words_num=self.spinBox_3.value(),
                                         min_occur_time=self.spinBox_4.value()):
            self.print_result_6(str(item))

    # 让窗口7的显示框显示关键句统计结果
    def window_7_Browser_result(self):
        for item in trs.get_key_sentences(num=self.spinBox_5.value()):
            self.print_result_7(str(item.sentences) + ' ' + str(round(item.weight, 5)) + '\n')


    # 显示框1的输出结果
    def print_result(self, content):
        self.textBrowser.append(content)
        self.cursor = self.textBrowser.textCursor()

    # 窗口2显示框1的输出结果
    def print_result_21(self, content):
        self.w2.textBrowser.append(content)
        self.cursor = self.w2.textBrowser.textCursor()

    # 窗口2显示框2的输出结果
    def print_result_22(self, content):
        self.w2.textBrowser_2.append(content)
        self.cursor = self.w2.textBrowser_2.textCursor()

    # 窗口3显示框的输出结果
    def print_result_3(self, content):
        self.w3.textBrowser.append(content)
        self.cursor = self.w3.textBrowser.textCursor()

    # 窗口4显示框的输出结果
    def print_result_4(self, content):
        self.w4.textBrowser.append(content)
        self.cursor = self.w4.textBrowser.textCursor()

    # 窗口5显示框1，显示关键词统计结果，包含特殊语气词
    def print_result_51(self, content):
        self.w5.textBrowser.append(content)
        self.cursor = self.w5.textBrowser.textCursor()

    # 窗口5显示框2，显示关键词统计结果，不包含特殊语气词
    def print_result_52(self, content):
        self.w5.textBrowser_2.append(content)
        self.cursor = self.w5.textBrowser_2.textCursor()

    # 窗口6显示框的输出结果
    def print_result_6(self, content):
        self.w6.textBrowser.append(content)
        self.cursor = self.w6.textBrowser.textCursor()

    # 窗口7显示框的输出结果
    def print_result_7(self, content):
        self.w7.textBrowser.append(content)
        self.cursor = self.w7.textBrowser.textCursor()

# 让窗口能够正常展示、运行、关闭的主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w1 = W1()
    w1.show()
    sys.exit(app.exec_())