import telebot #сама библеотека для бота https://pypi.org/project/pyTelegramBotAPI/
from telebot import types #модуль типов для бота
import configure #наш файл configure где хранится токен для бота и owm
import time 
from datetime import datetime #библеотека для работы со временем https://pythonworld.ru/moduli/modul-datetime.html
from pyowm import OWM #OpenWeatherMap's для работы с погодой https://pypi.org/project/pyowm/ сайт проекта https://home.openweathermap.org/api_keys
from pyowm.utils import config, timestamps


BotToken = configure.config['BotToken'] 
owm = OWM(configure.config['OWMapi']) 

bot = telebot.TeleBot(BotToken) #обращяемся к боту по токену 
   
@bot.message_handler(content_types = ['text']) 
def get_text_messages(message): #в телеботе все работает на функциях, в аргументе функции указываем наше сообщение
    if message.text == "Привет": #ну тут все понятно
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/start":

        start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 52)
        finish_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 20, 35) #дату можно указать как на компе (как тут), или строго. Вот так
        '''
        ПРИМЕР
        datetime.datetime(2006, 11, 21, 16, 30)
        2006    # year
        11      # month
        21      # day
        16      # hour
        30      # minute
        '''
        mgr = owm.weather_manager() ##обращяемся к OpenWeatherMap's по токену (почти то же что у telebot)
        observation = mgr.weather_at_place('Gomel’') # Поиск текущей погоды в Гомеле  и получение подробностей (до w = observation.weather)
        w = observation.weather
        temp= int(w.temperature('celsius')['temp']) #переменной temp присваиваем средние значение температуры (вместо ['temp'] можно  {'temp_max': 10.5 => ['temp_max'] , 'temp': 9.7 => ['temp'] , 'temp_min': 9.0 => [temp_min]})
        today = datetime.today() #тут понятно 
        day = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'] #тоже понятно
        week_day = (day[int(today.strftime('%w'))]) #datetime.weekday() - день недели в виде числа, понедельник - 0, воскресенье - 6.=> int(today.strftime('%w')) элнменты массива о = Воскресенье 6 = Суббота
        bot.send_message(message.chat.id,"Бот активен")
        while True:
            if start_time < datetime.now() < finish_time: #сравниваем наше время (datetime.now()) с start_time и finish_time
                print('success') #выводим в консоль success (можно убрать)
                bot.send_message(message.chat.id, 'СЕГОДНЯ \n' +  week_day + '\n' +  today.strftime('%m-%d-%Y\n') +  today.strftime('%H : %M\n')  + 'Температура:   '+ str(temp) + '℃' )
                break
            else:
                print('fail')
            time.sleep(10) # можно 1800
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /start.")


        
bot.polling(none_stop = True, interval = 0)
