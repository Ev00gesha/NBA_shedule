import mimetypes
import os
import schedule
import telebot
import psycopg2
import time
import threading
import secure
from buttons import *
from today_games import *
from find_game import *


bot = telebot.TeleBot(os.getenv('TOKEN'))
db_con = psycopg2.connect(os.getenv('DB'))
db_cur = db_con.cursor()


def show_today_games():
    db_cur.execute('SELECT id_user FROM users WHERE show_today_games = TRUE')
    users_send = db_cur.fetchall()
    if users_send:
        result = find_today_games()
        for user in users_send[0]:
            bot.send_message(user, 'Рассылка матчей которые пройдут в ближайшую ночь')
            for game in result:
                bot.send_message(user, game, reply_markup=to_main)


def timer():
    schedule.every(30).seconds.do(show_today_games)
    # schedule.every().day.at('22:10').do(show_today_games)
    while True:
        schedule.run_pending()


def create_team_list():
    teams = ''
    for key, item in TEAM.items():
        teams += f'{key}: {item}\n'
    return teams


def set_team(chat_id, new_team):
    team = get_team(chat_id)
    db_cur.execute('UPDATE users SET team = %s WHERE id_user = %s', (new_team, str(chat_id)))
    db_con.commit()
    if team:
        bot.send_message(chat_id, 'Любимая команда обновлена')
        settings(chat_id)
    else:
        bot.send_message(chat_id, 'Отлично, ты выбрал команду\nТеперь в любой момент можешь сразу узнать когда '
                                  'следующий матч')
        main(chat_id)


def get_team(chat_id):
    db_cur.execute('SELECT team FROM users WHERE id_user = %s;', (str(chat_id),))
    return db_cur.fetchone()[0]


def all_team(chat_id):
    bot.send_message(chat_id, 'Выбери конференцию', reply_markup=conf_inl)


def change_team(chat_id):
    teams = create_team_list()
    bot.send_message(chat_id, 'Чтобы поменять команду напиши мне сокращение команды, которое ты видишь ниже')
    time.sleep(4)
    bot.send_message(chat_id, teams)


def single_team(chat_id):
    team = get_team(chat_id)
    if team:
        bot.send_message(chat_id, 'Подожди немного, сейчас матч найдется')
        result = find(team)
        bot.send_message(chat_id, f'Твоя любимая команда {TEAM[team]}(можно поменять в настройках)')
        bot.send_message(chat_id, result, reply_markup=to_main)
    else:
        bot.send_message(chat_id, 'Ты еще не выбрал любимую команду(\nНапиши мне одно из сокращений команд, которые '
                                  'ты видишь ниже')
        time.sleep(4)
        teams = create_team_list()
        bot.send_message(chat_id, teams)


def set_bool(chat_id, column):
    db_cur.execute(f'SELECT {column} FROM users WHERE id_user = %s', (str(chat_id),))
    result = db_cur.fetchone()[0]
    db_cur.execute(f'UPDATE users SET {column} = %s WHERE id_user = %s', (not result, str(chat_id)))
    db_con.commit()
    return result


def set_bool_team_result(chat_id):
    result = set_bool(chat_id, 'team_result')
    if not result:
        team = get_team(chat_id)
        if team:
            bot.send_message(chat_id, f'После каждого завершенного матча, {TEAM[team]}, Вы будете получать '
                                      'сообщение с результатом матча')
        else:
            bot.send_message(chat_id, 'Чтобы отправлять Вам результаты матча, Вы должны выбрать команду. Напишите '
                                      'сокращение команды которое находиться ниже')
            time.sleep(4)
            teams = create_team_list()
            bot.send_message(chat_id, teams)
    else:
        bot.send_message(chat_id, 'Вам не будут приходить сообщения с результатами матча')
    settings(chat_id)


def set_bool_show_games(chat_id):
    result = set_bool(chat_id, 'show_today_games')
    if not result:
        bot.send_message(chat_id, 'В определенное время будет приходить список матчей, которые пройдут в текущий день')
    else:
        bot.send_message(chat_id, 'Список матчей приходить не будет')
    settings(chat_id)


def settings(chat_id):
    team = get_team(chat_id)
    db_cur.execute('SELECT team_result FROM users WHERE id_user = %s', (str(chat_id),))
    team_result_bool = db_cur.fetchone()[0]
    db_cur.execute('SELECT show_today_games FROM users WHERE id_user = %s', (str(chat_id),))
    show_td_games_bool = db_cur.fetchone()[0]
    cng_tm = f'Любимая команда: {TEAM[team] if team else "не выбрана"}\n'
    tm_rt = f'Отправка результата матча любимой команды: {"✅" if team_result_bool else "❌"}\n'
    sh_td = f'Отправка всех матчей которые проходят сегодня: {"✅" if show_td_games_bool else "❌"}\n'
    result = cng_tm + tm_rt + sh_td
    chg_team = types.KeyboardButton('Поменять команду')
    msg_team_result = 'Отправлять результаты' if not team_result_bool else 'Не отправлять результаты'
    team_result = types.KeyboardButton(msg_team_result)
    msg_all_games = 'Отправлять расписание матчей' if not show_td_games_bool else 'Не отправлять расписание матчей'
    all_games = types.KeyboardButton(msg_all_games)
    menu = types.KeyboardButton('Меню')
    settings_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    settings_kb.add(chg_team).add(team_result, all_games).add(menu)
    bot.send_message(chat_id, result, reply_markup=settings_kb)


def check_user(chat_id):
    db_cur.execute('SELECT id_user FROM users')
    return any(map(lambda x: str(chat_id) == x[0], db_cur.fetchall()))


def main(chat_id):
    main_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_all = types.KeyboardButton('Все команды')
    btn_single = types.KeyboardButton('Любимая команда')
    btn_settings = types.KeyboardButton('Настройки')
    main_kb.add(btn_all, btn_single, btn_settings)
    bot.send_message(chat_id, 'Мы в главном меню', reply_markup=main_kb)


@bot.message_handler(['start'])
def start_bot(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'В этом боте ты можешь легко узнать расписание игр в NBA\nТакже ты можешь ввести '
                              'команду /info и узнать весь функционал бота')
    if check_user(chat_id):
        main(chat_id)
    else:
        db_cur.execute('INSERT INTO users(id_user) VALUES(%s)', (chat_id,))
        db_con.commit()
        main(chat_id)


@bot.message_handler(['info'])
def info(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'С помощью кнопки "Все команды", выбирается команда из всех команд NBA и приходит '
                              'сообщение с датой и временем следующего матча.\nС помощью кнопки "Любимая команда", '
                              'первый раз выбирается команда и потом можно узнавать когда следующий матч именно этой '
                              'команды.\nСледующие 2 функции включаются в настройках!!!\nФункция "Отправка результата '
                              'матча любимой команды", когда матч завершается приходит результат матча.\nФункция '
                              '"Отправка всех игр которые будут проходить в текущий день", в определенное время будет '
                              'приходить сообщение со списком всех матчей которые будут проходить в этот день.')
    main(chat_id)


@bot.message_handler(content_types=['text'])
def navigator(message):
    chat_id = message.chat.id
    if message.text == 'Все команды':
        all_team(chat_id)
    elif message.text == 'Любимая команда':
        single_team(chat_id)
    elif message.text == 'Настройки':
        settings(chat_id)
    elif message.text == 'Меню':
        main(chat_id)
    elif message.text.upper() in TEAM.keys():
        set_team(chat_id, message.text.upper())
    elif message.text == 'Поменять команду':
        change_team(chat_id)
    elif message.text == 'Отправлять результаты' or message.text == 'Не отправлять результаты':
        set_bool_team_result(chat_id)
    elif message.text == 'Отправлять расписание матчей' or message.text == 'Не отправлять расписание матчей':
        set_bool_show_games(chat_id)
    else:
        bot.send_message(chat_id, 'Я не понимаю твою команду')
        main(chat_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('east'))
def callback_east(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Выбирай команду', reply_markup=east_inl)


@bot.callback_query_handler(func=lambda call: call.data.startswith('west'))
def callback_west(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Выбирай команду', reply_markup=west_inl)


@bot.callback_query_handler(func=lambda call: call.data not in ['east', 'west'])
def callback_teams(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Подожди немного, сейчас матч найдется')
    game_info = find(call.data)
    bot.send_message(chat_id, game_info, reply_markup=to_main)


if __name__ == '__main__':
    thr = threading.Thread(target=timer, name='timer')
    thr.start()
    bot.polling(none_stop=True, interval=0)
