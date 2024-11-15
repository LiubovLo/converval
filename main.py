import telebot
from config import TOKEN, API_KEY
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Доступные валюты
CURRENCIES = {
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB",
}


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message: telebot.types.Message):
    """Отправляет инструкции по использованию бота."""
    text = (
        "Добро пожаловать! Чтобы узнать цену на валюту, отправьте сообщение в формате:\n"
        "<имя валюты> <имя валюты для конвертации> <количество>\n"
        "Например: евро доллар 100\n\n"
        "Команды:\n"
        "/start или /help - Показать это сообщение\n"
        "/values - Показать список доступных валют"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    """Выводит список доступных валют."""
    text = "Доступные валюты:\n" + "\n".join(CURRENCIES.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    """Обрабатывает запрос на конвертацию валют."""
    try:
        values = message.text.lower().split()
        if len(values) != 3:
            raise APIException(
                "Неверное количество параметров. Формат: <валюта> <валюта для конвертации> <количество>.")

        base_name, quote_name, amount = values
        base = CURRENCIES.get(base_name)
        quote = CURRENCIES.get(quote_name)

        if not base:
            raise APIException(f"Неизвестная валюта: {base_name}.")
        if not quote:
            raise APIException(f"Неизвестная валюта: {quote_name}.")

        total_amount = CurrencyConverter.get_price(base, quote, amount, API_KEY)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {e}")
    else:
        text = f"Цена {amount} {base_name} в {quote_name} составляет {total_amount}"
        bot.reply_to(message, text)


bot.polling(none_stop=True)

