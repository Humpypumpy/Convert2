import os
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from convert import convert_image
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
app = Flask(__name__)

@app.route("/")
def home():
    return "Image Converter Bot is running."

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    os.makedirs("downloads", exist_ok=True)
    input_path = f"downloads/{message.document.file_name}"
    await bot.download_file(file.file_path, input_path)

    keyboard = InlineKeyboardMarkup()
    for fmt in ['png', 'jpeg', 'webp', 'bmp']:
        keyboard.add(InlineKeyboardButton(fmt.upper(), callback_data=f"{input_path}|{fmt}"))
    await message.answer("Choose the format to convert to:", reply_markup=keyboard)

@dp.callback_query_handler()
async def convert_handler(callback: types.CallbackQuery):
    input_path, output_format = callback.data.split('|')
    output_path = convert_image(input_path, output_format)

    with open(output_path, "rb") as file:
        await bot.send_document(callback.message.chat.id, file)

    os.remove(input_path)
    os.remove(output_path)

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def run_bot():
    executor.start_polling(dp)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
