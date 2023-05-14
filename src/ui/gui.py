# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lll.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import datetime
import platform
import webbrowser
from fuzzywuzzy import fuzz
from num2t4ru import num2text

from PyQt5 import QtCore, QtGui, QtWidgets

from functions import speak, voice


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.setMinimumSize(QtCore.QSize(290, 375))
        Form.setMaximumSize(QtCore.QSize(290, 375))
        Form.setBaseSize(QtCore.QSize(290, 375))
        Form.setMouseTracking(True)
        Form.setLayoutDirection(QtCore.Qt.RightToLeft)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("background-color: #494D4E")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 340, 231, 31))
        self.plainTextEdit.setMouseTracking(True)
        self.plainTextEdit.setAutoFillBackground(False)
        self.plainTextEdit.setStyleSheet("background-color: #808080")
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit.setLineWidth(0)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setCenterOnScroll(False)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 71, 22))
        self.comboBox.setMouseTracking(True)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("Еще")
        self.comboBox.setIconSize(QtCore.QSize(0, 0))
        self.comboBox.setPlaceholderText("")
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(245, 340, 20, 31))
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/micro.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(24, 22))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(265, 340, 20, 31))
        self.pushButton_3.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/strelka.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(24, 22))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Виртуальный ассистент"))
        self.comboBox.setWhatsThis(_translate("Form", "<html><head/><body><p><br/></p></body></html>"))
        self.comboBox.setItemText(0, _translate("Form", "Еще"))
        self.comboBox.setItemText(1, _translate("Form", "Настройки"))
        self.comboBox.setItemText(2, _translate("Form", "Аватар"))

        self.pushButton_2.clicked.connect(self.voice_input)
        self.pushButton_3.clicked.connect(self.enter_input)

    def voice_input(self):
        self.pushButton_2.setEnabled(False)
        speak.va_speak('Говорите')
        voice.va_listen(self.voice_processing)
        self.pushButton_2.setEnabled(True)

    def voice_processing(self, text):
        self.execute_cmd(text)
        # print(text)

    def enter_input(self):
        self.pushButton_3.setEnabled(False)
        self.execute_cmd(self.plainTextEdit.toPlainText())
        self.pushButton_3.setEnabled(True)

    def execute_cmd(self, command):
        print("Ваша команда: " + command)
        command_list = {
            "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'),
            "ctime": ('время', 'текущее время', 'сейчас времени', 'который час'),
            "system": ('моя система', 'система', 'какая у меня система'),
            "open_browser": ('открой браузер', 'запусти браузер', 'браузер'),
        }

        rc = {'cmd': '', 'percent': 0}
        for c, v in command_list.items():

            for x in v:
                vrt = fuzz.ratio(command, x)
                if vrt > rc['percent']:
                    rc['command'] = c
                    rc['percent'] = vrt

        if rc['percent'] < 50:
            rc['command'] = 'dontknow'

        if rc['command'] == 'help':
            text = "Я умею: ..."
            text += "произносить какое сейчас время ..."
            text += "вывести информацию о системе ..."
            text += "и открыть браузер"
            speak.va_speak(text)

        elif rc['command'] == 'ctime':
            now = datetime.datetime.now()
            text = "Сейчас " + num2text(now.hour) + " " + num2text(now.minute)
            speak.va_speak(text)

        elif rc['command'] == 'system':
            speak.va_speak("Вывожу информацию о системе в консоль")
            sys = platform.uname()
            print("Информация о системе:\n" \
                  f"    Имя системы/OS - {sys[0]}\n" \
                  f"    Сетевое имя компьютера - {sys[1]}\n" \
                  f"    Выпуск системы - {sys[2]}\n" \
                  f"    Версия выпуска системы - {sys[3]}\n" \
                  f"    Тип машины - {sys[4]}\n" \
                  f"    Имя процессора - {sys[5]}")

        elif rc['command'] == 'open_browser':
            speak.va_speak("Открываю браузер")
            url = "https://ya.ru/"
            webbrowser.open(url)

        elif rc['command'] == 'dontknow':
            if 'скажи' in command:
                command = command.replace('скажи', "").strip()
                speak.va_speak(command)
            else:
                speak.va_speak("Я не знаю такой команды")

# import resours.res_rs

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())
