import json
import requests
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        url = f'https://api.apilayer.com/fixer/convert?to={quote_ticker}&from={base_ticker}&amount=1'

        payload = {}
        headers = {
            "apikey": "43NYwv74alzM8CqJl5k2eEnWmvN5sdtd"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.text
        total_base = json.loads(result)['result']
        return total_base

