from PyQt5 import QtWidgets
import sys
from ui.gui import Ui_Form
import ui.resours.res_rs


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

