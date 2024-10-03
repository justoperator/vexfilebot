import telebot

token = 'PASTE HERE YOUR API TOKEN FROM @BotFather'
bot = telebot.TeleBot(token)

admns = [PASTE HERE YOUR TELEGRAM ID]

db = 'database/main.db'

last_message_id = None #variable that saves the last bot message in order to delete it before sending a new one