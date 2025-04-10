from telegram.ext import Updater, CommandHandler
import os

TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("Welcome to Spinwin Bot!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
