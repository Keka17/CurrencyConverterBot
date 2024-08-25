import requests
import json
from config import keys, api_key


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'невозможно перевести одинаковые валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать количество {amount}.')

        r = requests.get(f'https://api.exchangerate-api.com/v4/latest/{quote_ticker}',
                         headers={'apikey': api_key})
        total_base = json.loads(r.content)['rates'][base_ticker] * float(amount)

        return total_base

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            return CurrencyConverter.convert(quote, base, amount)
        except ConvertionException as e:
            raise ConvertionException(f'Тип ошибки: {e}')