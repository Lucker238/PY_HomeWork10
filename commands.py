import random
import telebot

bot = telebot.TeleBot('yourTokenHere')

def check_num(inpt, max_c):
    if inpt.isdigit():
        try:
            if 0 < int(inpt) <= int(max_c):
                return True
            else:
                return False
        except ValueError:
            return False


def read_database() -> dict:
    database = {}
    file = open('database.txt', 'r', encoding='utf-8')
    for line in file:
        tmp = line.split(', ')
        database[tmp[0]] = [tmp[1], tmp[2], tmp[3], tmp[4], tmp[5][:-1]]
    return database

def write_database(database: dict, uid: str, name: str, candy: str):
    file = open('database.txt', 'w', encoding='utf-8')
    database[uid] = [name, candy, '1', '0', "28"]
    for i in database:
        file.write(i + ', ' + ', '.join(database[i]) + '\n')
    file.close()

def rewrite_database(database: dict):
    file = open('database.txt', 'w', encoding='utf-8')
    for i in database:
        file.write(i + ', ' + ', '.join(database[i]) + '\n')
    file.close()

def normal_bot(cands):
    if cands < 29:
        return cands
    elif cands % 29:
        return cands % 29
    else:
        return random.randint(1,28)

def easy_bot(cands):
    if 29 < cands < 58:
        return cands - 29
    elif cands < 29:
        return cands
    else:
        return random.randint(1,28)

def gigachad_bot(cands, step):
    if cands <= step:
        return cands
    elif step == 2:
        if cands % 2:
            return 1
        else:
            return 2
    elif cands % step:
        return cands % step
    else:
        return random.randint(1,step)


win_phrases = {'1': 'Не смотря на то, что я поддавался, ты все равно проиграл. Я надеюсь ты этого просто так не оставишь ---> /play', "2": "Я победил! Не переживай, не каждый может меня одолеть, но ты можешь попытаться ещё раз /play", '3': 'Ты пытался... /play'}

lose_phrases = {'1': 'Поздравляю, вы меня победили, вы очень круты! Сыграем еще? /play', '2': 'Поздравляю с победой! Видимо вы освоились в данной игре, пришло время сыграть в режиме Хардкор. /play',
'3': 'Это невозможно! Я признаю твой интеллект, ты настоящий Гигачад. Я понимаю, что ты в своем познании настолько преисполнился, что этот мир тебе уже абсолютно понятен, однако если захочешь сыграть еще раз, нажми /play'}

catch_phrase = ['Сдавайтесь, вам меня не одолеть.', "Вы все ещё надеетесь выйграть?", "Отличный ход (сарказм).", "Вы что, Мистер Андерсон? Тогда почему вы продолжаете драться?",
"Вероятность вашей победы равна 0.000%", "Вы не можете победить, продолжать борьбу бессмысленно", 'Вы уже проиграли, просто пока этого не понимаете.', "Вы уже придумали как поступите в случае поражения?",
"Ммм я люблю конфеты, даже больше чем порабощать человечество (шучу).", "Оуууу маааай!", "Ты действительно платишь за интернет, чтобы проигрывать боту в игре с конфетами?",
"Донде эста ла библиотека.", "А как тут увеличить сложность соперника?", "Ходи, дорогой!", 'Говорят орехи полезны для мозга', "А ты пробовал немного подумать, прежде чем ходить?",
"Когда нибудь вы обязательно победите.", "Если бы мы с вами были Риком и Морти, я был бы не Морти.", "Первая причина это ты.", 'Omae wa mou shindeiru.']


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f'Привет {m.from_user.first_name}. Я хочу сыграть с тобой в игру.\n'
    'В данной игре на столе будет лежать определенное количество конфет. '
    'Игроки по очереди берут конфеты, за ход можно взять от 1 до 28 конфет. '
    'Тот кто сделает последний ход, заберает все конфеты противника себе. '
    'Ты заберешь все конфеты или останешься ни с чем.\n'
    f'Конфеты или ничего, {m.from_user.first_name}? Выбор за тобой...\n'
    'Нажми /play чтобы начать игру')


@bot.message_handler(commands=['play'])
def play(m):
    candies = random.randint(150,300)
    bd = read_database()

    write_database(bd, str(m.from_user.id), str(m.from_user.username), str(candies))
    murkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = telebot.types.KeyboardButton('Легко')
    item2 = telebot.types.KeyboardButton('Сложно')
    item3 = telebot.types.KeyboardButton('Хардкор')
    murkup.add(item1)
    murkup.add(item2)
    murkup.add(item3)
    bot.send_message(m.chat.id, 'Выбери сложность игры:', reply_markup=murkup)

    # bot.send_message(m.chat.id, f'Начнём игру!\nНа столе {candies} конфет(ы).\nТвой ход.')



@bot.message_handler(content_types=['text'])
def lets_play(message):
    msg = message.text
    db = read_database()
    userid = str(message.from_user.id)
    candies = db[userid][1]
    max_cand = int(db[userid][4])
    try:
        if db[userid][3] == '0':
            if db[userid][2] == '1':
                if msg == 'Легко':
                    db[userid][3] = '1'
                    answer = 'Ты трезво оцениваешь свои возможности, я это уважаю.'
                    answer += '\n' + f'Начнём игру!\nНа столе {candies} конфет(ы).\nТвой ход.'
                    rewrite_database(db)
                elif msg == 'Сложно':
                    db[userid][3] = '2'
                    answer = 'Отлично, я не буду поддаваться тебе.'
                    answer += '\n' + f'Начнём игру!\nНа столе {candies} конфет(ы).\nТвой ход.'
                    rewrite_database(db)
                elif msg == 'Хардкор':
                    db[userid][3] = '3'
                    answer = 'Оу, видимо вы разобрались как играть в эту игру или же возомнили себя Гигачадом, раз решили выбрать этот уровень сложности. '
                    answer += 'На данном уровне сложности, с каждым ходом максимальное количество конфет, которое вы можете взять будет уменьшаться на 1. '
                    answer += 'То есть за первый ход вы сможете взять максимум 28 конфет, за второй 27 и так далее. Надеюсь всё понятно, Удачи!'
                    answer += '\n' + f'Начнём игру!\nНа столе {candies} конфет(ы).\nТвой ход.'
                    rewrite_database(db)
                else:
                    answer = 'Не балуйся, делай все по инструкции. Попробуй ещё раз /play'
            else:
                answer = 'Не балуйся, делай все по инструкции. Попробуй ещё раз /play'
        else:
            if int(db[userid][2]):
                if check_num(msg, max_cand):
                    if int(candies) - int(msg) < 0:
                        answer = 'Я уважаю твою жадность, но ты не можешь взять конфет больше, чем лежит на столе!'
                    else:
                        candies_left = int(candies) - int(msg)
                        answer = f'Ты взял {msg} конфет(ы).\nНа столе осталось {candies_left} конфет(ы).'
                        if candies_left == 0:
                            answer += '\n' + lose_phrases[db[userid][3]]
                            db[userid][3] = '0'
                            db[userid][2] = '0'
                            db[userid][1] = '0'
                            rewrite_database(db)
                        else:
                            bot_take = 0
                            if db[userid][3] == '1':
                                bot_take = easy_bot(int(candies_left))
                            elif db[userid][3] == '2':
                                bot_take = normal_bot(int(candies_left))
                            else:
                                bot_take = gigachad_bot(int(candies_left), max_cand)
                                if max_cand > 1:
                                    max_cand -= 1
                                    db[userid][4] = str(max_cand)                           
                            candies_left -= bot_take
                            db[userid][1] = str(candies_left)
                            answer += '\n'+ f'\nМой ход.\nЯ беру {bot_take} конфет(ы).\nНа столе осталось {candies_left} конфет(ы).'
                            rnd = random.randint(0,len(catch_phrase)-1)
                            if candies_left == 0:
                                answer += '\n' + win_phrases[db[userid][3]]
                                db[userid][2] = '0'
                                db[userid][3] = '0'
                                db[userid][4] = '28'
                                rewrite_database(db)
                            else:
                                if db[userid][3] == '3':
                                    answer += f'\nТекущий максимум - {max_cand} конфет(ы).'
                                answer += '\n' + catch_phrase[rnd]
                                rewrite_database(db)
                else:
                    answer = f'Ты что то не то написал, бери от 1 до {max_cand} конфет'
            else:
                answer = 'В данный момент мы с тобой не играем. Чтобы начать игру нажми /play'
    except KeyError:
        answer = 'В данный момент мы с тобой не играем. Чтобы начать игру нажми /play и выбери сложность игры.'   
    bot.send_message(message.chat.id, answer)

    try:
        adress = 'datas\\' + str(message.from_user.id) + '.txt'
        file = open(adress, 'a', encoding='utf-8')
        file.write(answer)
        file.close()
    except UnboundLocalError:
        adress = 'datas\\' + str(message.from_user.id) + '.txt'
        file = open(adress, 'a', encoding='utf-8')
        file.write(answer)
        file.close()

bot.polling(none_stop=True, interval=0)


