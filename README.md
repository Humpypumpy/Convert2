# Telegram Image Converter Bot

This is a Telegram bot to convert images between formats like PNG, JPEG, WebP, BMP.

### 🚀 Deploy on Render

1. Go to [Render](https://render.com) and login.
2. Click **New → Web Service**
3. Connect your GitHub or upload this zip.
4. Fill in:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Environment Variable**: `BOT_TOKEN=<your-telegram-bot-token>`
5. Deploy. Done ✅

It creates a `downloads/` folder automatically for temporary files.