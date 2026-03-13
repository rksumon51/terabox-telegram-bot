import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# TeraDL API
API = "https://teradl-api.vercel.app/api"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a TeraBox link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("⏳ Processing TeraBox Link...")

    try:

        r = requests.get(API, params={"url": url})
        data = r.json()

        video = data["video"][0]["url"]

        await update.message.reply_text("📤 Uploading video...")

        await update.message.reply_video(video=video)

    except Exception as e:

        await update.message.reply_text(f"❌ Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Started")

app.run_polling()
