import telebot

import settings
from app.dictionary import Translation, Interpretation

bot = telebot.TeleBot(settings.TOKEN)


def text_format(dictionary):
    part = '*[Word] {title}\n[Part of speech] {label}\n[Transcription] {transcription}*\n'.format(**dictionary)
    descriptions = []
    for description in dictionary.get('description', []):
        if len(description) + len(part) < 4096:
            part += description
            if description is dictionary.get('description')[-1]:
                descriptions.append(part)
        else:
            descriptions.append(part)
            part = description
    return descriptions


@bot.message_handler(commands=['dict', 'tr'])
def interpretation_word(message):
    word_list = message.text.split()
    if len(word_list) == 1:
        bot.send_message(message.chat.id, 'Вы не указали слово')
    elif len(word_list) > 2:
        bot.send_message(message.chat.id, 'Должно быть одно слово')
    else:
        choice, word = word_list
        if choice == '/dict':
            dictionary = Interpretation.get_dict(word)
        else:
            dictionary = Translation.get_dict(word)

        if dictionary:
            txt = text_format(dictionary)
            for part in txt:
                bot.send_message(message.chat.id, part, parse_mode='Markdown')
            if dictionary.get('audio'):
                bot.send_audio(message.chat.id, dictionary.get('audio'))
        else:
            bot.send_message(message.chat.id, 'Нет такого слова.')


bot.polling()
