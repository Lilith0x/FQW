import platform

import config
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import webbrowser
import random


def va_respond(command):
    # print(voice)
    if command.startswith(config.VA_ALIAS) or True:
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(command))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            return [0, "Я не поняла вас"]
        else:
            return execute_cmd(cmd['cmd'])

    else:
        return [0, "Я не поняла вас"]
    # stt.Speach.test = False


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()
    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    # result = []

    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказать о вашем устройстве ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"

        text_2 = "Я умею: \n"
        text_2 += "1) произносить время \n"
        text_2 += "2) рассказать о вашем устройстве \n"
        text_2 += "3) рассказывать анекдоты \n"
        text_2 += "4) открывать браузер."

        return [1, text, text_2]
        # tts.Voice.va_speak(text)

    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2words(now.hour) + " " + num2words(now.minute)

        text_2 = now

        return [2, text, str(text_2)]
        # tts.Voice.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']
        return [3, random.choice(jokes)]
        # tts.Voice.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        url = "https://ya.ru/"
        webbrowser.open(url)
        return [4]

    elif cmd == 'system':
        text = "Вывожу информацию о вашей системе"
        sys = platform.uname()
        text_2 = "Информация о системе:\n" \
                 f"    Имя системы/OS - {sys[0]}\n" \
                 f"    Сетевое имя компьютера - {sys[1]}\n" \
                 f"    Выпуск системы - {sys[2]}\n" \
                 f"    Версия выпуска системы - {sys[3]}\n" \
                 f"    Тип машины - {sys[4]}\n" \
                 f"    Имя процессора - {sys[5]}"
        return [5, text, text_2]

# начать прослушивание команд

# stt.Speach.va_listen(va_respond)
# num = 1
# while num:
#     num = int(input('Test = '))
#     if num == 1:
#         print('Говорите: ')
#         stt.Speach.test = True
#         stt.Speach.va_listen(va_respond)
# print(va_respond('вирта открой браузер'))