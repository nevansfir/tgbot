# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен теперь берется из переменных окружения

async def start(update, context):
    buttons = [
        ["Заказать эдит", "Купить проект"],
        ["Отзывы"],
        ["Портфолио"]
    ]
    await update.message.reply_text(
        "Привет! Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def handle_message(update, context):
    text = update.message.text
    if text == "Портфолио":
        await update.message.reply_text("Мои работы: [ссылка на портфолио]")
    elif text == "Заказать эдит":
        await update.message.reply_text("Опишите, какой эдит вам нужен:")
    elif text == "Купить проект":
        await update.message.reply_text("Доступные проекты: [ссылка на каталог]")
    elif text == "Отзывы":
        await update.message.reply_text("Отзывы клиентов: [ссылка на отзывы]")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Настройка webhook для Render.com (порт 10000)
    RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        PORT = 10000
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"https://{RENDER_EXTERNAL_HOSTNAME}/{TOKEN}"
        )
    else:
        # Локальный режим (polling) для отладки
        application.run_polling()

if __name__ == "__main__":
    main()
