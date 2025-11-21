import os
import zipfile
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from repurpose import make_variations
from utils import download_video

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/tmp/output")
NUM_VARIATIONS = int(os.environ.get("NUM_VARIATIONS", "20"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    await msg.reply_text("⏳ Downloading...")

    try:
        video_path = await download_video(msg, OUTPUT_DIR)
    except Exception as e:
        await msg.reply_text(f"❌ Download failed: {e}")
        return

    await msg.reply_text("🎨 Making variations...")

    try:
        files = make_variations(video_path, num_variations=NUM_VARIATIONS, out_dir=OUTPUT_DIR)
    except Exception as e:
        await msg.reply_text(f"❌ Processing error: {e}")
        return

    zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for f in files:
            z.write(f, arcname=os.path.basename(f))

    await msg.reply_document(open(zip_path, "rb"))

    await msg.reply_text("✅ Done!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
