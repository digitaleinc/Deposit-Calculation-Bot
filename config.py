from telebot import TeleBot
import sqlite3

# Please change 'YOUR_BOT_TOKEN' to your Telegram BotFather Token
bot = TeleBot('YOUR_BOT_TOKEN')

# Replace user_id with your
admins = ['user_id']

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()
