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

async def check_secret_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверка секретного токена вебхука"""
    if not WEBHOOK_SECRET:
        return True
        
    secret_header = update.effective_message.webhook_data.get('secret') if update.effective_message else None
    return secret_header == WEBHOOK_SECRET

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_secret_token(update, context):
        return
        
    buttons = [
        ["Заказать эдит", "Купить проект"],
        ["Отзывы", "Портфолио"]
    ]
    await update.message.reply_text(
        "Привет! Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_secret_token(update, context):
        return

    text = update.message.text
    if text == "Портфолио":
        await update.message.reply_text("Мои работы: [ссылка на портфолио]")
    elif text == "Заказать эдит":
        await update.message.reply_text("Опишите, какой эдит вам нужен:")
    elif text == "Купить проект":
        await update.message.reply_text("Доступные проекты: [ссылка на каталог]")
    elif text == "Отзывы":
        await update.message.reply_text("Отзывы клиентов: [ссылка на отзывы]")

async def setup_webhook(app: Application):
    """Настройка вебхука с секретным токеном"""
    await app.bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

async def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        print("🚀 Инициализация бота...")
        await application.initialize()
        
        if os.getenv("RENDER"):
            print("🌐 Режим: Webhook")
            await setup_webhook(application)
            await application.run_webhook(
                listen="0.0.0.0",
                port=int(os.getenv("PORT", 10000)),
                secret_token=WEBHOOK_SECRET,
                webhook_url=WEBHOOK_URL
            )
        else:
            print("🔄 Режим: Polling")
            await application.run_polling()
            
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    finally:
        if application.running:
            print("⏹️ Остановка бота...")
            await application.stop()
            await application.shutdown()
        print("✅ Бот завершил работу")

if __name__ == "__main__":
    asyncio.run(main())
