import keyboard
from PyQt5.QtCore import QThread, pyqtSignal


class HotKeysSettingsThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(HotKeysSettingsThread, self).__init__()
        self.hotkey_button = None
        self.hotkeys_button = None

    def set_hotkey_button(self, hotkey_button):
        self.hotkey_button = hotkey_button

    def read_file_hotkeys(self, config):
        self.hotkeys_button = [config['Hotkeys']['hotkey_1'], config['Hotkeys']['hotkey_2'],
                               config['Hotkeys']['hotkey_3']]

    def set_hotkeys_button(self, hotkeys):
        self.hotkeys_button = hotkeys

    def run(self):
        hotkey = keyboard.read_hotkey(suppress=False)
        self.signal.emit(hotkey)


class HotKeysThread(QThread):

    def __init__(self, main_window):
        super(HotKeysThread, self).__init__()
        self.main_window = main_window
        self.hotkeys = None

    def set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys

    def remove_hotkeys(self, hotkeys):
        keyboard.remove_hotkey(hotkeys[0])
        keyboard.remove_hotkey(hotkeys[1])
        keyboard.remove_hotkey(hotkeys[2])

    def run(self):
        keyboard.add_hotkey(self.hotkeys[0], self.main_window.start_voice_input)

        keyboard.add_hotkey(self.hotkeys[1], self.main_window.show_close_win_hotkeys)

        keyboard.add_hotkey(self.hotkeys[2], self.main_window.show_close_avatar_hotkeys)

        # Попытка добавить для текстового ввода - Enter
        # keyboard.add_hotkey('shift+enter', self.main_window.send)
