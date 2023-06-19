import time
from easygui import fileopenbox, diropenbox

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp, QMessageBox, QInputDialog, QMainWindow, \
    QDialogButtonBox, QApplication
from PyQt5.QtCore import pyqtSlot

from src.ui.clientui import Ui_MainWindow
from src.functions.voice_input import VoiceInputThread
from src.functions.intent_classifier import IntentClassifier
from src.functions.voice_assistant import VoiceAssistantThread
from src.functions.hotkeys import HotKeysSettingsThread, HotKeysThread
from src.functions.functions_assistant import FunctionsAssistantThread


class MainWindow(QMainWindow, Ui_MainWindow):
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
        # self.block_voice_input = True
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

        # Подключение модели распознавания

        self.nlu = IntentClassifier()

        # Приветствие
        # Закомменчено, чтобы приложение запускалось
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

        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save_hotkey)

        self.check_turn_hotkeys = int(self.settings_config['Hotkeys']['turn_on_off'])
        if self.check_turn_hotkeys == 0:
            self.buttonBox.button(QDialogButtonBox.Reset).setText("Включить клавиши")

        elif self.check_turn_hotkeys == 1:
            self.buttonBox.button(QDialogButtonBox.Reset).setText("Отключить клавиши")
            self.start_hotkeys()

        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.turn_hotkey)

        self.check_tray_hk = 1
        self.check_avatar_hk = 1

        # Подключение функционала самого помощника
        self.thread_functions = FunctionsAssistantThread()
        self.thread_functions.signal_result.connect(self.command_execution)

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
        with open("../data/config/settings.ini", 'w', encoding='utf-8') as configfile:
            self.settings_config.write(configfile)

        self.settings_config.read('../data/config/settings.ini', encoding='utf-8')

    def turn_hotkey(self):
        if self.check_turn_hotkeys == 0:
            self.start_hotkeys()
            self.buttonBox.button(QDialogButtonBox.Reset).setText("Отключить клавиши")
            self.check_turn_hotkeys = 1
            # pass
        elif self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)
            self.buttonBox.button(QDialogButtonBox.Reset).setText("Включить клавиши")
            self.check_turn_hotkeys = 0

        self.settings_config["Hotkeys"]["turn_on_off"] = str(self.check_turn_hotkeys)
        with open("../data/config/settings.ini", 'w', encoding='utf-8') as configfile:
            self.settings_config.write(configfile)

        self.settings_config.read('../data/config/settings.ini', encoding='utf-8')

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
        screen = QApplication.desktop().screenGeometry()
        widget = self.geometry()
        x = int((3 * screen.height()) / 100)
        y = int((screen.height() - widget.height()) - (1 * screen.width()) / 100)
        self.move(x, y)

    def one_avatar(self):
        self.label_13.setPixmap(QPixmap("../data/resours/head/4.png"))
        self.thread_voice_assistant.set_voice_assistant(1)

    def two_avatar(self):
        self.label_13.setPixmap(QPixmap("../data/resours/head/1.png"))
        self.thread_voice_assistant.set_voice_assistant(1)

    def three_avatar(self):
        self.label_13.setPixmap(QPixmap("../data/resours/head/3.png"))
        self.thread_voice_assistant.set_voice_assistant(0)

    def four_avatar(self):
        self.label_13.setPixmap(QPixmap("../data/resours/head/2.png"))
        self.thread_voice_assistant.set_voice_assistant(0)

    def close_avatar(self):
        self.label_13.setPixmap(QPixmap(""))

    def on_min(self):
        self.showMinimized()

    # def turn_off_button(self):
    #     self.pushButton.setEnabled(False)
    #     self.pushButton_2.setEnabled(False)
    #
    # def turn_on_button(self):
    #     self.pushButton.setEnabled(True)
    #     self.pushButton_2.setEnabled(True)

    # @pyqtSlot()
    def send(self):
        if self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)
        self.textBrowser.append("Ваша команда: " + self.textEdit.toPlainText())
        self.va_respond(str(self.textEdit.toPlainText()).lower())

        # удаление текста после отправки сообщения
        self.textEdit.clear()

    def start_voice_input(self):
        if self.check_turn_hotkeys == 1:
            self.thread_hotkeys.remove_hotkeys(self.thread_hk_settings.hotkeys_button)

        self.start_speak_assistant("Говоритее")
        self.thread_voice.handler_status = True

        # Попытка оптимизации
        # self.thread_voice.stream.start_stream()

        self.thread_voice.start()

    @pyqtSlot(list)
    def signal_handler(self, voice_command):

        self.textBrowser.append("Ваша команда: " + voice_command[1])
        self.thread_voice.handler_status = False

        # Попытка оптимизации
        # self.thread_voice.stream.stop_stream()

        self.thread_voice.exit()
        if voice_command[0] == 1:
            self.va_respond(voice_command[1])

        elif voice_command[0] == -1:
            self.textBrowser.append(voice_command[1])

    def start_speak_assistant(self, text):
        self.thread_voice_assistant.set_text_say(text)
        self.thread_voice_assistant.start()
        self.thread_voice_assistant.exit()

    @pyqtSlot(list)
    def command_execution(self, result):
        # print(result)
        if result[0] == -1:
            self.start_speak_assistant(result[1])
            self.textBrowser.append(result[1])

        elif result[0] == 0:
            self.show_focus_window()
            text, ok = QInputDialog.getText(self, 'Настройки',
                                            'Введите номер пункта, который хотите настроить:\n'
                                            '1. Добавить файл в быстрый доступ;\n'
                                            '2. Добавить папку в быстрый доступ;\n'
                                            '3. Добавить сайт в быстрый доступ.')
            if text and ok:
                if text == '1':
                    self.add_file()
                elif text == '2':
                    self.add_dir()
                elif text == '3':
                    self.add_site()
                else:
                    QMessageBox.warning(self, "Ошибка", "Нет такого пунтка")

                self.settings_config.read('../data/config/settings.ini', encoding='utf-8')

            else:
                QMessageBox.warning(self, "Ошибка", "Отмена операции")


        else:
            self.start_speak_assistant(result[1])
            self.textBrowser.append(result[2])

        self.textBrowser.append("-----------")
        # self.turn_on_button()
        if self.check_turn_hotkeys == 1:
            self.start_hotkeys()

    def va_respond(self, command):

        command = command[0:28]

        intent = self.nlu.clear_text(command)
        cmd = self.nlu.get_intent(intent)
        return self.execute_cmd(cmd, command)

    def execute_cmd(self, choice, request):
        # print(choice)
        choice = int(choice)

        if choice in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.thread_functions.choice_funct = choice

            if choice in [7, 8, 9]:
                self.thread_functions.data_file = self.settings_config
                self.thread_functions.name_open_thing = request

            elif choice == 10:
                self.show_focus_window()

                text, ok = QInputDialog.getText(self, 'Ввод заметки',
                                                'Введите ваш текст для дальнейшего сохранения '
                                                'его в файле "Заметки от VirtA.txt".')

                if ok and text:
                    self.thread_functions.text_temp = text
                else:
                    QMessageBox.warning(self, "Ошибка", "Отмена операции")

            self.thread_functions.start()

        elif choice == 11:
            self.start_speak_assistant(f"Здравствуйте! Меня зовут Виртаа")
            if self.check_turn_hotkeys == 1:
                self.start_hotkeys()
            self.textBrowser.append("-----------")

        elif choice == 12:
            self.start_speak_assistant(f"До свидания")
            time.sleep(3)
            self.close()

        elif choice == -1:
            self.textBrowser.append("Я не поняла вас")
            self.start_speak_assistant("Я не поняла вас")
            # self.turn_on_button()
            if self.check_turn_hotkeys == 1:
                self.start_hotkeys()
            self.textBrowser.append("-----------")

    # Если окно свернуто и не в фокусе
    def show_focus_window(self):
        self.show()
        self.activateWindow()

    def add_file(self):
        choice_dir = fileopenbox()

        if choice_dir != None:
            text, ok = QInputDialog.getText(self, 'Ввод команды',
                                            'Введите команду для открытия файла:')

            if ok and text:
                self.settings_config["PathFile"][text.lower()] = choice_dir
                with open("../data/config/settings.ini", 'w', encoding='utf-8') as configfile:
                    self.settings_config.write(configfile)

                QMessageBox.about(self, "Успешно", "Файл успешно добавлен в быстрый доступ.")
            else:
                QMessageBox.warning(self, "Ошибка", "Отмена операции")
        else:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали файл")

    def add_dir(self):
        choice_dir = diropenbox()

        if choice_dir != None:
            text, ok = QInputDialog.getText(self, 'Ввод команды',
                                            'Введите команду для открытия папки:')

            if ok and text:
                self.settings_config["PathDirectory"][text.lower()] = choice_dir
                with open("../data/config/settings.ini", 'w', encoding='utf-8') as configfile:
                    self.settings_config.write(configfile)

                QMessageBox.about(self, "Успешно", "Папка успешно добавлена в быстрый доступ.")
            else:
                QMessageBox.warning(self, "Ошибка", "Отмена операции")
        else:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали папку")

    def add_site(self):
        text, ok = QInputDialog.getText(self, 'Ввод сайта',
                                        'Введите адрес сайта, который хотите добавить в быстрый доступ:')

        if ok and text:
            site = text
            text, ok = QInputDialog.getText(self, 'Ввод команды',
                                            'Введите команду для открытия сайта:')
            if ok and text:

                self.settings_config["Site"][text.lower()] = site
                with open("../data/config/settings.ini", 'w', encoding='utf-8') as configfile:
                    self.settings_config.write(configfile)

                QMessageBox.about(self, "Успешно", "Сайт успешно добавлен в быстрый доступ.")

            else:
                QMessageBox.warning(self, "Ошибка", "Отмена операции")

        else:
            QMessageBox.warning(self, "Ошибка", "Отмена операции")


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
