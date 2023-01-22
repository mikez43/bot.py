import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, 'Чтобы начать работу введите команду боту в следующем формате: \
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\
Увидеть весь список валют: /values')

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Для конвертации необходимо 3 параметра')

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {base} - {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)