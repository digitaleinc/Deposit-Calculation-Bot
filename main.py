from config import bot, admins


def start_bot():
    print("Bot was successfully started")
    for admin in admins:
        bot.send_message(admin, f"✅ Bot was started")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == '__main__':
    start_bot()
