import sys
import os
import django
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ------------------------------
# Django
# ------------------------------
sys.path.append(r"H:\Projects\subio2.0")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subio.settings')
django.setup()

from django.contrib.auth import get_user_model
from subscriptions.models import Subscription

User = get_user_model()
bot = telebot.TeleBot("8597610610:AAFk5997JlG_uL6TAjSWMRyB65Ya_BiMmCQ")

# тимчасове зберігання стану користувачів
user_sessions = {}

# ------------------------------
# /start
# ------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вітаю! 👋\nВведи свій нік з сайту SUBIO:")
    user_sessions[chat_id] = {"step": "username"}

# ------------------------------
# Авторизація
# ------------------------------
@bot.message_handler(func=lambda m: True)
def auth_handler(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_sessions:
        bot.send_message(chat_id, "Напиши /start")
        return

    step = user_sessions[chat_id]["step"]

    # крок 1: нік
    if step == "username":
        try:
            user = User.objects.get(username=text)
        except User.DoesNotExist:
            bot.send_message(chat_id, "❌ Користувача з таким ніком не знайдено. Спробуй ще раз:")
            return
        user_sessions[chat_id]["user"] = user
        user_sessions[chat_id]["step"] = "password"
        bot.send_message(chat_id, "✅ Нік знайдено. Введи пароль:")
        return

    # крок 2: пароль
    if step == "password":
        user = user_sessions[chat_id]["user"]
        if not user.check_password(text):
            bot.send_message(chat_id, "❌ Невірний пароль. Спробуй ще раз:")
            return
        user_sessions[chat_id]["authenticated"] = True
        user_sessions[chat_id]["step"] = "done"
        bot.send_message(chat_id, f"🎉 Вхід успішний, {user.username}!\nТепер використай /subs щоб побачити підписки.")
        return

# ------------------------------
# Показ підписок
# ------------------------------
@bot.message_handler(commands=['subs'])
def show_subs(message):
    chat_id = message.chat.id
    session = user_sessions.get(chat_id)
    if not session or not session.get("authenticated"):
        bot.send_message(chat_id, "❌ Спочатку увійди через /start")
        return

    user = session["user"]
    subs = Subscription.objects.filter(user=user)
    if not subs.exists():
        bot.send_message(chat_id, "📭 У тебе немає підписок")
        return

    for sub in subs:
        kb = InlineKeyboardMarkup()
        kb.row(
            InlineKeyboardButton("Редагувати", callback_data=f"edit_{sub.id}"),
            InlineKeyboardButton("Видалити", callback_data=f"delete_{sub.id}"),
            InlineKeyboardButton("Сплачено", callback_data=f"paid_{sub.id}")
        )
        bot.send_message(
            chat_id,
            f"🔹 *{sub.service_name}*\n💰 {sub.price} {sub.currency} / {sub.billing_cycle}\n📅 Наступний платіж: {sub.next_payment_date}\n📌 Статус: {sub.status}",
            reply_markup=kb,
            parse_mode="Markdown"
        )

# ------------------------------
# Callback кнопок
# ------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        action, sub_id = call.data.split("_")
        sub_id = int(sub_id)
        sub = Subscription.objects.get(id=sub_id)
        chat_id = call.message.chat.id

        # перевірка, чи підписка належить користувачу
        user = user_sessions.get(chat_id, {}).get("user")
        if not user or sub.user != user:
            bot.answer_callback_query(call.id, "❌ Ця підписка тобі не належить")
            return

        if action == "delete":
            sub.delete()
            bot.edit_message_text("✅ Підписку видалено", chat_id=chat_id, message_id=call.message.message_id)
        elif action == "paid":
            sub.mark_paid()
            bot.edit_message_text(
                f"💰 Оплату зараховано. Наступний платіж: {sub.next_payment_date}",
                chat_id=chat_id,
                message_id=call.message.message_id
            )
        elif action == "edit":
            bot.answer_callback_query(call.id, "Редагування скоро буде")
    except Exception as e:
        bot.answer_callback_query(call.id, f"Помилка: {str(e)}")

# ------------------------------
# Запуск бота
# ------------------------------
bot.polling(none_stop=True)
