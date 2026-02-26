import telebot
import os
from flask import Flask, request

TOKEN = os.environ.get("8733511425:AAHa7r-CyEbyinRchPF6hM7NHR3EUflwXDY")
ADMIN_ID = 5156518018  # آیدی عددی خودت

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_user(message):
    user_id = message.reply_to_message.forward_from.id
    bot.send_message(user_id, message.text)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    bot.remove_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))