import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)
# @CurrencyConverter_SF_bot

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы конвертировать интересующую валюту, '
            'введите данные в формате: \n'
            'имя валюты, цену которой хотите узнать, \n'
            'имя валюты, в которой надо узнать цену первой валюты, \n'
            'количество первой валюты.\n'
            'Узнать список доступных валют:  /values.')
    bot.reply_to(message, text)


flags = {
    'USD': '🇺🇸',
    'EUR': '🇪🇺',
    'RUB': '🇷🇺',
    'GBP': '🇬🇧',
    'CNY': '🇨🇳',
    'JPY': '🇯🇵',
    'CHF': '🇨🇭',
    'SEK': '🇸🇪'
}


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Конвертация доступна в:'
    for key in keys.keys():
        flag = flags.get(keys[key], '')
        text = '\n'.join((text, f'{flag} {key}'))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = values
        converter = CurrencyConverter()
        total_base = converter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {total_base:.2f} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()  # запуск бота