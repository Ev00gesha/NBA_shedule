import requests
from bs4 import BeautifulSoup as bs
from buttons import *
from parse_config import *


def find(team):
    response = requests.get(f'https://www.basketball-reference.com/teams/{team.upper()}/2023_games.html')
    if response.status_code == 200:
        soup = bs(response.text, 'lxml')
        all_games = soup.find('div', class_='table_wrapper')
        body = all_games.find('tbody')
        games = body.find_all('tr')
        result_games = []
        for i in range(len(games)):
            date = games[i].find('td', {'data-stat': 'date_game'})
            opp = games[i].find('td', {'data-stat': 'opp_name'})
            time = games[i].find('td', {'data-stat': 'game_start_time'})
            if date and opp and time:
                game_date_us = datetime.strptime(f'{date.get("csk")} {time.text[:-1]} PM', '%Y-%m-%d %I:%M %p')
                game_date_ru = USA.localize(game_date_us).astimezone(Europe)
                date_list = [int(i) for i in str(game_date_ru.date()).split('-')]
                date_str = f'{date_list[2]} {months[date_list[1] - 1]} {date_list[0]}'
                result = f'''Следующий матч {TEAM[team]}\nДата: {date_str}\n''' \
                         f'''Время: {game_date_ru.time().strftime("%H:%M")}\nПротив {opp.text}'''
                output_data = dict(zip(['game_date_us', 'result'], [game_date_us, result]))
                result_games.append(output_data)
        for i in range(len(result_games)):
            game_date_us = result_games[i]['game_date_us']
            if game_date_us.date() == time_now.date():
                if game_date_us.time() >= time_now.time():
                    return result_games[i]['result']
                else:
                    return result_games[i + 1]['result']
            elif game_date_us.date() > time_now.date():
                return result_games[i]['result']
            else:
                continue
        return 'Игра не найдена'
    else:
        return 'Ошибка( Скоро все исправим'


def main():
    find('LAC')


if __name__ == '__main__':
    main()
