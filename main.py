import os
from telegram import Update, MessageEntity, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Just send me a message, photo, or video and my creator will reply soon.")

def forward_to_admin(update: Update, context: CallbackContext):
    user = update.message.from_user

    # Compose the prefix message to admin
    user_info = f"New message from @{user.username or user.first_name} (ID: {user.id}):"
    
    # Forward text
    if update.message.text:
        text = f"{user_info}\n\n{update.message.text}"
        context.bot.send_message(chat_id=ADMIN_ID, text=text)

    # Forward photos
    elif update.message.photo:
        # Get the highest resolution photo
        photo = update.message.photo[-1]
        caption = f"{user_info}\n\n{update.message.caption or ''}"
        context.bot.send_photo(chat_id=ADMIN_ID, photo=photo.file_id, caption=caption)

    # Forward videos
    elif update.message.video:
        caption = f"{user_info}\n\n{update.message.caption or ''}"
        context.bot.send_video(chat_id=ADMIN_ID, video=update.message.video.file_id, caption=caption)

    else:
        # Unsupported message types
        context.bot.send_message(chat_id=ADMIN_ID, text=f"{user_info}\n\n[Unsupported message type]")

def handle_admin_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text or ""
        try:
            user_id = int(original_text.split("ID: ")[1].split(")")[0])
        except (IndexError, ValueError):
            update.message.reply_text("Couldn't extract user ID. Make sure you're replying to the bot's forwarded message.")
            return

        # If admin reply contains photo(s)
        if update.message.photo:
            photo = update.message.photo[-1]
            caption = update.message.caption or ""
            context.bot.send_photo(chat_id=user_id, photo=photo.file_id, caption=caption)

        # If admin reply contains video
        elif update.message.video:
            caption = update.message.caption or ""
            context.bot.send_video(chat_id=user_id, video=update.message.video.file_id, caption=caption)

        # If admin reply is text
        elif update.message.text:
            context.bot.send_message(chat_id=user_id, text=update.message.text)

        else:
            update.message.reply_text("Unsupported reply type. Please send text, photo, or video.")

    else:
        update.message.reply_text("Reply to a user's message to respond.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.private & Filters.reply, handle_admin_reply))
    dp.add_handler(MessageHandler(Filters.private & ~Filters.command, forward_to_admin))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
