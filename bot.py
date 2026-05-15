from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import easyocr
import requests

API_URL = "PASTE_URL_HERE"

reader = easyocr.Reader(['en','ru'])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("img.jpg")

    result = reader.readtext("img.jpg", detail=0)

    teachers = []
    subjects = []

    for line in result:
        if "math" in line.lower() or "ֆիզ" in line.lower():
            subjects.append(line)
        else:
            teachers.append(line)

    requests.post(API_URL, json={
        "teachers": teachers,
        "subjects": subjects
    })

    await update.message.reply_text("Ավելացվեց ✅")

app = ApplicationBuilder().token("PASTE_TOKEN").build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
