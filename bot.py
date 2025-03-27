# -*- coding: utf-8 -*-
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Клавиатуры
    main_keyboard = ReplyKeyboardMarkup([
        ["Заказать эдит", "Купить проект"],
        ["Отзывы", "Портфолио"]
    ], resize_keyboard=True)

    # Обработчики команд
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Выбери действие:",
            reply_markup=main_keyboard
        )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "Портфолио":
            await update.message.reply_text("Мои работы: [ссылка на портфолио]")
        elif text == "Заказать эдит":
            await update.message.reply_text("Опишите, какой эдит вам нужен:")
        elif text == "Купить проект":
            await update.message.reply_text("Доступные проекты: [ссылка на каталог]")
        elif text == "Отзывы":
            await update.message.reply_text("Отзывы клиентов: [ссылка на отзывы]")

    # Настройка обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        print("🚀 Запуск бота в режиме webhook...")
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(
            url="https://tgbot.onrender.com/webhook",
            secret_token=os.getenv("WEBHOOK_SECRET")
        )
        
        async with application:
            await application.run_webhook(
                listen="0.0.0.0",
                port=10000,
                webhook_url="https://tgbot.onrender.com/webhook",
                secret_token=os.getenv("WEBHOOK_SECRET")
            )
            
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    finally:
        print("⏹️ Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
