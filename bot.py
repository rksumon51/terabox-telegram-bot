import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Terabox API
API = "https://api-production-359d.up.railway.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send a Terabox link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text
    await update.message.reply_text("⏳ Processing...")

    try:

        # Step 1: Get file info
        r = requests.post(f"{API}/generate_file", json={"url": url})
        data = r.json()

        if data["status"] != "success":
            await update.message.reply_text("❌ Failed to read link")
            return

        file = data["list"][0]

        payload = {
            "shareid": data["shareid"],
            "uk": data["uk"],
            "sign": data["sign"],
            "timestamp": data["timestamp"],
            "fs_id": file["fs_id"]
        }

        # Step 2: Generate download link
        r2 = requests.post(f"{API}/generate_link", json=payload)
        link_data = r2.json()

        if link_data["status"] != "success":
            await update.message.reply_text("❌ Failed to generate link")
            return

        download_link = link_data["download_link"]

        await update.message.reply_text("📤 Uploading video...")
        await update.message.reply_video(video=download_link)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🤖 Bot Started")

app.run_polling()
