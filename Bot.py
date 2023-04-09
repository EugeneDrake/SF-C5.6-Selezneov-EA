import telebot
from config import TOKEN, keys
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = 'Привет! Для старта введите комманду боту в формате: <имя валюты> <в какую перевести> ' \
           '<количество переводимой валюты>. ' \
           ' При вводе дробного числа необходимо использовать точку вместо запятой. '\
           '\nУвидеть весь список доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException("Неподходящее количество параметров! Введите три параметра!"\
                               ' Инструкция по вводу /help')

        quote, base, amount = values
        total_base = Converter.get_price(quote.lower(), base.lower(), amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()