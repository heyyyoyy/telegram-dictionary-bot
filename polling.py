import telebot
import settings
from dictionary import Translate, Interpretation

bot = telebot.TeleBot(settings.TOKEN)


def parts_of_interpretation(msg):
    list_descriptions = []
    part = ''
    for description in msg:
        if len(part) < 3800:
            part += '\[Description] {}\n\[Examples] {}\n'.format(description[0], description[1])
            if description is msg[-1]:
                list_descriptions.append(part)
        else:
            list_descriptions.append(part)
            part = '\[Description] {}\n\[Examples] {}\n'.format(description[0], description[1])
    return list_descriptions


def parts_of_translate(msg):
    list_descriptions = []
    part = ''
    for description in msg:
        if len(part) < 3800:
            part += '\[Description] {}\n''\[Translate] {}\n''\[Examples] {}\n'.format(description[0],
                                                                                      description[1],
                                                                                      description[2])
            if description is msg[-1]:
                list_descriptions.append(part)
        else:
            list_descriptions.append(part)
            part = '\[Description] {}\n''\[Translate] {}\n''\[Examples] {}\n'.format(description[0],
                                                                                     description[1],
                                                                                     description[2])
    return list_descriptions


def text_interpretation(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = parts_of_interpretation(dictionary['descr'])
    if descr == '':
        return string
    return string, descr


def text_translate(dictionary):
    string = '*[Word] {}*\n*[Part of speech] {}*\n*[Transcription] {}*\n'.format(
        dictionary['title'], dictionary['label'], dictionary['transcr']
    )
    descr = parts_of_translate(dictionary['descr'])
    if descr == '':
        return string
    return string, descr


@bot.message_handler(commands=['dict'])
def interpretation_word(message):
    dictionary = Interpretation.get_dict(message.text)
    if dictionary:
        main_txt, description = text_interpretation(dictionary)
        bot.send_message(message.chat.id, main_txt, parse_mode='Markdown')
        for desc in description:
            bot.send_message(message.chat.id, desc, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


@bot.message_handler(commands=['tr'])
def translate_word(message):
    dictionary = Translate.get_dict(message.text)
    if dictionary:
        main_txt, description = text_translate(dictionary)
        bot.send_message(message.chat.id, main_txt, parse_mode='Markdown')
        for desc in description:
            bot.send_message(message.chat.id, desc, parse_mode='Markdown')
        bot.send_audio(message.chat.id, dictionary['audio'])
    else:
        bot.send_message(message.chat.id, 'Нет такого слова.')


bot.polling()
