import telebot
import json
import os

# 🔐 আপনার Token এখানে বসানো হয়েছে
TOKEN = "7963805480:AAGFdQJqW6apdUjhCuxE9bENW5lNl_7MKeE"
bot = telebot.TeleBot(TOKEN)

# 👑 Owner ID
OWNER_ID = 5132461928

DATA_FILE = "numbers.json"

# ফাইল থেকে ডাটা লোড
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# ফাইলে ডাটা সেভ
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Get Number")
    bot.send_message(message.chat.id, "👋 Welcome! Click 'Get Number' to receive a number.", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Get Number")
def get_number(message):
    data = load_data()
    if not data:
        bot.send_message(message.chat.id, "❌ No numbers available yet.")
        return
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for country in data.keys():
        markup.add(country)
    bot.send_message(message.chat.id, "🌍 Select a country:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in load_data().keys())
def send_number(message):
    data = load_data()
    country = message.text
    number = data.get(country)
    if number:
        bot.send_message(message.chat.id, f"📞 {country}: {number}")
    else:
        bot.send_message(message.chat.id, "❌ Number not found.")

# ✅ Owner-only check
def is_owner(message):
    return message.from_user.id == OWNER_ID

@bot.message_handler(commands=['add'])
def add_number(message):
    if not is_owner(message):
        return bot.reply_to(message, "❌ You are not allowed to use this command.")
    
    try:
        _, country, number = message.text.split(" ", 2)
        data = load_data()
        data[country] = number
        save_data(data)
        bot.reply_to(message, f"✅ Added: {country} → {number}")
    except:
        bot.reply_to(message, "⚠️ Usage: /add Country Number")

@bot.message_handler(commands=['del'])
def delete_number(message):
    if not is_owner(message):
        return bot.reply_to(message, "❌ You are not allowed to use this command.")
    
    try:
        _, country = message.text.split(" ", 1)
        data = load_data()
        if country in data:
            del data[country]
            save_data(data)
            bot.reply_to(message, f"🗑 Deleted: {country}")
        else:
            bot.reply_to(message, "❌ Country not found.")
    except:
        bot.reply_to(message, "⚠️ Usage: /del Country")

@bot.message_handler(commands=['list'])
def list_numbers(message):
    if not is_owner(message):
        return bot.reply_to(message, "❌ You are not allowed to use this command.")
    
    data = load_data()
    if not data:
        bot.reply_to(message, "❌ No numbers available.")
        return
    msg = "\n".join([f"{c} → {n}" for c, n in data.items()])
    bot.reply_to(message, f"📋 Number List:\n{msg}")

print("🤖 Bot is running...")
bot.polling()