import requests
import json


class APIException(Exception):
    """Исключение для обработки ошибок пользователя."""
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str, api_key: str):
        """Возвращает цену на указанное количество валюты."""
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество валюты должно быть числом.")

        if base.upper() == quote.upper():
            raise APIException("Нельзя переводить валюту саму в себя.")

        url = f"https://min-api.cryptocompare.com/data/price?fsym={base.upper()}&tsyms={quote.upper()}"
        headers = {"Authorization": f"Apikey {api_key}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise APIException(f"Ошибка API: {response.status_code}")

            data = response.json()
        except json.JSONDecodeError:
            raise APIException("Ошибка в формате ответа от API.")
        except Exception as e:
            raise APIException(f"Ошибка при обращении к API: {e}")

        if quote.upper() not in data:
            raise APIException("Указанная валюта недоступна для конвертации.")

        rate = data[quote.upper()]
        total = amount * rate
        return round(total, 2)
