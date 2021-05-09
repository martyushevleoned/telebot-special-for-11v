import telebot  # pip3 install PyTelegramBotAPI
from config import TOKEN, EDITORS, BLACK_LIST, Func, Keyboard

messages = {
    '/timetable': 'Func.timetable_out()',
    '/schedule': 'Func.schedule_out()',
    '/tomorrow': 'Func.tomorrow_hw_out()',
    '/all_hw': 'Func.all_hw_out()',
}

commands = {
    '/day_hw': 'bot.send_message(m.chat.id, "выберите день", reply_markup=Keyboard.day_key)',
    '/start': 'bot.send_message(m.chat.id, "халоу")'
}

bot = telebot.TeleBot(TOKEN)
current_chat = 0
current_lesson = ''
waiter = False


def reset():
    global current_chat, waiter, current_lesson
    current_chat = 0
    current_lesson = ''
    waiter = False


@bot.message_handler(commands=['add_hw'])
def start_message(m):
    global current_chat
    if m.chat.id in EDITORS:
        if current_chat == 0:
            current_chat = m.chat.id
            bot.send_message(m.chat.id, 'выберите предмет', reply_markup=Keyboard.sub_key)
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
                text=Func.day_hw_out(i),
                reply_markup=None,
                parse_mode='Markdown')

    # exit from admin mod
    global current_chat, current_lesson, waiter

    if call.data == 'exit':
        if call.message.chat.id == current_chat:
            reset()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='выход',
                reply_markup=None,
                parse_mode='Markdown')
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='nope',
                reply_markup=None,
                parse_mode='Markdown')

    # choose subject
    elif call.data in Func.sub:
        if call.message.chat.id == current_chat:
            current_lesson = call.data
            waiter = True
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=call.data + '\n' + 'текущее дз:' + '\n' + Func.hw[current_lesson] + '\nвведите дз:',
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


@bot.message_handler(content_types=['text'])
def send_text(m):
    if m.from_user.is_bot is False:

        m.text = m.text.replace('@special_for_11v_telebot', '')
        bot.send_message(-385288047, m.from_user.first_name + '\n' + str(m.chat.id) + '\n' + m.text)

        if m.chat.id in BLACK_LIST:
            bot.send_message(m.chat.id, 'тебе здесь не рады')

        elif m.chat.id == current_chat and waiter is True:
            Func.hw[current_lesson] = m.text
            bot.send_message(m.chat.id, 'дз сохранено')
            bot.send_message(-373136347, Func.download_hw())
            reset()

        elif m.text in messages.keys():
            bot.send_message(m.chat.id, eval(messages[m.text]))

        elif m.text in commands:
            eval(commands[m.text])

        elif m.chat.id in EDITORS:
            if m.text == '/reset':
                reset()
                bot.send_message(m.chat.id, 'success')

            elif m.text == '/download_hw':
                bot.send_message(m.chat.id, Func.download_hw())

            elif '/upload_hw' in m.text:
                Func.upload_hw(m.text)
                bot.send_message(m.chat.id, Func.all_hw_out())

            else:
                bot.send_message(m.chat.id, 'я не понял, что ты написал')

        else:
            bot.send_message(m.chat.id, 'я не понял, что ты написал')


bot.polling(none_stop=True)
