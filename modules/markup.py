from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import json


# Markup
def gen_markup_regular_payment(calc_id):
    extra_data1 = {"regular": 1, "calc_id": calc_id}
    extra_data2 = {"regular": 0, "calc_id": calc_id}

    extra_data_json1 = json.dumps(extra_data1)
    extra_data_json2 = json.dumps(extra_data2)

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("✅ Yes", callback_data=extra_data_json1),
               InlineKeyboardButton("❌ No", callback_data=extra_data_json2))
    return markup


def gen_markup_start():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Calculate"))
    return markup
