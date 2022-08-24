import requests
from bs4 import BeautifulSoup as bs
from datetime import date
from parse_config import *


def find_today_games():
    result = []
    month = date.today().strftime('%B').lower()
    # response = requests.get(f'https://www.basketball-reference.com/leagues/NBA_2023_games-october.html')
    # if response.status_code == 200:
    #     pass
    # else:
    #     return False
    file = open('test_today_games.html')
    soup = bs(file.read(), 'lxml')
    shd = soup.find('div', class_='table_wrapper').find('tbody')
    games = shd.find_all('tr')
    date_today = time_now.strftime('%a, %b %d, %Y')
    for game in games:
        date_game = game.find('th', {'data-stat': 'date_game'}).find('a').text
        if date_today == date_game:
            time = game.find('td', {'data-stat': 'game_start_time'})
            date_us = datetime.strptime(f'{date_game} {time.text[:-1]} PM', '%a, %b %d, %Y %I:%M %p')
            date_ru = USA.localize(date_us).astimezone(Europe)
            date_list = [int(i) for i in str(date_ru.date()).split('-')]
            date_str = f'{date_list[2]} {months[date_list[1] - 1]} {date_list[0]}'
            home = game.find('td', {'data-stat': 'home_team_name'}).find('a').text
            visitor = game.find('td', {'data-stat': 'visitor_team_name'}).find('a').text
            info = f'''{home} - {visitor}\nДата: {date_str}\n''' \
                   f'''Время: {date_ru.time().strftime("%H:%M")}'''
            result.append(info)
    return result


def main():
    for game in find_today_games():
        print(game)


if __name__ == '__main__':
    main()
