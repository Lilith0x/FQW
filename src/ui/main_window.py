import threading
import time
import keyboard
from PyQt5.QtCore import pyqtSlot

import config

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp, QDialogButtonBox, QMessageBox, QInputDialog
from PyQt5 import QtGui, QtWidgets, QtCore

from src.ui.clientui import Ui_MainWindow
from src.functions.voice_input import VoiceInputThread
from src.functions.voice_assistant import VoiceAssistantThread
from src.functions.functions import va_respond
from src.functions.hotkeys import HotKeysSettingsThread, HotKeysThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, settings_config):
        super().__init__()
        self.setupUi(self)

        self.settings_config = settings_config

        self.move_window()

        # кнопка отправки сообщения
        self.pushButton.clicked.connect(self.send)

        # кнопка отправки голосового сообщения
        self.pushButton_2.clicked.connect(self.start_voice_input)

        # сворачивание в трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("../data/resours/icon.png"))
        show_action = QAction("Открыть", self)
        hide_action = QAction("Скрыть", self)
        quit_action = QAction("Закрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        # self.tray_icon.().

        # поток для голосового ввода
        self.thread_voice = VoiceInputThread()
        self.thread_voice.signal.connect(self.signal_handler)

        # поток для озвучки ассистента
        self.thread_voice_assistant = VoiceAssistantThread()

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

        # Старт
        self.textBrowser.append(
            f"{self.settings_config['VirtA']['VA_NAME']} (v{self.settings_config['VirtA']['VA_VER']}) начал свою работу ..." + "\n")
        self.start_speak_assistant(f"Здравствуйте! Меня зовут Виртаа")

        # Попытка добавить для текстового ввода - Enter
        # self.textEdit.installEventFilter(self)  # Для ввода Enter

        # Горячие клавиши
        self.thread_hk_settings = HotKeysSettingsThread()
        self.thread_hk_settings.signal.connect(self.change_hotkey)
        self.thread_hk_settings.read_file_hotkeys(self.settings_config)

        self.button_list = [self.pushButton_7, self.pushButton_8, self.pushButton_9]
        for button in range(len(self.button_list)):
            self.button_list[button].setText(self.thread_hk_settings.hotkeys_button[button])
            self.button_list[button].clicked.connect(self.on_hotkey_click)

        self.thread_hotkeys = HotKeysThread(self)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save_hotkey)

        self.check_turn_hotkeys = int(self.settings_config['Hotkeys']['turn_on_off'])
        if self.check_turn_hotkeys == 0:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText("Включить клавиши")

        elif self.check_turn_hotkeys == 1:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText("Отключить клавиши")
            self.start_hotkeys()

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.turn_hotkey)

        self.check_tray_hk = 1
        self.check_avatar_hk = 1

        QInputDialog.getText(self, 'Ввод заметки',
                                            'Введите ваш текст для дальнейшего сохранения '
                                            'его в файле "Заметки от VirtA.txt".')


    # Попытка добавить для текстового ввода - Enter
    # def eventFilter(self, obj, event):
    #     if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
    #         if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus() and event.modifiers() == QtCore.Qt.ShiftModifier:
    #             self.send()
    #     # self.textEdit.clear()
    #     return super().eventFilter(obj, event)

    def start_hotkeys(self):
        self.thread_hotkeys.set_hotkeys(self.thread_hk_settings.hotkeys_button)
        self.thread_hotkeys.start()

    def on_hotkey_click(self):
        button = self.sender()
        for i in self.button_list:
            i.setEnabled(False)

        button.setStyleSheet('background-color: rgb(128, 128, 128);')
        self.thread_hk_settings.set_hotkey_button(button)
        self.thread_hk_settings.start()
        if self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)

    def change_hotkey(self, hotkey):
        if hotkey in self.thread_hk_settings.hotkeys_button:
            QMessageBox.warning(self, "Ошибка", "'Данное сочетание клавиш уже используется")

            for button in range(len(self.button_list)):
                # but_list.append(button.text())
                self.button_list[button].setText(self.thread_hk_settings.hotkeys_button[button])
        else:
            self.thread_hk_settings.hotkey_button.setText(hotkey)

        self.thread_hk_settings.hotkey_button.setStyleSheet('background-color: rgb(73, 77, 78);')

        for i in self.button_list:
            i.setEnabled(True)
        if self.check_turn_hotkeys == 1:
            self.start_hotkeys()

    def save_hotkey(self):
        if self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)

        but_list = []
        for button in self.button_list:
            but_list.append(button.text())
        if len(but_list) == len(list(set(but_list))):
            self.thread_hk_settings.set_hotkeys_button(but_list)
        else:
            QMessageBox.warning(self, "Ошибка", "У вас есть одинаковые сочетания")


        if self.check_turn_hotkeys == 1:
            self.start_hotkeys()

        self.settings_config["Hotkeys"]["hotkey_1"] = self.thread_hk_settings.hotkeys_button[0]
        self.settings_config["Hotkeys"]["hotkey_2"] = self.thread_hk_settings.hotkeys_button[1]
        self.settings_config["Hotkeys"]["hotkey_3"] = self.thread_hk_settings.hotkeys_button[2]
        with open("../data/config/settings.ini", 'w') as configfile:
            self.settings_config.write(configfile)

    def turn_hotkey(self):
        if self.check_turn_hotkeys == 0:
            self.start_hotkeys()
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText("Отключить клавиши")
            self.check_turn_hotkeys = 1
            # pass
        elif self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText("Включить клавиши")
            self.check_turn_hotkeys = 0

        self.settings_config["Hotkeys"]["turn_on_off"] = str(self.check_turn_hotkeys)
        with open("../data/config/settings.ini", 'w') as configfile:
            self.settings_config.write(configfile)

    def show_close_avatar_hotkeys(self):
        if self.check_avatar_hk == 1:
            self.close_avatar()
            self.check_avatar_hk = 0
        elif self.check_avatar_hk == 0:
            self.one_avatar()
            self.check_avatar_hk = 1

    def show_close_win_hotkeys(self):
        if self.check_tray_hk == 1:
            self.hide()
            self.check_tray_hk = 0
        elif self.check_tray_hk == 0:
            self.show()
            self.check_tray_hk = 1

    def move_window(self):
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = int((3 * screen.height()) / 100)
        y = int((screen.height() - widget.height()) - (1 * screen.width()) / 100)
        self.move(x, y)

    def one_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("../data/resours/head/4.png"))
        self.thread_voice_assistant.set_voice_assistant(1)

    def two_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("../data/resours/head/1.png"))
        self.thread_voice_assistant.set_voice_assistant(1)

    def three_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("../data/resours/head/3.png"))
        self.thread_voice_assistant.set_voice_assistant(0)

    def four_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("../data/resours/head/2.png"))
        self.thread_voice_assistant.set_voice_assistant(0)

    def close_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap(""))

    def on_min(self):
        self.showMinimized()

    # @pyqtSlot()
    def send(self):
        self.textBrowser.append("Ваша команда: " + self.textEdit.toPlainText())
        result = va_respond(self.textEdit.toPlainText())

        # удаление текста после отправки сообщения
        self.textEdit.clear()
        self.command_execution(result)

    def start_voice_input(self):
        self.start_speak_assistant("Говоритее")
        self.thread_voice.handler_status = True

        # Попытка оптимизации
        # self.thread_voice.stream.start_stream()

        self.thread_voice.start()

    @QtCore.pyqtSlot(list)
    def signal_handler(self, voice_command):
        self.textBrowser.append("Ваша команда: " + voice_command[0])
        self.thread_voice.handler_status = False

        # Попытка оптимизации
        # self.thread_voice.stream.stop_stream()

        self.thread_voice.exit()

        result = va_respond(voice_command[0])
        self.command_execution(result)

    def start_speak_assistant(self, text):
        self.thread_voice_assistant.set_text_say(text)
        self.thread_voice_assistant.start()
        self.thread_voice_assistant.exit()

    def command_execution(self, result):
        if result[0] in [0, 3]:
            self.start_speak_assistant(result[1])
            self.textBrowser.append(result[1])

        # if result[1] == :
        #     self.start_speak_assistant(result[1])

        elif result[0] == 4:
            self.start_speak_assistant('Открываю браузер')
            # self.textBrowser.append(result[1])

        elif result[0] in [1, 2, 5]:
            self.start_speak_assistant(result[1])
            self.textBrowser.append(result[2])

        # Для записи в заметки
        # else:
        #     text, ok = QInputDialog.getText(self, 'Ввод заметки',
        #                                     'Введите ваш текст для дальнейшего сохранения '
        #                                     'его в файле "Заметки от VirtA.txt".')
        #     if ok:
        #         if text:
        #             Funct.text_temp = text
        #         else:
        #             print('Вы ничего не ввели')
        #     else:
        #         print('Отмена операции')

        self.textBrowser.append("-----------")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
