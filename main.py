import telebot
import config
import sqlite3
from telebot import TeleBot, types

bot = telebot.TeleBot('6280622401:AAEf5VjIFGw-s4t2K0isti4oyHEJmFr4cX4')
name = None
@bot.message_handler(commands=['start', 'hello'])
def main(message):
    bot.send_message(message.chat.id, '<b>Привет</b>', parse_mode='html')
    bot.send_message(message.chat.id, f' Привет, {message.from_user.first_name}')

@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))



@bot.message_handler(commands=['check'])
def start(message):
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id integer auto_increment primary key, name varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, для регистрации введите имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id,'Введите имя')
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name) VALUES ('%s')" % (name))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


@bot.message_handler()
def info(message):
    if message.text.lower()== 'привет':
       bot.send_message(message.chat.id, f'Залупа')
bot.polling(none_stop = True)