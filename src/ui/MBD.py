from PyQt5 import QtWidgets

from clientui import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)

    def send(self):
        self.textBrowser.append(self.textEdit.toPlainText())
        self.textEdit.repaint()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
