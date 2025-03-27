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
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ["Заказать эдит", "Купить проект"],
        ["Отзывы", "Портфолио"]
    ]
    await update.message.reply_text(
        "Привет! Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
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

async def run_bot():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        if os.getenv("RENDER"):
            print("🚀 Запуск в режиме webhook")
            await application.bot.set_webhook(
                url=WEBHOOK_URL,
                secret_token=WEBHOOK_SECRET,
                drop_pending_updates=True
            )
            await application.run_webhook(
                listen="0.0.0.0",
                port=int(os.getenv("PORT", 10000)),
                webhook_url=WEBHOOK_URL,
                secret_token=WEBHOOK_SECRET
            )
        else:
            print("🔄 Запуск в режиме polling")
            await application.run_polling()
            
    except asyncio.CancelledError:
        print("🔌 Получен сигнал завершения")
    except Exception as e:
        print(f"⚠️ Ошибка: {type(e).__name__}: {e}")
    finally:
        if application.running:
            print("⏹️ Завершение работы...")
            await application.stop()
            await application.shutdown()
        print("✅ Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n👋 Ручное завершение")
