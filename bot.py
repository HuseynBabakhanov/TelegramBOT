from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Notification for 2 hours (Small Hunt)
async def small_hunt(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="Let's go smallHUNT!")

# Notification for 8 hours (Big Hunt)
async def big_hunt(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="Let's go bigHUNT!")

# Command to start small hunt (2 hours) timer
async def small_hunt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if context.job_queue is not None:
        # Schedule the task to run in 2 hours
        context.job_queue.run_once(small_hunt, when=2 * 3600, data={'chat_id': chat_id})
        await update.message.reply_text("You're done! I'll notify you when the smallHUNT is ready.")

# Command to start big hunt (8 hours) timer
async def big_hunt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if context.job_queue is not None:
        # Schedule the task to run in 8 hours
        context.job_queue.run_once(big_hunt, when=8 * 3600, data={'chat_id': chat_id})
        await update.message.reply_text("You're done! I'll notify you when the bigHUNT is ready.")

# Start command to welcome the user and show available commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, Let's go HUNT!\nUse commands:\n"
        "/small_hunt - Go SmallHunt (2 hours)\n"
        "/big_hunt - Go BigHunt (8 hours)"
    )

def main():
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("small_hunt", small_hunt_command))
    application.add_handler(CommandHandler("big_hunt", big_hunt_command))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
