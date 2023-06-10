from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp
from src.ui.clientui import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets, QtCore
from src.functions.voice_input import VoiceInputThread
from src.functions.voice_assistant import VoiceAssistantThread
import config
from src.functions.functions import va_respond


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
        self.textBrowser.append(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ..." + "\n")
        self.start_speak_assistant(f"Здравствуйте! Меня зовут Виртаа")

        # self.textEdit.installEventFilter(self)
        # def eventFilter(self, obj, event):
        #     if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
        #         if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus() and event.modifiers() == QtCore.Qt.ShiftModifier:
        #             self.send()
        #             self.textEdit.clear()
        #     return super().eventFilter(obj, event)

        # Горячие клавиши
        self.button_list = [self.ui.key1, self.ui.key2, self.ui.key3]
        self.draw_values()

    def file_read():
        bind_dict = {}
        if os.path.exists('hotkey.dt'):
            with open('hotkey.dt') as inf:
                for line in inf:
                    if re.match(r'([^:]+):([^:]+)', line):
                        bind_dict[line[:line.find(':')]] = line[line.find(':') + 1:].strip()
                    else:
                        file_clear()
        else:
            file_clear()
        return bind_dict

    def draw_values(self):
        k = 0
        for key, value in file_read().items():
            self.button_list[k].setText(key)
            self.lineEdit_list[k].setText(value)
            k += 1

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
        # self.start_speak_assistant("Ваша команда: " + self.textEdit.toPlainText())

        self.textBrowser.append("Ваша команда: " + self.textEdit.toPlainText())
        # удаление текста после отправки сообщения
        self.textEdit.clear()

        # self.start_speak_assistant("Выполняю")
        result = va_respond(self.textEdit.toPlainText())
        self.command_execution(result)
        # self.textEdit.clear()

    def start_voice_input(self):
        self.start_speak_assistant("Говоритее")
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
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
