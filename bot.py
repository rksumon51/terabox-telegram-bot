import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from terabox import get_download_link
import requests

BOT_TOKEN = os.getenv("7999779554:AAH946UyAN9X2srGF3zO0q_2Z6He0zm3aaM")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Processing TeraBox Link...")

    try:
        link = get_download_link(url)

        await update.message.reply_text("📥 Downloading file...")

        file = requests.get(link)

        with open("video.mp4", "wb") as f:
            f.write(file.content)

        await update.message.reply_video(video=open("video.mp4", "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Started")

app.run_polling()
