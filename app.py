import telebot

from db.app.config import bot_key
from logic.search import search
import time
from threading import *
from models.search_settings import SearchSetting


keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Зарегистрироваться и ввеси параметры поиска', 'Пока')

bot = telebot.TeleBot(bot_key, parse_mode=None)
users = []

search_settings_list = []
keys = ["INUlItqvya", "LvPcGWZIMA", "weAEpMYozh"]


def searching(search_settings):
    while True:
        for setting in search_settings:
            print('searching')
            items = search(setting)
            if items:
                bot.send_photo(setting.chat_id, items[0].photo, caption=items[0].to_string())
                setting.links.append(items[0].link)
            time.sleep(20)


s1 = Thread(target=searching, args=[search_settings_list])
s1.start()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Для начала работы введите ключ (beta)")


@bot.message_handler(commands=['exit'])
def exit_message(message):
    bot.send_message(message.chat.id, "Exit")


@bot.message_handler(commands=['help'])
def help_user(message):
    print("help")
    if message.chat.id in users:
        bot.send_message(message.chat.id, "Параметры поиска вводятся начиная с символов двоеточия (;;).\n"
                         "Далее через проблем пишется название товара (Телевизор)\n"
                                          "Далее также через пробел пишем цену без указания валюты (300)")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "Зарегистрироваться и ввеси параметры поиска".lower():
        users.append(message.chat.id)
        bot.send_message(message.chat.id, "Введите параметы ввода. Пример:\n;; Телевизор 300")
        bot.send_message(message.chat.id, "Если вы хотите более подробное объяснение - используйте команду /help")

    elif message.text.lower() == "Пока".lower():
        exit_message(message)

    elif message.text.startswith(";;"):
        params = message.text.split()
        try:
            setting = SearchSetting(message.chat.id, params[1], params[2])
            search_settings_list.append(setting)
            bot.send_message(message.chat.id, "Вы успешно подписались на рассылку")
        except IndexError:
            bot.send_message(message.chat.id, "Проверьте корректность ввода")

    elif message.text in keys:




bot.polling()
