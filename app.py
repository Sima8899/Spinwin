import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# Hardcoded Config
TELEGRAM_TOKEN = "7808400054:AAGL0Jx3Q3j_hYw8k77C8pYW8yQ4HbBIkjc"
MERCHANT_ID = "34215172"
API_KEY = "b485e9b4ca554123a2705709a30a284f"

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

@app.route('/')
def home():
    return "Bot is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "ok"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /deposit to check your payment and get 5 spins.")

def deposit(update: Update, context: CallbackContext):
    qr_image = "https://i.ibb.co/bM6c4k3T/BHARATPE-QR-3.png"
    update.message.reply_photo(qr_image, caption="Send ₹50 to this BharatPe QR.\nThen wait 20 seconds, your payment will be verified automatically.")

    txn_id = "510100347135"
    url = "https://api.bharatpe.com/v1/transactions/verify"

    headers = {
        "apiKey": API_KEY,
        "Content-Type": "application/json"
    }

    params = {
        "merchantId": MERCHANT_ID,
        "transactionId": txn_id
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        if data.get("status") == "SUCCESS":
            update.message.reply_text("✅ Payment successful!\nYou got 5 spins.")
        else:
            update.message.reply_text("❌ Payment not found or pending. Try again in a few seconds.")
    except Exception as e:
        update.message.reply_text("Error verifying payment.")
        print(e)

from telegram.ext import Application, ApplicationBuilder

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
dp = application.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("deposit", deposit))
