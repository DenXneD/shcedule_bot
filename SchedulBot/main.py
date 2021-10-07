import telebot
import time
from telebot import types
from classes import config
from classes.Users import Users
from classes.Tools import BackTool
from classes.Community import Data
from time import sleep
from threading import Thread
import schedule
from classes.storage import Loader, NamesStorage
from classes.Parser import Parser

# Thread begin

server_shift = 0


def send_lesson():
    time_now = BackTool.get_time_dict(server_shift)
    now = BackTool.get_curr_time_str(add_hour=server_shift / 3600, add_min=3)

    if time_now["day"] != 'Sat' and time_now["day"] != 'Sun':
        users = Loader.load_data(NamesStorage.load_way)
        for user_id in users:
            today_sch = BackTool.beautified_today_info(Data.today_group_schedule(user_id, shift=server_shift))
            if users[user_id]["remind"]:
                sleep(0.1)
                try:
                    for lesson in today_sch:
                        if lesson[3:8] == str(now):
                            bot.send_message(user_id, "<b>Нагадую, через 3 хвилини розпочинається пара:</b>",
                                             parse_mode='html')
                            bot.send_message(user_id, lesson, parse_mode='html')
                            print("Message sent to", user_id)
                except:
                    print("Message sent error: ", user_id)


schedule.every().day.at("08:57").do(send_lesson)
schedule.every().day.at("10:27").do(send_lesson)
schedule.every().day.at("12:07").do(send_lesson)
schedule.every().day.at("13:37").do(send_lesson)
schedule.every().day.at("15:07").do(send_lesson)
schedule.every().day.at("16:37").do(send_lesson)
schedule.every().day.at("18:07").do(send_lesson)

schedule.every().day.at("14:50").do(send_lesson)


def message_reminder():
    while True:
        schedule.run_pending()
        sleep(5)


bot = telebot.TeleBot(config.TOKEN)
Thread(target=message_reminder).start()


# Thread end

@bot.message_handler(commands=['start'])
def welcome(message):
    Users.authorize(user_id=message.chat.id, user_group=list(Parser.parse(0).keys())[0])
    bot.send_message(message.chat.id,
                     "Привіт, {0.first_name}!\nЯ - <b>{1.first_name}</b>."
                     "Цього бота було створено, щоб допомогти вам відстежувати "
                     "розклад.\n".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    set_group(message)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     "<b>Список команд:</b>\n"
                     "/start - запустити бота\n"
                     "/info - список команд\n"
                     "/group - змінити групу\n"
                     "/prep - інформація про викладачів\n"
                     "/remind - управління сповіщеннями\n"
                     "/today - пари на сьогоді\n"
                     "/tomorrow - пари на завтра\n"
                     "/week - пари на неділю\n"
                     "/nextweek - пари на наступну неділю\n"
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(commands=['group'])
def set_group(message):
    ipz_groups = Parser.parse(0).keys()
    markup = types.InlineKeyboardMarkup(row_width=3)
    for group_name in ipz_groups:
        button = types.InlineKeyboardButton(group_name, callback_data=group_name)
        markup.add(button)

    bot.send_message(message.chat.id,
                     "Будь ласка, оберіть свою групу.".format(message.from_user, bot.get_me()),
                     reply_markup=markup)


@bot.message_handler(commands=['today'])
def today(message):
    time_now = BackTool.get_time_dict(server_shift)
    if time_now["day"] == 'Sat' or time_now["day"] == 'Sun':
        bot.send_message(message.chat.id, "Сьогодні пари відсутні!")
    else:
        today_sch = BackTool.beautified_today_info(Data.today_group_schedule(message.chat.id, server_shift))
        if len(today_sch) == 0:
            bot.send_message(message.chat.id, "Сьогодні пари відсутні!")
        else:
            for lesson in today_sch:
                bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    time_tom = BackTool.get_time_dict(86400 + server_shift)
    if str(time_tom["day"]) == 'Sat' or str(time_tom["day"]) == 'Sun':
        bot.send_message(message.chat.id, "Завтра пари відсутні!")
    else:
        today_sch = BackTool.beautified_today_info(
            Data.today_group_schedule(message.chat.id, shift=86400 + server_shift))
        if len(today_sch) == 0:
            bot.send_message(message.chat.id, "Завтра пари відсутні!")
        else:
            for lesson in today_sch:
                bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['week'])
def week(message):
    week_sch = BackTool.beautified_week_info(Data.week_group_schedule(message.chat.id, shift=server_shift / 3600))
    for lesson in week_sch:
        bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['nextweek'])
def nextweek(message):
    week_sch = BackTool.beautified_week_info(Data.week_group_schedule(message.chat.id, shift=168 + server_shift / 3600))
    for lesson in week_sch:
        bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['prep'])
def prep(message):
    bot.send_message(message.chat.id, BackTool.beautified_prep_info(Parser.prep_parse()), parse_mode='html',
                     disable_web_page_preview=True);


@bot.message_handler(commands=['remind'])
def reminder(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton("Так", callback_data="Так")
    button_no = types.InlineKeyboardButton("Ні", callback_data="Ні")
    markup.add(button_yes, button_no)

    persons = Loader.load_data(NamesStorage.load_way)
    if persons[str(message.chat.id)]["remind"] is True:
        bot.send_message(message.chat.id, "Нагадувач працює. Ви хотіли б його вимкнути?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Нагадувач вимкнено. Ви хотіли б його ввімкнути?", reply_markup=markup)


@bot.message_handler(commands=['get_server_time'])
def get_server_time(message):
    server_time = time.ctime(time.time()).split()
    real_time = time.ctime(time.time() + server_shift).split()
    bot.send_message(message.chat.id, "Час на сервері: " + ' '.join(server_time))
    bot.send_message(message.chat.id, "Реальний час: " + ' '.join(real_time))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message.text == "Будь ласка, оберіть свою групу.":
        group = call.data
        # Remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ви обрали групу.", reply_markup=None)
        # Add user to base
        Users.authorize(user_id=call.message.chat.id, user_group=group)
        info(call.message)

    elif call.message.text == "Нагадувач працює. Ви хотіли б його вимкнути?":
        sbj_name = call.data
        if sbj_name == "Так":
            Users.switch_off_remind_by_user_id(call.message.chat.id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач працює.", reply_markup=None)

    elif call.message.text == "Нагадувач вимкнено. Ви хотіли б його ввімкнути?":
        sbj_name = call.data
        if sbj_name == "Так":
            Users.switch_on_remind_by_user_id(call.message.chat.id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач увімкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнений.", reply_markup=None)


@bot.message_handler(content_types=['text'])
def reaction(message):
    print(message.text)
    info(message)


# RUN
while True:
    bot.polling(none_stop=True, interval=2, timeout=600)
