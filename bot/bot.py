import os
import logging
from telegram import Update, Document
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from app.database import save_table_from_html, init_db

TOKEN = os.getenv("7831735814:AAGTbpWdukE0tXLuCD6P74dcoI0dau1HYHk")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Роза ДАТАБЕЙС: Пришли HTML-файл со списком служащих")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document
    if document.mime_type == "text/html":
        file = await document.get_file()
        content = await file.download_as_bytearray()
        text = content.decode("utf-8")
        count = save_table_from_html(text)
        await update.message.reply_text(f"Сохранено {count} записей.")
    else:
        await update.message.reply_text("Прошу HTML-файл.")

def run_bot():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()