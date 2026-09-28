from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os
from datetime import datetime
from dotenv import load_dotenv
from news_api import get_top_news
from temperature_api import get_temp

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# Заглушки API
# =========================

def get_kyiv_temperature():
    temp = get_temp()
    return f"Температура у Києві: {int(temp)}°C"


def get_latest_news():
    """
    Наприклад: NewsAPI або RSS.
    """
    return get_top_news()


# =========================
# Обробники
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я простий інформаційний бот.\n\n"
        "Можеш запитати:\n"
        "• котра година\n"
        "• температура у Києві\n"
        "• останні новини"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # -------------------------
    # Котра година
    # -------------------------
    if "котра година" in text or "яка година" in text:
        current_time = datetime.now().strftime("%H:%M")

        await update.message.reply_text(
            f"Зараз {current_time}"
        )

    # -------------------------
    # Температура
    # -------------------------
    elif "температура" in text or "погода" in text:
        temperature = get_kyiv_temperature()

        await update.message.reply_text(
            f"🌡 {temperature}"
        )

    # -------------------------
    # Новини
    # -------------------------
    elif "новини" in text:
        news = get_latest_news()

        response = "📰 Останні новини:\n\n"

        for i, item in enumerate(news, start=1):
            response += f"{i}. {item}\n"

        await update.message.reply_text(response)

    # -------------------------
    # Невідоме питання
    # -------------------------
    else:
        await update.message.reply_text(
            "Не знаю, як відповісти 😕\n\n"
            "Спробуй запитати:\n"
            "• котра година\n"
            "• температура у Києві\n"
            "• останні новини"
        )


# =========================
# Запуск бота
# =========================

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot started...")

    application.run_polling()


if __name__ == "__main__":
    main()
