import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set your bot token and your Telegram user ID (admin)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # Your personal Telegram ID

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Just send me a message and my creator will reply soon.")

# When a user sends a message
def handle_user_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    msg = f"New message from @{user.username or user.first_name} (ID: {user.id}):\n\n{update.message.text}"
    context.bot.send_message(chat_id=ADMIN_ID, text=msg)

# When admin replies
def handle_admin_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        # Extract user ID from the original message
        original_text = update.message.reply_to_message.text
        try:
            user_id = int(original_text.split("ID: ")[1].split(")")[0])
            context.bot.send_message(chat_id=user_id, text=update.message.text)
        except:
            update.message.reply_text("Couldn't extract user ID. Make sure you're replying to the bot's forwarded message.")
    else:
        update.message.reply_text("Reply to a user's message to respond.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.private & Filters.reply, handle_admin_reply))
    dp.add_handler(MessageHandler(Filters.private & ~Filters.command, handle_user_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
