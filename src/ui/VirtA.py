from clientui import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # кнопка отправки сообщения
        self.pushButton.clicked.connect(self.send)
        # кнопка сворачивания приложения
        self.pushButton_3.clicked.connect(self.on_min)
        # кнопка закрытия приложения
        self.pushButton_4.clicked.connect(self.close)

        # кнопки для открытия каждого аватара
        self.pushButton_5.clicked.connect(self.one_avatar)
        self.pushButton_10.clicked.connect(self.two_avatar)
        self.pushButton_12.clicked.connect(self.three_avatar)
        self.pushButton_11.clicked.connect(self.four_avatar)
        self.pushButton_6.clicked.connect(self.close_avatar)

    def one_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/4.png"))

    def two_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/1.png"))

    def three_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/3.png"))

    def four_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/2.png"))

    def close_avatar (self):
        self.label_13.setPixmap(QtGui.QPixmap(""))

    def on_min(self):
        self.showMinimized()

    def send(self):
        self.textBrowser.append(self.textEdit.toPlainText() + "\n")
        self.textEdit.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
