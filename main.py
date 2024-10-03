from languages import tr
from config import admns, db, last_message_id, bot
import telebot
from telebot import types
import sqlite3
import json
import time
import os

def get_user_language(user_id):
    conn = sqlite3.connect(db, timeout=10)
    c = conn.cursor()

    c.execute("SELECT lang FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return 'en'

def delete_last_message(chat_id):
    global last_message_id
    if last_message_id:
        try:
            bot.delete_message(chat_id, last_message_id)
        except telebot.apihelper.ApiException as e:
            if 'message to delete not found' in str(e):
                print(f"Message not found: {last_message_id}")
            else:
                print(f"Error deleting message {last_message_id}: {e}")
        last_message_id = None

@bot.message_handler(commands=['start'])
def startr(message):
    global last_message_id
    user_id = message.from_user.id
    firstname = message.from_user.first_name

    conn = sqlite3.connect(db, timeout=10)
    c = conn.cursor()

    c.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    user_exists = c.fetchone()

    if user_exists:
        user_id = message.from_user.id
        lang = get_user_language(user_id)

        delete_last_message(message.chat.id)

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
        btn2 = types.InlineKeyboardButton(tr[lang]['login'], callback_data='login')
        btn3 = types.InlineKeyboardButton(tr[lang]['ihaveacc'], callback_data='hhaveacc')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)

        sent_message = bot.send_message(message.chat.id, tr[lang]['start_two'], parse_mode='Markdown', reply_markup=markup)
        last_message_id = sent_message.message_id
    else:
        lang = 'en'
        markup = types.InlineKeyboardMarkup()

        delete_last_message(message.chat.id)

        en = types.InlineKeyboardButton(tr[lang]['english'], callback_data='en_start')
        ru = types.InlineKeyboardButton(tr[lang]['russian'], callback_data='ru_start')
        pl = types.InlineKeyboardButton(tr[lang]['polish'], callback_data='pl_start')
        ind = types.InlineKeyboardButton(tr[lang]['indian'], callback_data='ind_start') 
        arab = types.InlineKeyboardButton(tr[lang]['arabic'], callback_data='arab_start')
        markup.add(en, ru)
        markup.add(pl, ind)
        markup.add(arab)

        sent_message = bot.send_message(message.chat.id, f'Hello, {firstname}. Choose your language:', reply_markup=markup)
        last_message_id = sent_message.message_id
    conn.close()

@bot.callback_query_handler(func=lambda call: True)
def inlineButtonsCalls(call):
    try:
        global last_message_id
        user_id = call.from_user.id
        lang = get_user_language(user_id)
        username = call.from_user.username

        conn = sqlite3.connect(db, timeout=10)
        c = conn.cursor()

        delete_last_message(call.message.chat.id)

        if call.data in ['en_start', 'ru_start', 'pl_start', 'ind_start', 'arab_start']:
            if call.data == 'en_start':
                lang_code = 'en'
            elif call.data == 'ru_start':
                lang_code = 'ru'
            elif call.data == 'pl_start':
                lang_code = 'pl'
            elif call.data == 'ind_start':
                lang_code = 'ind'
            elif call.data == 'arab_start':
                lang_code = 'arab'

            c.execute('INSERT INTO users (id, username, lang) VALUES (?, ?, ?)', (user_id, username, lang_code))

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(tr[lang_code]['register'], callback_data='register')
            btn2 = types.InlineKeyboardButton(tr[lang_code]['login'], callback_data='login')
            btn3 = types.InlineKeyboardButton(tr[lang_code]['hmm'], callback_data='hmm')
            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)

            sent_message = bot.send_message(call.message.chat.id, tr[lang_code]['first_start'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

            conn.commit()

        elif call.data == 'hmm':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
            btn2 = types.InlineKeyboardButton(tr[lang]['login'], callback_data='login')
            markup.add(btn1)
            markup.add(btn2)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['hmm_text'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'login':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            login = types.InlineKeyboardButton(tr[lang]['login'], url='https://vexfile.com/login?rf=473998')
            imlogalrd = types.InlineKeyboardButton(tr[lang]['imlogalrd'], callback_data='hlog')
            markup.add(login)
            markup.add(imlogalrd)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['loginmessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'register':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            reg = types.InlineKeyboardButton(tr[lang]['register'], url='https://vexfile.com/register?rf=473998')
            imlogalrd = types.InlineKeyboardButton(tr[lang]['imregalrd'], callback_data='hreg')
            markup.add(reg)
            markup.add(imlogalrd)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['registermessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'idnthaveacc_inl':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
            btn2 = types.InlineKeyboardButton(tr[lang]['login'], callback_data='login')
            markup.add(btn1)
            markup.add(btn2)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['idnthaveacc_text'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'menu':
            user_id = call.from_user.id
            lang = get_user_language(user_id)
            
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(tr[lang]['profile_inl'], url='https://vexfile.com/home?rf=473998') #profile
            btn2 = types.InlineKeyboardButton(tr[lang]['files_inl'], url='https://vexfile.com/fileshare?rf=473998') #files link
            btn4 = types.InlineKeyboardButton(tr[lang]['payments_inl'], url='https://vexfile.com/payments?rf=473998') #payments
            btn5 = types.InlineKeyboardButton(tr[lang]['settings_inl'], url='https://vexfile.com/profile?rf=473998') #setting
            btn6 = types.InlineKeyboardButton(tr[lang]['prices_inl'], url='https://vexfile.com/rates?rf=473998') #prices for actions           
            btn7 = types.InlineKeyboardButton(tr[lang]['idnthaveacc_inl'], callback_data='idnthaveacc_inl') #i dnt have acc
            
            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn4)
            markup.add(btn5)
            markup.add(btn6)
            markup.add(btn7)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['inlinemenumessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'hlog':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            log = types.InlineKeyboardButton(tr[lang]['login'], callback_data='login')
            reg = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
            imusurelog = types.InlineKeyboardButton(tr[lang]['imlogalrd'], callback_data='menu')
            markup.add(log)
            markup.add(reg)
            markup.add(imusurelog)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['sureloginmessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'hreg':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            reg = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
            imusurereg = types.InlineKeyboardButton(tr[lang]['imregalrd'], callback_data='menu')
            markup.add(reg)
            markup.add(imusurereg)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['sureregistermessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id

        elif call.data == 'hhaveacc':
            delete_last_message(call.message.chat.id)

            markup = types.InlineKeyboardMarkup()
            log = types.InlineKeyboardButton(tr[lang]['login'], callback_data='login')
            reg = types.InlineKeyboardButton(tr[lang]['register'], callback_data='register')
            imusureha = types.InlineKeyboardButton(tr[lang]['ihaveacc'], callback_data='menu')
            markup.add(log)
            markup.add(reg)
            markup.add(imusureha)

            sent_message = bot.send_message(call.message.chat.id, tr[lang]['surehaveaccmessage'], parse_mode='Markdown', reply_markup=markup)
            last_message_id = sent_message.message_id
        else:
            return

        conn.close()

    except Exception as e:
        print(e)

#ADMIN COMMANDS:

@bot.message_handler(commands=['list'])
def list_users(message):
    if message.from_user.id in admns:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        bot.send_message(message.chat.id, f"Users: {user_count}")
        conn.close()
    else:
        bot.reply_to(message, '.')

def save_news(news_text):
    news_file = 'news.json'
    news_data = {'news': news_text}
    with open(news_file, 'w', encoding='utf-8') as file:
        json.dump(news_data, file)

@bot.message_handler(commands=['addnews'])
def add_news(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in admns:
        msg = bot.send_message(message.chat.id, "Enter news text:")
        bot.register_next_step_handler(msg, save_news_step)
    else:
        bot.reply_to(message, '.')

def save_news_step(message):
    news_text = message.text
    save_news(news_text)
    bot.send_message(message.chat.id, "News saved!")

@bot.message_handler(commands=['seenews'])
def see_news(message):
    if message.from_user.id in admns:
        news_file = 'news.json'
        if os.path.exists(news_file):
            with open(news_file, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
                bot.send_message(message.chat.id, f"last news:\n\n{news_data['news']}")
        else:
            bot.send_message(message.chat.id, ".")
    else:
        bot.reply_to(message, '.')

@bot.message_handler(commands=['news'])
def send_news(message):
    if message.from_user.id in admns:
        news_file = 'news.json'
        if os.path.exists(news_file):
            with open(news_file, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
                news_text = news_data['news']

            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT id FROM users")
            users = c.fetchall()

            successful_users = []

            for user in users:
                try:
                    bot.send_message(user[0], news_text)
                    successful_users.append(user[0])
                except Exception as e:
                    print(f"Error sending message to {user[0]}: {e}")

            bot.send_message(message.chat.id, f"News succesful sent to {len(successful_users)} users.")
            conn.close()
        else:
            bot.send_message(message.chat.id, ".")
    else:
        bot.reply_to(message, '.')

if __name__=='__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=120, skip_pending=True)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue