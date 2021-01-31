import telebot

from core.key import bot_key
from logic.password_generate import get_pass
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


@bot.message_handler(commands=['36ce58394c734dac9132c7de704b1ca43c93d3fd93c8179e38272b68821da6a3'])
def create_licence(message):
    lic = get_pass()
    keys.append(lic)
    bot.send_message(message.chat.id, f"Length: {len(keys)}\nNew: {lic}")


@bot.message_handler(content_types=['text'])
def send_text(message):
    user = next((u for u in users if u.chat_id == message.chat.id), None)
    if message.text in keys and user is None:
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
        user = User(message.chat.id, message.text)
        keys.remove(message.text)
        user.reg_step += 1
        user.search_settings.append(SearchSetting(message.chat.id))
        users.append(user)
        bot.send_message(message.chat.id, "Регистрируем ваш первый поисковой запрос. Для этого выберите свой регион",
                         reply_markup=regions_keyboard)

    elif user is not None and user.reg_step == 1 and message.text in regions.values():
        user.reg_step += 1
        user.search_settings[-1].region = next(key for key in regions.keys() if regions[key] == message.text)
        bot.send_message(message.chat.id, "Вы успешно выбрали регион. \nТеперь выберите категорию",
                         reply_markup=cats_keyboard)

    elif user is not None and user.reg_step == 2 and message.text in categories.values():
        user.reg_step += 1
        user.search_settings[-1].cat = next(key for key in categories.keys() if categories[key] == message.text)
        bot.send_message(message.chat.id, "Отлично, теперь введите название товара, по которому будем искать")

    elif user is not None and user.reg_step == 3:
        user.reg_step += 1
        user.search_settings[-1].name = message.text
        bot.send_message(message.chat.id, "Теперь введите максимальную цену, за которую готовы преобрести товар")

    elif user is not None and user.reg_step == 4:
        user.reg_step += 1
        try:
            price = float(message.text)
        except ValueError:
            bot.send_message(message.chat.id, "Вы ввели неверное значение")
            return
        user.search_settings[-1].price = price

        bot.send_message(message.chat.id, "Ваш поисковой запрос готов \n"
                                          "Для удаления и создания новых запросов используйте команду /requests")
        user.search_settings[-1].is_searchable = True

    elif user is not None and user.reg_step == 5 and message.text == "/requests":
        sender_message = "Id\tНазвание\tЦена\n"
        for i in range(len(user.search_settings)):
            sender_message += f"{i}\t{user.search_settings[i].to_string()} {'✅' if user.search_settings[i].is_searchable else '❌'}\n"
        if len(user.search_settings) == 0:
            sender_message = f"У вас нет запросов на данный момент\n"
        sender_message += "\nВы можете создать новый или удалить запрос через /create и /delete [id]\n" \
                          "А также остановить (/stopRequest [id]) и восстановить /resumeRequest [id])"
        bot.send_message(message.chat.id, sender_message)

    elif user is not None and user.reg_step == 5 and message.text.startswith("/delete"):
        # noinspection PyBroadException
        try:
            request_id = int(message.text.split('/delete ')[1])
            request = user.search_settings[request_id]
            user.search_settings.remove(user.search_settings[request_id])
            bot.send_message(message.chat.id, f"Запрос {request.to_string()} был успешно удалён")
        except Exception:
            bot.send_message(message.chat.id, "Произошла ошибка на сервере, проверьте правильность ввода")

    elif user is not None and user.reg_step == 5 and message.text.startswith("/stopRequest"):
        # noinspection PyBroadException
        try:
            request_id = int(message.text.split('/stopRequest ')[1])
            request = user.search_settings[request_id]
            user.search_settings[request_id].is_searchable = False
            bot.send_message(message.chat.id, f"Запрос {request.to_string()} был успешно остановлен")
        except Exception:
            bot.send_message(message.chat.id, "Произошла ошибка на сервере, проверьте правильность ввода")

    elif user is not None and user.reg_step == 5 and message.text.startswith("/resumeRequest"):
        # noinspection PyBroadException
        try:
            request_id = int(message.text.split('/resumeRequest ')[1])
            request = user.search_settings[request_id]
            user.search_settings[request_id].is_searchable = True
            bot.send_message(message.chat.id, f"Запрос {request.to_string()} был успешно запущен")
        except Exception:
            bot.send_message(message.chat.id, "Произошла ошибка на сервере, проверьте правильность ввода")

    elif user is not None and user.reg_step == 5 and message.text == "/create":
        user.reg_step = 1
        user.search_settings.append(SearchSetting(message.chat.id))
        bot.send_message(message.chat.id, "Регистрируем новый поисковой запрос. Для этого выберите свой регион",
                         reply_markup=regions_keyboard)


bot.polling()
