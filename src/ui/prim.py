import sys
from random import randrange
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
import PyQt5
from PyQt5.QtWidgets import QApplication


class WrapLabel(QtWidgets.QTextEdit):
    def __init__(self, text=''):
        super().__init__(text)
        self.setStyleSheet('''
            WrapLabel {
                border: 1px outset palette(dark);
                border-radius: 8px;
                background: palette(light);
            }
        ''')
        self.setReadOnly(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Maximum)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.updateGeometry)

    def minimumSizeHint(self):
        doc = self.document().clone()
        doc.setTextWidth(self.viewport().width())
        height = doc.size().height()
        height += self.frameWidth() * 2
        return QtCore.QSize(150, height - 100)

    def sizeHint(self):
        return self.minimumSizeHint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometry()


class ChatTest(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()

        container = QtWidgets.QWidget()
        self.setMinimumSize(250, 250)
        self.setWidget(container)
        self.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout(container)
        layout.addStretch()
        self.resize(480, 360)

        for i in range(1, 11):
            QtCore.QTimer.singleShot(1000 * i, lambda i=i:
            self.addMessage('1' * randrange(70, 350), i)
                                     )

    def addMessage(self, text, i):
        wrapLabel = WrapLabel(text)
        if i % 2:
            wrapLabel.setStyleSheet('''
                WrapLabel {
                    border: 1px outset palette(dark);
                    border-radius: 8px;
                    background: palette(light);
                    margin-left: 50px;
                    background: #FFFEB7;
                }
            ''')
        else:
            wrapLabel.setStyleSheet('''
                WrapLabel {
                    border: 1px outset palette(dark);
                    border-radius: 8px;
                    background: palette(light);
                    margin-right: 50px;
                    background: #C8E6F5;
                    color: #6D3939;
                }
            ''')

        self.widget().layout().addWidget(wrapLabel)
        QtCore.QTimer.singleShot(0, self.scrollToBottom)

    def scrollToBottom(self):
        QtWidgets.QApplication.processEvents()
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ChatTest()
    w.show()
    sys.exit(app.exec_())

    # Натройка визуала самого окна, прозрачноть и т д
    self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_NoSystemBackground, True)
    self.setAttribute(Qt.WA_TranslucentBackground, True)

    # геометрия самого окна
    MainWindow.setGeometry(QtCore.QRect(60, 145, 540, 1220))
    MainWindow.setFixedSize(540, 1220)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt