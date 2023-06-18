import threading
import time
import keyboard
import config

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp, QDialogButtonBox
from PyQt5 import QtGui, QtWidgets, QtCore

from src.ui.clientui import Ui_MainWindow
from src.functions.voice_input import VoiceInputThread
from src.functions.voice_assistant import VoiceAssistantThread
from src.functions.functions import va_respond, clear_text, intent_rec
from src.functions.hotkeys import HotKeysSettingsThread, HotKeysThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move_window()

        # кнопка отправки сообщения
        self.pushButton.clicked.connect(self.send)

        # кнопка отправки голосового сообщения
        self.pushButton_2.clicked.connect(self.start_voice_input)

        # сворачивание в трей
        tray_icon = None

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resours/icon.png"))

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
        # self.tray_icon.contextMenu().

        # # поток для голосового ввода
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
        self.textBrowser.append("Вирта 0.2 начал свою работу ..." + "\n")
        self.start_speak_assistant(f"Здравствуйте! Меня зовут Виртаа")

        self.textEdit.installEventFilter(self)  # Для ввода Enter

        # Горячие клавиши
        self.thread_hk_settings = HotKeysSettingsThread()
        self.thread_hk_settings.signal.connect(self.change_hotkey)
        self.button_list = [self.pushButton_7, self.pushButton_8, self.pushButton_9]
        self.read_file_hotkeys()
        #
        # print(self.button_list)
        for button in self.button_list:
            button.clicked.connect(self.on_key_click)

        # self.saveButton = self.buttonBox_4.button(QDialogButtonBox.Apply)
        # self.saveButton.clicked.connect(self.save_elements)
        #
        # self.clearButton = self.buttonBox_4.button(QDialogButtonBox.Reset)
        # self.clearButton.clicked.connect(self.clear_elements)

        # self.startButton.clicked.connect(self.start_program)
        # self.start_program()
        self.thread_hotkeys = HotKeysThread(self, ['ctrl+q', 'ctrl+w', 'ctrl+e'])
        self.thread_hotkeys.start()
        # self.thread_hotkeys.exit()


    # def start_program(self):
    #     self.return_off()
    #     threading.Thread(target=self.animate_button, args=(self.sender(),)).start()
    #     global program_status
    #     program_status = not program_status
    #     if program_status:
    #         self.ui.startButton.setText('Остановить')
    #         self.save_elements()
    #         threading.Thread(target=bind_thread, args=(file_read(),)).start()
    #     else:
    #         self.ui.startButton.setText('Запустить')

    # def save_elements(self):
    #     # self.return_off()
    #     threading.Thread(target=self.animate_button, args=(self.sender(),)).start()
    #     bind_dict = self.button_list
    #         # {self.button_list[i].text():self.lineEdit_list[i].text() for i in range(len(self.button_list)) if self.lineEdit_list[i].text() and self.button_list[i].text()}
    #     # file_save(bind_dict)

    # def clear_elements(self):
    #     threading.Thread(target=self.animate_button, args=(self.sender(),)).start()
    #     # self.can_return = not self.can_return
    #     # if self.can_return:
    #     #     self.ui.clearButton.setText('Вернуть')
    #     for element in self.button_list:
    #         element.setText('')
    #     # else:
    #     #     self.ui.clearButton.setText('Очистить')
    #     #     self.draw_values()

    # def animate_button(self, button):
    #     button.setStyleSheet('background-color: #D3D3D3;')
    #     time.sleep(0.5)
    #     button.setStyleSheet('')

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
            if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus() and event.modifiers() == QtCore.Qt.ShiftModifier:
                self.send()
        # self.textEdit.clear()
        return super().eventFilter(obj, event)

    def start_hotkeys(self):
        pass

    def on_key_click(self):
        button = self.sender()
        for i in self.button_list:
            i.setEnabled(False)

        button.setStyleSheet('background-color: rgb(128, 128, 128);')

        check = self.button_list.index(button)
        # print(check)
        # print(self.button_list[check].text())

        # Tut
        # if self.button_list[check].text() != '':
        #     print(112)
        self.thread_hotkeys.remove_hotkey(self.button_list[check].text())

        self.thread_hk_settings.set_hotkey_button(button)
        self.thread_hk_settings.start()

    def change_hotkey(self, hotkey):
        self.thread_hk_settings.hotkey_button.setText(hotkey)
        for i in self.button_list:
            i.setEnabled(True)
        self.thread_hk_settings.hotkey_button.setStyleSheet('background-color: rgb(73, 77, 78);')

        check = self.button_list.index(self.thread_hk_settings.hotkey_button)
        # print(check)
        # self.button_list[check] = hotkey
        self.thread_hotkeys.set_hotkey(hotkey, check)

    def read_file_hotkeys(self):
        k = 0
        # self.button_list = config.VA_HOT_KEYS
        for key in ['ctrl+q', 'ctrl+w', 'ctrl+e']:
            self.button_list[k].setText(key)
            # self.lineEdit_list[k].setText(value)
            k += 1


    def apply_hotkey(self):
        pass

    def reset_hotkey(self):
        pass

    def move_window(self):
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = int((3 * screen.height()) / 100)
        y = int((screen.height() - widget.height()) - (1 * screen.width()) / 100)
        self.move(x, y)

    def one_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/4.png"))

    def two_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/1.png"))

    def three_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/3.png"))

    def four_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap("resours/head/2.png"))

    def close_avatar(self):
        self.label_13.setPixmap(QtGui.QPixmap(""))

    def on_min(self):
        self.showMinimized()

    def send(self):

        self.textBrowser.append("Ваша команда: " + self.textEdit.toPlainText())

        # self.start_speak_assistant("Выполняю")
        result = va_respond(self.textEdit.toPlainText())
        self.command_execution(result)

        # удаление текста после отправки сообщения
        self.textEdit.clear()

    def start_voice_input(self):
        self.start_speak_assistant("Говорите")
        self.thread_voice.handler_status = True
        # self.thread_voice.stream.start_stream() - ФИКСИТЬ
        self.thread_voice.start()
        # self.textBrowser.clear()

    def signal_handler(self, voice_command):
        # self.start_speak_assistant(voice_command[0])

        self.textBrowser.append("Ваша команда: " + voice_command[0])
        self.thread_voice.handler_status = False
        # self.thread_voice.stream.stop_stream() - ВОТ ЭТО НУЖНО БУДЕТ ОТФИКСИТЬ
        self.thread_voice.exit()

        # self.start_speak_assistant("Выполняю")
        result = va_respond(voice_command[0])
        self.command_execution(result)

    def start_speak_assistant(self, text):
        self.thread_voice_assistant.set_text_say(text)
        self.thread_voice_assistant.start()
        self.thread_voice_assistant.exit()

        # pass
        # self.thread_voice_assistant.stop() - ХЗ ВЫХОД ИЛИ СТОП

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

        self.textBrowser.append("-----------")


if __name__ == "__main__":
    # print(va_respond('пожалуйста, скажи время'))
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
