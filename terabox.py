import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://teradl-api.vercel.app/api"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a TeraBox link.")


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("⏳ Processing TeraBox Link...")

    try:

        r = requests.get(API, params={"url": url}, timeout=30)

        if r.status_code != 200:
            raise Exception("API server error")

        data = r.json()

        video_url = None

        # different possible response formats
        if isinstance(data, dict):

            if "video" in data and len(data["video"]) > 0:
                video_url = data["video"][0].get("url")

            elif "download" in data:
                video_url = data["download"]

            elif "url" in data:
                video_url = data["url"]

        if not video_url:
            raise Exception("Download link not found")

        await update.message.reply_text("📤 Uploading video...")

        await update.message.reply_video(video=video_url)

    except Exception as e:

        await update.message.reply_text(f"❌ Error: {str(e)}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Started")

app.run_polling()
