import json
import os
import pickle
import re
import webbrowser

import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog
from num2words import num2words
from datetime import datetime
import platform


class FunctionsAssistantThread(QtCore.QThread):
    signal_result = QtCore.pyqtSignal(list)
    choice_funct = None
    text_temp = None

    def run(self):
        if FunctionsAssistantThread.choice_funct == 0:
            self.setting()

        elif FunctionsAssistantThread.choice_funct == 1:
            self.say_help()

        elif FunctionsAssistantThread.choice_funct == 2:
            self.say_time()

        elif FunctionsAssistantThread.choice_funct == 3:
            self.open_browser()

        elif FunctionsAssistantThread.choice_funct == 4:
            self.say_weather_city(0)

        elif FunctionsAssistantThread.choice_funct == 5:
            self.say_weather_city(1)

        elif FunctionsAssistantThread.choice_funct == 6:
            pass

        elif FunctionsAssistantThread.choice_funct == 7:
            self.write_file_text(FunctionsAssistantThread.text_temp)

    def setting(self):
        # добавлять папку, сайт или файл
        # если успею сделать имя пользователя и имя вирты - но на крайний случай,
        # так как это не используется в самом приложении

        pass

    def say_help(self):
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказать о вашем устройстве ..."
        text += "открыть папку, файл или сайт ..."
        text += "сказать, какая погода за окном ..."
        text += "найти ваше местоположение  ..."
        text += "записать что-нибудь в текстовый файл  ..."
        text += "и открывать браузер"

        text_2 = "Я умею: \n"
        text_2 += "1) произносить время \n"
        text_2 += "2) рассказать о вашем устройстве \n"
        text_2 += "3) открыть папку, файл или сайт  \n"
        text_2 += "4) сказать, какая погода за окном \n"
        text_2 += "5) найти ваше местоположение \n"
        text_2 += "6) записать что-нибудь в текстовый файл \n"
        text_2 += "7) открывать браузер."

        return [1, text, text_2]

    def say_time(self):
        now = datetime.now()
        text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang="ru")
        # print(text)
        text_2 = "Сегодня: " + f'{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}'
        self.signal_result.emit([2, text, str(text_2)])

    def open_browser(self):
        url = "https://ya.ru/"
        # url = "https://about:blank"
        webbrowser.open(url)

    def say_system(self):
        text = "Вывожу информацию о вашей системе"
        sys = platform.uname()
        text_2 = "Информация о системе:\n" \
                 f"    Имя системы/OS - {sys[0]}\n" \
                 f"    Сетевое имя компьютера - {sys[1]}\n" \
                 f"    Выпуск системы - {sys[2]}\n" \
                 f"    Версия выпуска системы - {sys[3]}\n" \
                 f"    Тип машины - {sys[4]}\n" \
                 f"    Имя процессора - {sys[5]}"

        self.signal_result.emit([5, text, text_2])

    def say_weather_city(self, choi):
        try:
            send_url = "http://api.ipstack.com/check?access_key=c024957c288f813bf6f290a7182aa3d7"
            geo_req = requests.get(send_url)
            geo_json = json.loads(geo_req.text)
            print(geo_json)
            # text = None
            if choi == 0:
                # Тут
                # text_say = "Ваше примерное местоположение:"
                if "city" in geo_json:
                    locat_data = geo_json['city']
                    # text =
                    text = f"Ваше примерное местоположение - {locat_data}"
                else:
                    text = f"{geo_json[0]}"
                self.signal_result.emit([5, text])

            elif choi == 1:
                city_id = geo_json["location"]["geoname_id"]
                appid = "3afeacd4d791d087699e1eef4315c1ec"
                try:
                    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', \
                                               'APPID': appid})
                    data = res.json()
                    text_say = "Погода на сегодня"
                    if 'name' in data:

                        text = text_say
                        text += f" {data['weather'][0]['description']},\n"
                        text += f"темп-ра: {data['main']['temp']} гр.,\n"
                        text += f"min темп-ра: {data['main']['temp_min']}, "
                        text += f"max темп-ра: {data['main']['temp_max']}"
                        # weat = weath_data['weather'][0]['description']
                        # self.CW.change_weather(weat)

                    else:
                        text = f"{data[0]}"

                    self.signal_result.emit([4, text_say, text])


                except:
                    self.signal_result.emit([-1, "К сожалению сервер не отвечает.\n"
                                                 "Попробуйте позже."])
        except:
            self.signal_result.emit([-1, "Похоже нет доступа к сети.\n"
                                         "Попробуйте позже."])

    def open_file_dir_cite(self, choi, name_open_thing):
        if choi == 0:
            pass
            # with open("Pickle/path_base_win.pickle", "rb") as f:
            #     path = pickle.load(f)
            # for i in path:
            #     i = r"\b" + f"{i}" + r"\b"
            #     i = re.search(i, result)
            #     if i:
            #         os.startfile(path[i[0]])
            # return 0
            # self.textEdit.setText("- Такой папки/файла нет.")

        elif choi == 1:
            pass
            # with open("Pickle/site_base.pickle", "rb") as f:
            #     data_site = pickle.load(f)
            #
            # for key in data_site:
            #     key = r"\b" + f"{key}" + r"\b"
            #     key = re.search(key, ans)
            #     if key:
            #         self.textEdit.setText(f"- Открываю {key[0]} в браузере.")
            #         webbrowser.get(brow).open(key[0])
            #         return 0
            #
            # self.textEdit.setText("- Я не знаю такого сайта")

    def write_file_text(self, text):
        write_text = str(text)

        now = datetime.now()
        data_write_text = f"{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}\n"
        data_write_text += write_text
        data_write_text += "\n"
        data_write_text += "------------------------------"
        data_write_text += "\n"

        with open("Заметки от VirtA.txt", "a", encoding="utf-8") as file:
            file.write(data_write_text)


test = FunctionsAssistantThread()
FunctionsAssistantThread.choice_funct = 0
test.run()
