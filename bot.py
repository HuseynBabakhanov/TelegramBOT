from dotenv import load_dotenv
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Load environment variables
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Persistent Reply Keyboard Menu
MAIN_MENU_KEYBOARD = [
    ["🐾 Small Hunt (2h)", "🦌 Big Hunt (8h)"],
    ["⏹ Stop Timers"]
]
MAIN_MENU = ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True)

# Notifications for timers
async def small_hunt(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="🐾 Time's up! Let's go smallHUNT!")
    context.job_queue.run_once(small_hunt, when=2 * 3600, data={'chat_id': chat_id})

async def big_hunt(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="🦌 Time's up! Let's go bigHUNT!")
    context.job_queue.run_once(big_hunt, when=8 * 3600, data={'chat_id': chat_id})

# Handlers for actions
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if text == "🐾 Small Hunt (2h)":
        context.job_queue.run_once(small_hunt, when=2 * 3600, data={'chat_id': chat_id})
        await update.message.reply_text("Small Hunt timer set for 2 hours! 🐾", reply_markup=MAIN_MENU)
    elif text == "🦌 Big Hunt (8h)":
        context.job_queue.run_once(big_hunt, when=8 * 3600, data={'chat_id': chat_id})
        await update.message.reply_text("Big Hunt timer set for 8 hours! 🦌", reply_markup=MAIN_MENU)
    elif text == "⏹ Stop Timers":
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in current_jobs:
            job.schedule_removal()
        await update.message.reply_text("All active timers have been stopped! ⏹", reply_markup=MAIN_MENU)
    else:
        await update.message.reply_text("Unknown command. Please use the menu buttons.", reply_markup=MAIN_MENU)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # When a user starts the bot, send the menu automatically
    await update.message.reply_text(
        "Hi! Let's go HUNT!\nChoose an option from the menu below:",
        reply_markup=MAIN_MENU
    )

    # Optionally, you can log the start event
    logger.info(f"User {update.effective_user.id} started the bot")

# Main function
def main():
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
