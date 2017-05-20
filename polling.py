import telebot
import settings
from dictionary import Translate, Interpretation

bot = telebot.TeleBot(settings.TOKEN)
interpretation = Interpretation()
translate = Translate()


def text_interpr(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = ''.join(map(lambda msg: '[[Description]] {}\n'
                                    '[[Examples]] {}\n'.format(msg[0], msg[1]), dictionary['descr']))
    if descr == '':
        return string
    return '{}{}'.format(string, descr)


def text_translate(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = ''.join(map(lambda msg: '[[Description]] {}\n'
                                    '[[Translate]] {}\n'
                                    '[[Examples]] {}\n'.format(msg[0], msg[1], msg[2]), dictionary['descr']))
    if descr == '':
        return string
    return '{}{}'.format(string, descr)


@bot.message_handler(commands=['dict'])
def interpret_word(message):
    interpretation.set_word(message.text.split()[-1])
    response = interpretation.response(settings.URL_INT)
    if response != '':
        dictionary = interpretation.get_dict()
        txt = text_interpr(dictionary)
        bot.send_message(message.chat.id, txt, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


@bot.message_handler(commands=['tr'])
def translate_word(message):
    translate.set_word(message.text.split()[-1])
    response = translate.response(settings.URL_TRANSLATE)
    if response != '':
        dictionary = translate.get_dict()
        txt = text_translate(dictionary)
        bot.send_message(message.chat.id, txt, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


bot.polling()