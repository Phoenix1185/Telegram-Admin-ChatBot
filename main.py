from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text("Welcome! Send me a photo, or use /photo to get one.")

def photo(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo="https://via.placeholder.com/300.png?text=Hello+from+Bot")

def handle_photo(update, context):
    file_id = update.message.photo[-1].file_id
    update.message.reply_text("Thanks for the photo! Here it is again:")
    context.bot.send_photo(chat_id=update.message.chat_id, photo=file_id)

def handle_text(update, context):
    update.message.reply_text("Send a photo or type /photo!")

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
