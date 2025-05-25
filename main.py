from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import logging

# Logging (optional but useful)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a photo, and I'll reply. You can also use /photo to get one.")

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://via.placeholder.com/300.png?text=Hello+from+Bot"
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="Here's a picture!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.photo[-1].file_id
    await update.message.reply_text("Nice photo! Here's your image again:")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_id)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo or type /photo!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("photo", send_photo))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
