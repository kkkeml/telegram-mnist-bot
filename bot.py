from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

model = load_model("mnist_cnn_model.h5")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне изображение с цифрой, и я её распознаю.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_path = "received_digit.jpg"
    await file.download_to_drive(image_path)

    try:
        img = Image.open(image_path).convert("L").resize((28, 28))
        img_array = np.array(img)
        img_array = 255 - img_array  # инвертируем
        img_array = img_array / 255.0
        img_array = img_array.reshape(1, 28, 28, 1)

        prediction = model.predict(img_array)
        predicted_digit = int(np.argmax(prediction))
        await update.message.reply_text(f"Я думаю, это цифра: {predicted_digit}")
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке изображения.")
        print(e)
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

def main():
    application = ApplicationBuilder().token("ВАШ ТОКЕН").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()

if __name__ == '__main__':
    main()

