import telebot

from core.key import bot_key
from logic.search import search
import time
from threading import *
from models.search_settings import SearchSetting
from models.user import User
from core.consts import regions, categories

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Зарегистрироваться и ввеси параметры поиска', 'Пока')


regions_keyboard = telebot.types.ReplyKeyboardMarkup()
regions_keyboard.row(regions.get('1'), regions.get('2'))
regions_keyboard.row(regions.get('3'), regions.get('4'))
regions_keyboard.row(regions.get('5'), regions.get('6'))
regions_keyboard.row(regions.get('7'))

cats_keyboard = telebot.types.ReplyKeyboardMarkup()
cats_keyboard.row(categories['3000'], categories['4000'])
cats_keyboard.row(categories['5000'], categories['6000'])
cats_keyboard.row(categories['7000'], categories['8000'])
cats_keyboard.row(categories['9000'], categories['10000'])
cats_keyboard.row(categories['11000'], categories['12000'])
cats_keyboard.row(categories['13000'], categories['14000'])
cats_keyboard.row(categories['15000'], categories['16000'])
cats_keyboard.row(categories['17000'], categories['18000'])
cats_keyboard.row(categories['19000'], categories['20000'])

bot = telebot.TeleBot(bot_key, parse_mode=None)
users = []

search_settings_list = []
keys = ["INUlItqvya", "LvPcGWZIMA", "weAEpMYozh"]


def searching(searchers):
    while True:
        for user in searchers:
            for setting in user.search_settings:
                if setting.is_searchable:
                    print('searching')
                    items = search(setting)
                    if items:
                        bot.send_photo(setting.chat_id, items[0].photo, caption=items[0].to_string())
                        setting.links.append(items[0].link)
                    time.sleep(20)


s1 = Thread(target=searching, args=[users])
s1.start()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Для начала работы введите ключ (beta)")


@bot.message_handler(content_types=['text'])
def send_text(message):
    user = next((u for u in users if u.chat_id == message.chat.id), None)
    if message.text in keys and user is None:
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
        user = User(message.chat.id, message.text)
        user.reg_step += 1
        user.search_settings.append(SearchSetting(message.chat.id))
        users.append(user)
        bot.send_message(message.chat.id, "Регистрируем ваш первый поисковой запрос. Для этого выберите свой регион",
                         reply_markup=regions_keyboard)

    elif user.reg_step == 1 and message.text in regions.values():
        user.reg_step += 1
        user.search_settings[0].region = next(key for key in regions.keys() if regions[key] == message.text)
        bot.send_message(message.chat.id, "Вы успешно выбрали регион. \nТеперь выберите категорию",
                         reply_markup=cats_keyboard)

    elif user.reg_step == 2 and message.text in categories.values():
        user.reg_step += 1
        user.search_settings[0].cat = next(key for key in categories.keys() if categories[key] == message.text)
        bot.send_message(message.chat.id, "Отлично, теперь введите название товара, по которому будем искать")

    elif user.reg_step == 3:
        user.reg_step += 1
        user.search_settings[0].name = message.text
        bot.send_message(message.chat.id, "Теперь введите максимальную цену, за которую готовы преобрести товар")

    elif user.reg_step == 4:
        user.reg_step += 1
        user.search_settings[0].price = message.text

        bot.send_message(message.chat.id, "Ваш поисковой запрос готов \n"
                                          "Для удаления и создания новых запросов используйте команду /requests")
        user.search_settings[0].is_searchable = True


bot.polling()
