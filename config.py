from telebot import types
from datetime import datetime

TOKEN = '1384356348:AAHvlCs2SFQCUepV5CsI6yqA5tk65pWSt7E'
EDITORS = [976798046, 1311758742, 413549520]
BLACK_LIST = [470540326]


class Func(object):
    # subjects
    sub = [
        'обж',  # 0
        'химия',  # 1
        'физика',  # 2
        'алгебра',  # 3
        'история',  # 4
        'география',  # 5
        'геометрия',  # 6
        'экономика',  # 7
        'литература',  # 8
        'физкультура',  # 9
        'русский язык',  # 10
        'информатика',  # 11
        'правоведение',  # 12
        'обществознание',  # 13
        'иностранный язык',  # 14
        'практикум по математике'  # 15
    ]

    # homework
    hw = dict.fromkeys(sub, '-')

    # schedule
    schedule = {
        'понедельник': [sub[0],
                        sub[14],
                        sub[3],
                        sub[3],
                        sub[2],
                        sub[7],
                        sub[12]],

        'вторник': [sub[15],
                    sub[15],
                    sub[2],
                    sub[1],
                    sub[8],
                    sub[10],
                    sub[9]],

        'среда': [sub[2],
                  sub[11],
                  sub[14],
                  sub[10],
                  sub[10],
                  sub[8],
                  sub[10]],

        'четверг': [sub[9],
                    sub[13],
                    sub[13],
                    sub[2],
                    sub[5],
                    sub[6],
                    sub[6]],

        'пятница': [sub[11],
                    sub[11],
                    sub[3],
                    sub[3],
                    sub[4]],

        'суббота': [sub[14],
                    sub[11],
                    sub[4],
                    sub[8]]
    }

    # timetable
    timetable = ['1) 8:15 - 8:55',
                 '2) 9:15 - 9:55',
                 '3) 10:15 - 10:55',
                 '4) 11:15 - 11:55',
                 '5) 12:15 - 12:55',
                 '6) 13:00 - 13:40',
                 '7) 13:45 - 14:25']

    # methods
    @classmethod
    def timetable_out(cls):
        answer = ''
        for time in range(len(cls.timetable)):
            answer += cls.timetable[time]
            answer += '\n'
        return answer

    @classmethod
    def schedule_out(cls):
        answer = ''
        for k, v in cls.schedule.items():
            answer += k.capitalize() + '\n'
            count = 1
            for s in v:
                answer += f'{count}) {s.capitalize()} \n'
                count += 1
            answer += '\n'
        return answer

    @classmethod
    def tomorrow_hw_out(cls):
        return cls.day_hw_out(datetime.today().isoweekday())

    @classmethod
    def all_hw_out(cls):
        answer = ''
        for k, v in cls.hw.items():
            answer += k.capitalize() + '\n'
            answer += v + '\n' + '\n'
        return answer

    @classmethod
    def day_hw_out(cls, date):
        date %= 7
        if date == 6:
            date = 0
        answer = list(cls.schedule.keys())[date].capitalize()
        answer += '\n' + '\n'
        count = 1
        for s in cls.schedule[list(cls.schedule.keys())[date]]:
            answer += f'{count}) {s.capitalize()}\n'
            answer += cls.hw[s] + '\n' + '\n'
            count += 1
        return answer

    @classmethod
    def download_hw(cls):
        answer = ''
        for v in cls.hw.values():
            answer += v.replace('\n', ' <3 ') + '\n'
        return answer

    @classmethod
    def upload_hw(cls, text):
        try:
            counter = 0
            for i in text.splitlines():
                if '/upload_hw' in i:
                    continue
                cls.hw[cls.sub[counter]] = i.replace(' <3 ', '\n')
                counter += 1
                print(i)
            print(cls.hw)
        except Exception:
            print('ну бывает')


class Keyboard(object):
    day_key = types.InlineKeyboardMarkup()
    day_key.add(types.InlineKeyboardButton(text='понедельник', callback_data='0'))
    day_key.add(types.InlineKeyboardButton(text='вторник', callback_data='1'))
    day_key.add(types.InlineKeyboardButton(text='среда', callback_data='2'))
    day_key.add(types.InlineKeyboardButton(text='четверг', callback_data='3'))
    day_key.add(types.InlineKeyboardButton(text='пятница', callback_data='4'))
    day_key.add(types.InlineKeyboardButton(text='суббота', callback_data='5'))

    sub_key = types.InlineKeyboardMarkup()
    for i in Func.sub:
        sub_key.add(types.InlineKeyboardButton(text=i, callback_data=i))
    sub_key.add(types.InlineKeyboardButton(text='выход', callback_data='exit'))
