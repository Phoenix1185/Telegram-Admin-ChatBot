import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(BOT_TOKEN)

# When a user sends a message
def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_msg = update.message.text

    # Forward user message to admin
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"From @{user.username or user.first_name} (ID: {user.id}):\n{user_msg}"
    )

    # Confirm to user
    update.message.reply_text("Message sent to admin.")

# When admin replies
def handle_admin_reply(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return

    reply_to = update.message.reply_to_message
    if not reply_to:
        update.message.reply_text("Reply to a user message to respond.")
        return

    # Extract user ID from original message
    try:
        text = reply_to.text
        target_id = int(text.split("ID: ")[1].split("):")[0])
        context.bot.send_message(chat_id=target_id, text=update.message.text)
        update.message.reply_text("Reply sent.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send your message and the admin will reply soon.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.reply & Filters.text, handle_admin_reply))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
