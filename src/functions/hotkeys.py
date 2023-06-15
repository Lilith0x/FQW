import keyboard
from PyQt5 import QtCore


class HotKeysSettingsThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

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
        # pass

    def run(self):
        hotkey = keyboard.read_hotkey(suppress=False)
        self.signal.emit(hotkey)


class HotKeysThread(QtCore.QThread):

    def __init__(self, main_window):
        super(HotKeysThread, self).__init__()
        self.main_window = main_window
        self.hotkeys = None

    def set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys

    # def install_hotkeys(self, hotkey, func):
    #     if func == 0:
    #         keyboard.add_hotkey(hotkey, self.main_window.start_voice_input)
    #
    #     elif func == 1:
    #         keyboard.add_hotkey(hotkey, self.main_window.close_avatar)
    #
    #     elif func == 2:
    #         keyboard.add_hotkey(hotkey, self.main_window.hide)

    def remove_hotkeys(self, hotkeys):
        keyboard.remove_hotkey(hotkeys[0])
        keyboard.remove_hotkey(hotkeys[1])
        keyboard.remove_hotkey(hotkeys[2])

    # def turn_off(self):
    #     keyboard.remove_hotkey(hotkeys[0])

    # def turn_on(self):
    #     keyboard.start_recording()

    # print('12')

    def run(self):
        # for i in range(len(self.hotkeys)):
        #     if i == 0:
        keyboard.add_hotkey(self.hotkeys[0], self.main_window.start_voice_input)

        # elif i == 1:
        keyboard.add_hotkey(self.hotkeys[1], self.main_window.close_avatar)

        # elif i == 2:
        keyboard.add_hotkey(self.hotkeys[2], self.main_window.hide)

        # keyboard.add_hotkey('shift+enter', self.main_window.send)

        # keyboard.unhook_all_hotkeys()
        # keyboard.remove_hotkey('ctrl+q')
        # keyboard.remove_hotkey('ctrl+w')
        # keyboard.remove_hotkey('ctrl+r')
        # keyboard.add_hotkey('ctrl+q', self.main_window.start_voice_input)

        print(len(keyboard._hotkeys))
        # print(keyboard.)
