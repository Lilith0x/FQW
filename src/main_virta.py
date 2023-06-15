from PyQt5 import QtWidgets
from ui.main_window import MainWindow
from configparser import ConfigParser

if __name__ == "__main__":
    config = ConfigParser()
    config.read('../data/config/settings.ini')

    app = QtWidgets.QApplication([])
    window = MainWindow(config)
    window.show()
    app.exec_()
