import platform

import set_config
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import webbrowser
import random

import pickle
import numpy as np

from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
# from intent_classifier import IntentClassifier
import nltk
import re
from nltk.corpus import stopwords


VA_CMD_LIST = {
    1: 'привет',
    2: 'пока',
    3: 'открытие файла/приложения',
    4: 'время',
    5: 'открытие браузера',
    6: 'анекдот',
    7: 'функционал',
    8: 'информация о системе',
    9: 'местоположение',
    10: 'погода',
    11: 'открытие сайта',
    12: 'открытие папки',
    13: 'изменение названия файла',
    14: 'изменение параметров',

}

# VA_CMD_LIST = {
#     "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'),
#     "ctime": ('время', 'текущее время', 'сейчас времени', 'который час'),
#     "joke": ('расскажи анекдот', 'рассмеши', 'шутка', 'расскажи шутку', 'пошути', 'развесели'),
#     "system": ('моя система', 'система', 'какая у меня система'),
#     "open_browser": ('открой браузер', 'запусти браузер', 'браузер')
# }

VA_ALIAS = ('вирта', 'вирт')

VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько')


class IntentClassifier:
    def __init__(self):
        self.classes = pickle.load(open('../../models/intent_classifier/classes_CNN.pkl', 'rb'))
        self.tokenizer = pickle.load(open('../../models/intent_classifier/tokenizer_CNN.pkl', 'rb'))
        self.label_encoder = pickle.load(open('../../models/intent_classifier/label_encoder_CNN.pkl', 'rb'))
        self.classifier = load_model('../../models/intent_classifier/intents.h5')

    def get_intent(self,text):
        self.text = [text]
        self.test_keras = self.tokenizer.texts_to_sequences(self.text)
        self.test_keras_sequence = pad_sequences(self.test_keras, maxlen=16, padding='post')
        self.pred = self.classifier.predict(self.test_keras_sequence)
        return self.label_encoder.inverse_transform(np.argmax(self.pred,1))[0]


def va_respond(command):

    if True:
        # обращаются к ассистенту
        intent = intent_rec(clear_text(command))
        cmd = VA_CMD_LIST.get(intent)
        # if cmd['cmd'] not in VA_CMD_LIST.keys():
        #     return [0, "Я не поняла вас"]
        # else:
        return execute_cmd(cmd)

    else:
        return [0, "Я не поняла вас"]

    # stt.Speach.test = False


def clear_text(text: str):
    text = text.lower()
    text = re.sub(r'[^а-яА-ЯёЁ ]', ' ', text)
    text = ' '.join(text.split())


    word_tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words("russian"))

    new_stop_words = ['пожалуйста', 'вирта']

    for i in new_stop_words:
        stop_words.add(i)

    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    text = ' '.join(filtered_sentence)

    return text


# def filter_cmd(raw_voice: str):
#     cmd = raw_voice
#
#     for x in VA_ALIAS:
#         cmd = cmd.replace(x, "").strip()
#
#     for x in VA_TBR:
#         cmd = cmd.replace(x, "").strip()
#     return cmd


# def recognize_cmd(cmd: str):
#     rc = {'cmd': '', 'percent': 0}
#     for c, v in VA_CMD_LIST.items():
#
#         for x in v:
#             vrt = fuzz.ratio(cmd, x)
#             if vrt > rc['percent']:
#                 rc['cmd'] = c
#                 rc['percent'] = vrt
#
#     return rc


def intent_rec(cmd: str):

    nlu = IntentClassifier()
    nlu.get_intent('')

    return nlu.get_intent(cmd)


def execute_cmd(cmd: str):
    # result = []
    if cmd == 'привет':
        return 0

    elif cmd == 'пока':
        return 0

    elif cmd == 'открытие файла/приложения':
        return 0


    elif cmd == 'время':

        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang="ru")
        # print(text)
        text_2 = "Сегодня: " + f'{now.day}-{now.month}-{now.year}'

        return [2, text, str(text_2)]
        # tts.Voice.va_speak(text)


    elif cmd == 'открытие браузера':
        url = "https://ya.ru/"
        webbrowser.open(url)
        return [4]

    elif cmd == 'анекдот':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']
        return [3, random.choice(jokes)]
        # tts.Voice.va_speak(random.choice(jokes))

    elif cmd == 'функционал':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказать о вашем устройстве ..."
        text += "рассказывать анекдоты ..."
        text += "открывать браузер ..."
        text += "открывать папки ..."
        text += "открывать сайты ..."
        text += "показывать погоду ..."
        text += "показывать местоположение ..."

        text_2 = "Я умею: \n"
        text_2 += "1) произносить время \n"
        text_2 += "2) рассказать о вашем устройстве \n"
        text_2 += "3) рассказывать анекдоты \n"
        text_2 += "4) открывать браузер \n"
        text_2 += "5) открывать папки \n"
        text_2 += "6) открывать сайты \n"
        text_2 += "7) показывать погоду \n"
        text_2 += "8) показывать местоположение."

        return [1, text, text_2]
        # tts.Voice.va_speak(text)

    elif cmd == 'информация о системе':
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

    elif cmd == 'местоположение':
        return 0

    elif cmd == 'погода':
        return 0

    elif cmd == 'открытие сайта':
        return 0

    elif cmd == 'открытие папки':
        return 0

    elif cmd == 'изменение названия файла':
        return 0

    elif cmd == 'изменение параметров':
        return 0


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

# nlu = IntentClassifier()
#
# print(nlu.get_intent('время'))
# va_respond('список команд')