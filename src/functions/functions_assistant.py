from json import loads
from os import startfile
from webbrowser import open
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from num2words import num2words
from datetime import datetime
from platform import uname


class FunctionsAssistantThread(QThread):
    signal_result = pyqtSignal(list)
    choice_funct = None
    text_temp = None
    data_file = None
    name_open_thing = None

    def run(self):

        if self.choice_funct == 0:
            self.setting()

        elif self.choice_funct == 1:
            self.say_help()

        elif self.choice_funct == 2:
            self.say_time()

        elif self.choice_funct == 3:
            self.open_browser()

        elif self.choice_funct == 4:
            self.say_system()

        elif self.choice_funct == 5:
            self.say_weather_city(0)

        elif self.choice_funct == 6:
            self.say_weather_city(1)

        elif self.choice_funct == 7:
            self.open_file_dir_site(0)

        elif self.choice_funct == 8:
            self.open_file_dir_site(1)

        elif self.choice_funct == 9:
            self.open_file_dir_site(2)

        elif self.choice_funct == 10:
            self.write_file_text(self.text_temp)

    def setting(self):
        self.signal_result.emit([0])

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

        self.signal_result.emit([1, text, text_2])

    def say_time(self):
        now = datetime.now()
        text_say = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang="ru")
        text = "Сегодня: " + f'{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}'
        self.signal_result.emit([2, text_say, str(text)])

    def open_browser(self):
        url = "https://ya.ru/"
        open(url)
        self.signal_result.emit([3, "Выполняю", "Открываю браузер"])

    def say_system(self):
        text_say = "Вывожу информацию о вашей системе"
        sys = uname()
        text = "Информация о системе:\n" \
               f"    Имя системы/OS - {sys[0]}\n" \
               f"    Сетевое имя компьютера - {sys[1]}\n" \
               f"    Выпуск системы - {sys[2]}\n" \
               f"    Версия выпуска системы - {sys[3]}\n" \
               f"    Тип машины - {sys[4]}\n" \
               f"    Имя процессора - {sys[5]}"

        self.signal_result.emit([4, text_say, text])

    def say_weather_city(self, choi):
        try:
            send_url = "http://api.ipstack.com/check?access_key=c024957c288f813bf6f290a7182aa3d7"
            geo_req = requests.get(send_url)
            geo_json = loads(geo_req.text)
            if choi == 0:
                # Тут
                # text_say = "Ваше примерное местоположение:"
                if "city" in geo_json:
                    locat_data = geo_json['city']
                    # text =
                    text = f"Ваше примерное местоположение - {locat_data}"
                else:
                    text = f"{geo_json[0]}"

                self.signal_result.emit([5, "Вывожу ваше расположение", text])

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
                        text += f": {data['weather'][0]['description']},\n"

                        text_say += f" {data['weather'][0]['description']}"

                        text += f"темп-ра: {data['main']['temp']} гр.,\n"
                        text += f"min темп-ра: {data['main']['temp_min']}, "
                        text += f"max темп-ра: {data['main']['temp_max']}"
                        # weat = weath_data['weather'][0]['description']
                        # self.CW.change_weather(weat)

                    else:
                        text = f"{data[0]}"

                    self.signal_result.emit([6, text_say, text])


                except:
                    self.signal_result.emit([-1, "К сожалению сервер не отвечает.\n"
                                                 "Попробуйте позже."])
        except:
            self.signal_result.emit([-1, "Похоже нет доступа к сети.\n"
                                         "Попробуйте позже."])

    def open_file_dir_site(self, choi):
        data_file = self.data_file
        open_thing = self.name_open_thing

        check = 0
        if choi == 0:
            for i in data_file["PathFile"]:
                if i in open_thing:
                    startfile(data_file['PathFile'][i])
                    check = 1
                    self.signal_result.emit([7, "Выполняю", "Открываю файл"])

            if check == 0:
                self.signal_result.emit([-1, "Я не знаю такого файла"])

        elif choi == 1:
            for i in data_file["PathDirectory"]:
                if i in open_thing:
                    startfile(data_file['PathDirectory'][i])
                    check = 1
                    self.signal_result.emit([8, "Выполняю", "Открываю папку"])

            if check == 0:
                self.signal_result.emit([-1, "Я не знаю такой папки"])

        elif choi == 2:
            for i in data_file['Site']:
                if i in open_thing:
                    open(data_file['Site'][i])
                    check = 1
                    self.signal_result.emit([9, "Выполняю", "Открываю сайт"])

            if check == 0:
                self.signal_result.emit([-1, "Я не знаю такого сайта"])



    def write_file_text(self, text):
        if text:
            write_text = str(text)

            now = datetime.now()
            data_write_text = f"{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}\n"
            data_write_text += write_text
            data_write_text += "\n"
            data_write_text += "------------------------------"
            data_write_text += "\n"

            with open("Заметки от VirtA.txt", "a", encoding="utf-8") as file:
                file.write(data_write_text)

        self.signal_result.emit([10, 'Выполняю', "Записываю"])


# test = FunctionsAssistantThread()
# test.choice_funct = 9
# # test.
# test.run()

# config = ConfigParser()
# config.read('../../data/config/settings.ini', encoding='utf-8')
# #
# print(config['PathFile']['заметки'])
# # for i in config['Site']:
# #     print(config['Site'][i])
# os.startfile(config['PathFile']['заметки'])
