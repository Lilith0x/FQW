from PyQt5 import QtWidgets

from clientui import Ui_MainWindow

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


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)

    def send(self):
        wrapLabel = WrapLabel()
        if self.textBrowser.append(self.textEdit.toPlainText()):
            wrapLabel.setStyleSheet('''
                WrapLabel {
                    border: 1px outset palette(dark);
                    border-radius: 8px;
                    background: palette(light);
                    margin-left: 50px;
                    background: #FFFEB7;
                }
            ''')
            self.textEdit.clear()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
