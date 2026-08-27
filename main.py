import telebot
from flask import Flask
from threading import Thread
from telebot import types

TOKEN = "8856354483:AAEq4E5DsYuzSkGxYP_pQYCf3aXgOGUQ7pE"
ADMIN_ID = 7562950426

bot = telebot.TeleBot(TOKEN)

user_history = {}

START_TEXT = """Приветствуем,в ROBLOX EXPLOIT BOT,выберите что вам нужно и следуйте инструкциям❤️🕷"""

WAIT_TEXT = "⏳ Ваше обращение в очереди, ожидайте! В процессе кодирования... 🌸"

INFO_TEXT = """ℹ️ ИНФОРМАЦИЯ:
Здесь ты можешь написать любые правила, контакты или условия работы твоего бота."""

ROULETTE_TEXT = """🎰 РУЛЕТКА ROBUX:
Тут опиши условия рулетки. Например: Испытай свою удачу и выиграй робуксы! Чтобы крутить рулетку, отправь..."""

AVATAR_TEXT = """🎨 СОЗДАНИЕ 3-D АВАТАРА:
Напиши сюда инструкцию. Например: Для создания уникального 3-D аватара вашего персонажа пришлите его никнейм в Roblox."""

RECOVERY_TEXT = """🔑 ВОССТАНОВЛЕНИЕ СТАРОГО АККАУНТА:
Текст для восстановления. Например: Чтобы подать заявку на восстановление старого аккаунта, укажите ник и год создания..."""


def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ℹ️ Информация")
    btn2 = types.KeyboardButton("🎰 Рулетка")
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton("🎨 Сделать свой 3-D аватар")
    btn4 = types.KeyboardButton("🔑 Восстановить свой старый аккаунт")
    markup.row(btn3)
    markup.row(btn4)
    return markup


@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, START_TEXT, reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID, content_types=['text'])
def handle_users_messages(message):
    if message.text == "ℹ️ Информация":
        bot.send_message(message.chat.id, INFO_TEXT)
    elif message.text == "🎰 Рулетка":
        bot.send_message(message.chat.id, ROULETTE_TEXT)
    elif message.text == "🎨 Сделать свой 3-D аватар":
        bot.send_message(message.chat.id, AVATAR_TEXT)
    elif message.text == "🔑 Восстановить свой старый аккаунт":
        bot.send_message(message.chat.id, RECOVERY_TEXT)
    else:
        fw = bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        user_history[fw.message_id] = message.chat.id
        bot.send_message(message.chat.id, WAIT_TEXT)


@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID, content_types=['photo', 'document', 'voice'])
def forward_files_to_admin(message):
    fw = bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    user_history[fw.message_id] = message.chat.id
    bot.send_message(message.chat.id, WAIT_TEXT)


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message is not None)
def reply_to_user(message):
    msg_id = message.reply_to_message.message_id
    if msg_id in user_history:
        user_id = user_history[msg_id]
        try:
            bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=message.message_id)
            bot.send_message(ADMIN_ID, "💬Ожидайте,ваш запрос в очереди и обработке кодингом💭")
        except Exception:
            bot.send_message(ADMIN_ID, "❌ Пользователь заблокировал бота.")
    else:
        bot.send_message(ADMIN_ID, "❌ Не удалось определить адресата.")


app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

bot.infinity_polling()
