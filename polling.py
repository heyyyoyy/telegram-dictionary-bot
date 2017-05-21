import telebot
import settings
from dictionary import Translate, Interpretation

bot = telebot.TeleBot(settings.TOKEN)


def text_interpretation(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = ''.join(map(lambda msg: '\[Description] {}\n'
                                    '\[Examples] {}\n'.format(msg[0], msg[1]), dictionary['descr']))
    if descr == '':
        return string
    return '{}{}'.format(string, descr)


def text_translate(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = ''.join(map(lambda msg: '\[Description] {}\n'
                                    '\[Translate] {}\n'
                                    '\[Examples] {}\n'.format(msg[0], msg[1], msg[2]), dictionary['descr']))
    if descr == '':
        return string
    return '{}{}'.format(string, descr)


@bot.message_handler(commands=['dict'])
def interpretation_word(message):
    dictionary = Interpretation.get_dict(message.text)
    if dictionary:
        txt = text_interpretation(dictionary)
        if len(txt) > 4096:
            offset = 0
            count = 4096
            for _ in txt:
                bot.send_message(message.chat.id, txt[offset:count], parse_mode='Markdown')
                offset += 4096
                count += 4096
                if len(txt) - offset < 4096:
                    bot.send_message(message.chat.id, txt[offset:], parse_mode='Markdown')
                    break
        else:
            bot.send_message(message.chat.id, txt, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


@bot.message_handler(commands=['tr'])
def translate_word(message):
    dictionary = Translate.get_dict(message.text)
    if dictionary:
        txt = text_translate(dictionary)
        if len(txt) > 4096:
            offset = 0
            count = 4096
            for _ in txt:
                bot.send_message(message.chat.id, txt[offset:count], parse_mode='Markdown')
                offset += 4096
                count += 4096
                if len(txt) - offset < 4096:
                    bot.send_message(message.chat.id, txt[offset:], parse_mode='Markdown')
                    break
        else:
            bot.send_message(message.chat.id, txt, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


bot.polling()
