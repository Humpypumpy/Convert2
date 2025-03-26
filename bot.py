import os
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv
from convert import convert_image
from flask import Flask

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
app = Flask(__name__)
session_data = {}

@app.route("/")
def home():
    return "Image Converter Bot is running."

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    os.makedirs("downloads", exist_ok=True)
    input_path = f"downloads/{message.document.file_name}"
    await bot.download_file(file.file_path, input_path)
    session_data[message.chat.id] = {"input": input_path}

    keyboard = InlineKeyboardMarkup()
    for fmt in ['png', 'jpeg', 'webp', 'tiff', 'avif', 'ico', 'bmp']:
        keyboard.add(InlineKeyboardButton(fmt.upper(), callback_data=f"format:{fmt}"))
    await message.answer("Choose format to convert to:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("format:"))
async def handle_format(callback: types.CallbackQuery):
    fmt = callback.data.split(":")[1]
    session_data[callback.message.chat.id]["format"] = fmt

    keyboard = InlineKeyboardMarkup()
    for scale in ['25', '50', '75', '100']:
        keyboard.add(InlineKeyboardButton(f"{scale}%", callback_data=f"scale:{scale}"))
    await callback.message.answer("Resize image (scale):", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("scale:"))
async def handle_resize(callback: types.CallbackQuery):
    scale = int(callback.data.split(":")[1])
    session_data[callback.message.chat.id]["scale"] = scale

    keyboard = InlineKeyboardMarkup()
    for q in ['90', '70', '50']:
        keyboard.add(InlineKeyboardButton(f"{q}% Quality", callback_data=f"quality:{q}"))
    await callback.message.answer("Choose quality:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("quality:"))
async def handle_quality(callback: types.CallbackQuery):
    quality = int(callback.data.split(":")[1])
    data = session_data.pop(callback.message.chat.id)
    input_path = data["input"]
    fmt = data["format"]
    scale = data["scale"]

    output_path = convert_image(input_path, fmt, scale, quality)

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