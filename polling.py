import telebot
import settings
from dictionary import Translate, Interpretation

bot = telebot.TeleBot(settings.TOKEN)


def text_format(dictionary):
    part = '*[Word] {}\n[Part of speech] {}\n[Transcription]*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr'])
    descriptions = []
    for description in dictionary['descr']:
        if len(description)+len(part) < 4096:
            part += description
            if description is dictionary['descr'][-1]:
                descriptions.append(part)
        else:
            descriptions.append(part)
            part = description
    return descriptions


@bot.message_handler(commands=['dict', 'tr'])
def interpretation_word(message):
    dictionary = Interpretation.get_dict(message.text) \
        if message.text.split()[0] == '/dict' else Translate.get_dict(message.text)
    if dictionary:
        txt = text_format(dictionary)
        for part in txt:
            bot.send_message(message.chat.id, part, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


bot.polling()
