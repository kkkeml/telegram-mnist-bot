from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне изображение с цифрой, и я её распознаю.")

def main():
    application = ApplicationBuilder().token("6453591442:AAGwVRFv8UA9gSwjoQaljT0I8XcsAT74gQA").build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == '__main__':
    main()
