from FQW.src.ui.cliengui import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from src.functions.voice_input import VoiceInputThread
from src.functions.voice_assistant import VoiceAssistantThread
import config
from src.functions.functions import va_respond

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # кнопка отправки сообщения
        self.pushButton.clicked.connect(self.send)

        # кнопка отправки голосового сообщения
        self.pushButton_2.clicked.connect(self.start_voice_input)

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

        self.textBrowser.append(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ..." + "\n")
        self.start_speak_assistant(f"Здравствуйте! Меня зовут Виртаа")


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

        # self.start_speak_assistant("Выполняю")
        result = va_respond(self.textEdit.toPlainText())
        self.command_execution(result)
        # self.textEdit.clear()

    def start_voice_input(self):
        self.start_speak_assistant("Говорите")
        self.thread_voice.handler_status = True
        self.thread_voice.start()
        # self.textBrowser.clear()

    def signal_handler(self, voice_command):
        # self.start_speak_assistant(voice_command[0])

        self.textBrowser.append("Ваша команда: " + voice_command[0])
        self.thread_voice.handler_status = False
        self.thread_voice.exit()

        # self.start_speak_assistant("Выполняю")
        result = va_respond(voice_command[0])
        # print(result)
        self.command_execution(result)


    def start_speak_assistant(self, text):
        self.thread_voice_assistant.set_text_say(text)
        self.thread_voice_assistant.start()
        self.thread_voice_assistant.exit()

        # self.thread_voice_assistant.stop()

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
