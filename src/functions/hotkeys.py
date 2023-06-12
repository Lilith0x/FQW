import keyboard
from PyQt5 import QtCore


class HotKeysSettingsThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(HotKeysSettingsThread, self).__init__()
        self.hotkey_button = None

    def set_hotkey_button(self, hotkey_button):
        self.hotkey_button = hotkey_button

    def run(self):
        hotkey = keyboard.read_hotkey(suppress=False)
        self.signal.emit(hotkey)


class HotKeysThread(QtCore.QThread):

    def __init__(self, main_window, hotkeys):
        super(HotKeysThread, self).__init__()
        self.main_window = main_window
        self.hotkeys = hotkeys

    def set_hotkey(self, hotkey, func):
        if func == 0:
            keyboard.add_hotkey(hotkey, self.main_window.start_voice_input)

        elif func == 1:
            keyboard.add_hotkey(hotkey, self.main_window.close_avatar)

        elif func == 2:
            keyboard.add_hotkey(hotkey, self.main_window.hide)

    def remove_hotkey(self, hotkey):
        keyboard.remove_hotkey(hotkey)
        # print('12')

    def run(self):
        for i in range(len(self.hotkeys)):
            if i == 0:
                keyboard.add_hotkey(self.hotkeys[i], self.main_window.start_voice_input)

            elif i == 1:
                keyboard.add_hotkey(self.hotkeys[i], self.main_window.close_avatar)

            elif i == 2:
                keyboard.add_hotkey(self.hotkeys[i], self.main_window.hide)

        # print(keyboard.)

