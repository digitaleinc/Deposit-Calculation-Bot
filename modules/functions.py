from modules.db import get_calculation, create_calculation, set_regular_payment_amount
from modules.markup import gen_markup_regular_payment

from config import bot

import random
import time


# Functions
def calc(deposit, percent, months, is_monthly, monthly_additional):
    dep = float(deposit)
    per = float(percent) / 100.0
    month_percent = round(per / 12, 8)
    print(f"Real year percent: {float(percent)}%")
    print(f"Real monthly percent: {round(month_percent * 100.0, 2)}%")
    profit_counting = 0

    for i in range(months):
        profit = round(dep * month_percent, 2)
        dep = round(dep + profit, 2)
        if is_monthly:
            print(f"ReDepositing {i + 1}: {dep} + additional {monthly_additional} uah")
            dep = round(dep + monthly_additional, 2)
        else:
            print(f"ReDepositing {i + 1}: {dep} uah")
        profit_counting = round(profit_counting + profit, 2)

    print(f"\nYour profit in the end of {months} months is: {profit_counting}\n"
          f"Money in the end: {dep - monthly_additional}")


def main_calculation(user_id, calc_id):
    deposit, percent, months, is_monthly, m_amount = get_calculation(calc_id)

    dep = float(deposit)
    per = float(percent) / 100.0
    month_percent = round(per / 12, 8)
    profit_counting = 0

    for i in range(months):
        profit = round(dep * month_percent, 2)
        dep = round(dep + profit, 2)
        if is_monthly == 1:
            dep = round(dep + m_amount, 2)
        profit_counting = round(profit_counting + profit, 2)

    monthly_pay = "❌ No"
    if is_monthly == 1:
        monthly_pay = "✅ Yes"
        bot.send_message(user_id,
                         f"-------INVESTMENT ORDER #<code>{calc_id}</code>-------\n"
                         f"\n"
                         f"💵 <b>Deposit amount: <u>{float(deposit)}</u></b>\n"
                         f"🏦 <b>Real year percent: {float(percent)}%</b>\n"
                         f"🧮 <b>Real monthly percent: {round(month_percent * 100.0, 2)}%</b>\n"
                         f"🔁 <b>Regular monthly payment:</b> {monthly_pay}\n"
                         f"➕ <b>Regular monthly amount:</b> {m_amount}\n"
                         f"\n"
                         f"📈 Profit in {months} months will be: <b>{profit_counting}</b>\n"
                         f"\n"
                         f"💰 Deposit balance in the end will be: <b>{dep - m_amount}</b>\n"
                         f"\n"
                         f"🇺🇦 <i>Thank you for using this bot. Looking forward to seeing you again!</i>",
                         parse_mode='HTML')
    else:
        m_amount = 0
        bot.send_message(user_id,
                         f"-------INVESTMENT ORDER #<code>{calc_id}</code>-------\n"
                         f"\n"
                         f"💵 <b>Deposit amount: <u>{float(deposit)}</u></b>\n"
                         f"🏦 <b>Real year percent: {float(percent)}%</b>\n"
                         f"🧮 <b>Real monthly percent: {round(month_percent * 100.0, 2)}%</b>\n"
                         f"🔁 <b>Regular monthly payment:</b> {monthly_pay}\n"
                         f"\n"
                         f"📈 Profit in {months} months will be: <b>{profit_counting}</b>\n"
                         f"\n"
                         f"💰 Deposit balance in the end will be: <b>{dep - m_amount}</b>\n"
                         f"\n"
                         f"🇺🇦 <i>Thank you for using this bot. Looking forward to seeing you again!</i>",
                         parse_mode='HTML')


def process_calculate1(message, amount=None):
    user_id = message.from_user.id
    if message.text.replace('.', '', 1).isdigit():
        if 0.01 <= float(message.text) <= 1000000000.0:
            amount = float(message.text)
            bot.send_message(user_id, "➗ Please provide real year percentage provided by your organisation "
                                      "(in range 0.01% - 99.99%, ex: <code>12.35</code>):", parse_mode='HTML')
            bot.register_next_step_handler(message, lambda msg: process_calculate2(msg, amount))
        else:
            bot.send_message(user_id, f"❌ You have entered value that out of range. "
                                      f"Try again, in range 0.01 - 1000000000 :)")
    else:
        bot.send_message(user_id, f"❌ You have entered invalid value. Try again, but without mistakes :)")


def process_calculate2(message, amount, year_percentage=None):
    user_id = message.from_user.id
    if message.text.replace('.', '', 1).isdigit():
        if 0.0001 <= float(message.text) <= 99.9999:
            year_percentage = float(message.text)
            bot.send_message(user_id, "⌛️ Please provide length of deposit in months: "
                                      "(in range 1 - 600 months, ex: <code>12</code>):", parse_mode='HTML')
            bot.register_next_step_handler(message, lambda msg: process_calculate3(msg, amount, year_percentage))
        else:
            bot.send_message(user_id, f"❌ You have entered value that out of range. "
                                      f"Try again, value in range 0.0001 - 99.9999 :)")
    else:
        bot.send_message(user_id, f"❌ You have entered invalid values. Try again, but without mistakes :)")


def process_calculate3(message, amount, year_percentage):
    user_id = message.from_user.id
    if message.text.isnumeric():
        if 1 <= int(message.text) <= 600:
            months = message.text
            calc_id = random.randint(100000000, 999999999)
            create_calculation(user_id, calc_id, amount, year_percentage, months)
            bot.send_message(user_id,
                             "❔ Do you want to make a regular monthly payment in addition to your "
                             "deposit/deposit until the end of the deposit term?",
                             reply_markup=gen_markup_regular_payment(calc_id))
    else:
        bot.send_message(user_id, f"❌ You have entered invalid values. Try again, but without mistakes :)")


def process_monthly_amount(message, calc_id):
    user_id = message.from_user.id
    if message.text.replace('.', '', 1).isdigit():
        if 0.01 <= float(message.text) <= 1000000.0:
            amount_monthly = float(message.text)
            set_regular_payment_amount(calc_id, amount_monthly)
            bot.send_message(user_id, "⏳ Calculating...")
            time.sleep(3)
            # Processing calculation
            main_calculation(user_id, calc_id)
        else:
            bot.send_message(user_id, f"❌ You have entered value that out of range. "
                                      f"Try again, in range 0.01 - 1000000 :)")
    else:
        bot.send_message(user_id, f"❌ You have entered invalid value. Try again, but without mistakes :)")
