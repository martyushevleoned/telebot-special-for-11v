import telebot  # pip3 install PyTelegramBotAPI
from config import TOKEN, EDITORS, BLACK_LIST, func, sub_key, day_key

messages = {
    '/timetable': 'func.timetable_out()',
    '/schedule': 'func.schedule_out()',
    '/tomorrow': 'func.tomorrow_hw_out()',
    '/all_hw': 'func.all_hw_out()',
}

commands = {
    '/day_hw': 'bot.send_message(m.chat.id, "выберите день", reply_markup=day_key)',
    '/start': 'bot.send_message(m.chat.id, "нажмите /")'
}

debug = {
    '/reset': 'reset()',
    '/stats': 'bot.send_message(m.chat.id, func.stats())'
}

current_chat = 0
current_lesson = ''
waiter = False


def reset():
    global current_chat, waiter, current_lesson
    current_chat = 0
    current_lesson = ''
    waiter = False


def listener(m):
    for msg in m:
        if msg.content_type == 'text':
            with open('messages.txt', 'a') as mess:
                mess.write(
                    str(msg.chat.id) + ' ' + msg.chat.first_name + ': ' + msg.text.replace('\n', ' <3 ') + '\n')
                mess.close()


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


@bot.message_handler(commands=['add_hw'])
def start_message(m):
    global current_chat
    if m.chat.id in EDITORS:
        if current_chat == 0:
            current_chat = m.chat.id
            bot.send_message(m.chat.id, 'выберите предмет', reply_markup=sub_key)
        else:
            bot.send_message(m.chat.id, 'подожди пару минут')
    else:
        bot.send_message(m.chat.id, 'недостаточно прав доступа')


@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
    # day hw
    for i in range(6):
        if call.data == str(i):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=func.day_hw_out(i),
                reply_markup=None,
                parse_mode='Markdown')

    # exit from admin mod
    if call.data == 'exit':
        reset()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='выход',
            reply_markup=None,
            parse_mode='Markdown')

    # choose subject
    elif call.data in func.sub:

        global current_chat, current_lesson, waiter

        if call.message.chat.id == current_chat:
            current_lesson = call.data
            waiter = True
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=call.data + '\n' + 'текущее дз:' + '\n' + func.hw[current_lesson] + '\nвведите дз:',
                reply_markup=None,
                parse_mode='Markdown')

        # protect
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='nope',
                reply_markup=None,
                parse_mode='Markdown')


# text
@bot.message_handler(content_types=['text'])
def send_text(m):
    if m.chat.id in BLACK_LIST:
        bot.send_message(m.chat.id, 'тебе здесь не рады')

    elif m.chat.id == current_chat and waiter is True:
        func.hw[current_lesson] = m.text
        func.save()
        bot.send_message(m.chat.id, 'дз сохранено')
        reset()

    elif m.text in messages.keys():
        bot.send_message(m.chat.id, eval(messages[m.text]))

    elif m.text in commands:
        eval(commands[m.text])

    elif m.text in debug and m.chat.id in EDITORS:
        eval(debug[m.text])
        bot.send_message(m.chat.id, 'что бы ты ни делал, я это сделал')

    else:
        bot.send_message(m.chat.id, 'я не понял, что ты написал')


func.load()
bot.polling(none_stop=True)
