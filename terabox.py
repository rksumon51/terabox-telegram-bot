import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

API = "https://api-production-359d.up.railway.app/api?url="


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("⏳ Processing TeraBox Link...")

    try:
        r = requests.get(API + url)
        data = r.json()

        video = data["video"]

        await update.message.reply_text("📥 Downloading Video...")

        file = requests.get(video)

        with open("video.mp4", "wb") as f:
            f.write(file.content)

        await update.message.reply_video(video=open("video.mp4", "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Started")

app.run_polling()
