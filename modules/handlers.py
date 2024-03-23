from modules.functions import process_calculate1, main_calculation, process_monthly_amount
from modules.db import set_regular_payment_yes, set_regular_payment_no
from modules.markup import gen_markup_start

from config import bot

import time
import json


# Handlers
@bot.callback_query_handler(func=lambda call: call.data and json.loads(call.data).get("regular") in [0, 1])
def callback_query(call):
    user_id = call.message.chat.id
    try:
        extra_data = json.loads(call.data)
        regular = extra_data.get("regular")
        calc_id = extra_data.get("calc_id")
        if regular == 1:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            set_regular_payment_yes(calc_id)
            message = bot.send_message(user_id,
                                       f"💰 Please, provide amount which you want to add every month as regular "
                                       f"payment to your main deposit "
                                       f"(value should be in range 0.01 - 1000000, ex: <code>5000</code>):",
                                       parse_mode='HTML')
            bot.register_next_step_handler(message, lambda msg: process_monthly_amount(msg, calc_id))
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            set_regular_payment_no(calc_id)
            bot.send_message(user_id, "⏳ Calculating...")
            time.sleep(3)
            # Processing calculation
            main_calculation(user_id, calc_id)
    except json.JSONDecodeError:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "An internal error has occurred. Please, try again")
        print("Decode error")


@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == 'private')
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = " "

    bot.send_message(user_id, f"👋 Hello {user_name}! It is a simple bot for calculating to get profit "
                              f"from your deposit(s)",
                     reply_markup=gen_markup_start())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Calculate":
        bot.send_message(user_id, f"💵 Please, provide the first deposit amount "
                                  f"(value should be in range 0.01 - 1000000000, ex: <code>10000</code>):",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, process_calculate1)
