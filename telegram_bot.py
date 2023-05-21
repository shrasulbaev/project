import telegram
from django.conf import settings


def send_message_to_telegram(message):
    # Создайте экземпляр бота, используя токен
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    # Отправьте сообщение в группу или канал бота
    bot.send_message(chat_id="@SHA-Лавка", text=message)


