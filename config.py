from telebot import types
from datetime import datetime

TOKEN = '1384356348:AAHvlCs2SFQCUepV5CsI6yqA5tk65pWSt7E'
EDITORS = [976798046, 1311758742, 413549520]
BLACK_LIST = [470540326]


class DataBase:
    # subjects
    sub = [
        'обж',  # 0
        'химия',  # 1
        'физика',  # 2
        'алгебра',  # 3
        'история',  # 4
        'геометрия',  # 5
        'экономика',  # 6
        'география',  # 7
        'литература',  # 8
        'информатика',  # 9
        'физкультура',  # 10
        'правоведение',  # 11
        'русский язык',  # 12
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
                        sub[8],
                        sub[6],
                        sub[11]],

        'вторник': [sub[8],
                    sub[15],
                    sub[8],
                    sub[1],
                    sub[2],
                    sub[12],
                    sub[10]],

        'среда': [sub[2],
                  sub[2],
                  sub[14],
                  sub[12],
                  sub[12],
                  sub[9]],

        'четверг': [sub[13],
                    sub[13],
                    sub[2],
                    sub[10],
                    sub[7],
                    sub[5],
                    sub[5]],

        'пятница': [sub[9],
                    sub[9],
                    sub[3],
                    sub[3],
                    sub[4],
                    sub[2],
                    sub[15]],

        'суббота': [sub[14],
                    sub[9],
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
    def timetable_out(self):
        answer = ''
        for time in range(len(self.timetable)):
            answer += self.timetable[time]
            answer += '\n'
        return answer

    def schedule_out(self):
        answer = ''
        for k, v in self.schedule.items():
            answer += k.capitalize() + '\n'
            count = 1
            for s in v:
                answer += f'{count}) {s.capitalize()} \n'
                count += 1
            answer += '\n'
        return answer

    def tomorrow_hw_out(self):
        return self.day_hw_out(datetime.today().isoweekday())

    def all_hw_out(self):
        answer = ''
        for k, v in self.hw.items():
            answer += k.capitalize() + '\n'
            answer += v + '\n' + '\n'
        return answer

    def day_hw_out(self, date):
        date %= 7
        if date == 6:
            date = 0
        answer = list(self.schedule.keys())[date].capitalize()
        answer += '\n' + '\n'
        count = 1
        for s in self.schedule[list(self.schedule.keys())[date]]:
            answer += f'{count}) {s.capitalize()}\n'
            answer += self.hw[s] + '\n' + '\n'
            count += 1
        return answer

    def save(self):
        with open('data.txt', 'w') as file:
            for v in self.hw.values():
                file.write(str(v).replace('\n', ' <3 ') + '\n')
            file.close()

    def load(self):
        with open('data.txt', 'r') as file:
            for line in self.sub:
                self.hw[line] = file.readline().replace('\n', '')
                self.hw[line] = self.hw[line].replace(' <3 ', '\n')
            file.close()


func = DataBase()

day_key = types.InlineKeyboardMarkup()
day_key.add(types.InlineKeyboardButton(text='понедельник', callback_data='0'))
day_key.add(types.InlineKeyboardButton(text='вторник', callback_data='1'))
day_key.add(types.InlineKeyboardButton(text='среда', callback_data='2'))
day_key.add(types.InlineKeyboardButton(text='четверг', callback_data='3'))
day_key.add(types.InlineKeyboardButton(text='пятница', callback_data='4'))
day_key.add(types.InlineKeyboardButton(text='суббота', callback_data='5'))

# keyboards
sub_key = types.InlineKeyboardMarkup()
for i in func.sub:
    sub_key.add(types.InlineKeyboardButton(text=i, callback_data=i))
sub_key.add(types.InlineKeyboardButton(text='выход', callback_data='exit'))
