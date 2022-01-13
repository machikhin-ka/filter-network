import telebot
from telebot import types

from config import TELEGRAM_TOKEN
from filters.CartoonFilter import Cartoonizer
from filters.CoolFilter import Cool
from filters.NegativeFilter import Negative
from filters.VintageFilter import Vintage

bot = telebot.TeleBot(TELEGRAM_TOKEN)
negative = Negative()
cartoon = Cartoonizer()
vintage = Vintage()
cool = Cool()

run_keyboard = types.ReplyKeyboardMarkup()
run_btn = types.KeyboardButton('filter')
run_keyboard.add(run_btn)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.from_user.id,
                     "Hi!\nI'm a bot for applying filters to your photos\nTo start, run the command \"/run\" or click "
                     "on the \"filter\" button",
                     reply_markup=run_keyboard)


@bot.message_handler(func=lambda message: message.text == 'filter')
def filter_btn_fun(message):
    do_filter(message)


@bot.message_handler(commands=['run'])
def do_filter(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    cartoon_btn = types.InlineKeyboardButton(text='Cartoon', callback_data='cartoon')
    keyboard.add(cartoon_btn)
    negative_btn = types.InlineKeyboardButton(text='Negative', callback_data='negative')
    keyboard.add(negative_btn)
    vintage_btn = types.InlineKeyboardButton(text='Vintage', callback_data='vintage')
    keyboard.add(vintage_btn)
    cool_btn = types.InlineKeyboardButton(text='Cool', callback_data='cool')
    keyboard.add(cool_btn)
    bot.send_message(message.from_user.id, "Choose one or more filters from the suggested ones below",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "cartoon":
        bot.send_message(call.message.chat.id, "Now upload your photo or picture")
        bot.register_next_step_handler(call.message, cartoon_photo)
    elif call.data == "negative":
        bot.send_message(call.message.chat.id, "Now upload your photo or picture")
        bot.register_next_step_handler(call.message, negative_photo)
    elif call.data == "vintage":
        bot.send_message(call.message.chat.id, "Now upload your photo or picture")
        bot.register_next_step_handler(call.message, vintage_photo)
    elif call.data == "cool":
        bot.send_message(call.message.chat.id, "Now upload your photo or picture")
        bot.register_next_step_handler(call.message, cool_photo)
    else:
        do_filter(call.message)


def cartoon_photo(message):
    photo = get_photo(message)
    bot.send_photo(message.chat.id, cartoon.render(photo))


def negative_photo(message):
    photo = get_photo(message)
    bot.send_photo(message.chat.id, negative.render(photo))


def vintage_photo(message):
    photo = get_photo(message)
    bot.send_photo(message.chat.id, vintage.render(photo))


def cool_photo(message):
    photo = get_photo(message)
    bot.send_photo(message.chat.id, cool.render(photo))


def get_photo(message):
    if message.content_type == 'document':
        return bot.download_file(bot.get_file(message.document.file_id).file_path)
    elif message.content_type == 'photo':
        return bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)


bot.infinity_polling()
