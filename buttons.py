from telebot import types

TEAM = {
    'LAC': 'Los-Angeles Clippers',
    'LAL': 'Los-Angeles Lakers',
    'GSW': 'Golden State Warriors',
    'PHO': 'Phoenix Suns',
    'SAC': 'Sacramento Kings',
    'DAL': 'Dallas Mavericks',
    'HOU': 'Houston Rockets',
    'MEM': 'Memphis Grizzlies',
    'NOP': 'New Orleans Pelicans',
    'SAS': 'San Antonio Spurs',
    'POR': 'Portland Trail Blazers',
    'MIN': 'Minnesota Timberwolves',
    'OKC': 'Oklahoma City Thunder',
    'DEN': 'Denver Nuggets',
    'UTA': 'Utah Jazz',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DET': 'Detroit Pistons',
    'IND': 'Indiana Pacers',
    'MIL': 'Milwaukee Bucks',
    'ATL': 'Atlanta Hawks',
    'CHO': 'Charlotte Hornets',
    'MIA': 'Miami Heat',
    'ORL': 'Orlando Magic',
    'WAS': 'Washington Wizards',
    'BOS': 'Boston Celtics',
    'NYK': 'New York Knicks',
    'BRK': 'Brooklyn Nets',
    'PHI': 'Philadelphia 76ers',
    'TOR': 'Toronto Raptors'
}

east_inl = types.InlineKeyboardMarkup()
btn_BOS = types.InlineKeyboardButton(
    text='Бостон Селтикс', callback_data='BOS')
btn_NYK = types.InlineKeyboardButton(
    text='Нью-Йорк Никс', callback_data='NYK')
btn_BRK = types.InlineKeyboardButton(
    text='Бруклин Нетс', callback_data='BRK')
btn_PHI = types.InlineKeyboardButton(
    text='Филадельфия 76 Сиксерс', callback_data='PHI')
btn_TOR = types.InlineKeyboardButton(
    text='Торонто Рапторз', callback_data='TOR')
btn_ATL = types.InlineKeyboardButton(
    text='Атланта Хоукс', callback_data='ATL')
btn_CHO = types.InlineKeyboardButton(
    text='Шарлотт Хорнетс', callback_data='CHO')
btn_MIA = types.InlineKeyboardButton(
    text='Майами Хит', callback_data='MIA')
btn_ORL = types.InlineKeyboardButton(
    text='Орладно Мэджик', callback_data='ORL')
btn_WAS = types.InlineKeyboardButton(
    text='Вашингтон Уизардс', callback_data='WAS')
btn_CHI = types.InlineKeyboardButton(
    text='Чикаго Буллз', callback_data='CHI')
btn_CLE = types.InlineKeyboardButton(
    text='Кливленд Кавальерс', callback_data='CLE')
btn_DET = types.InlineKeyboardButton(
    text='Детроит Пистонс', callback_data='DET')
btn_IND = types.InlineKeyboardButton(
    text='Индиана Пэйсерс', callback_data='IND')
btn_MIL = types.InlineKeyboardButton(
    text='Милуоки Бакс', callback_data='MIL')
east_inl.add(
    btn_BOS, btn_NYK, btn_BRK, btn_PHI, btn_TOR,
    btn_ATL, btn_CHO, btn_MIA, btn_ORL, btn_WAS,
    btn_CHI, btn_CLE, btn_DET, btn_IND, btn_MIL)

west_inl = types.InlineKeyboardMarkup()
btn_POR = types.InlineKeyboardButton(
    text='Портленд Трейл Блейзерс', callback_data='POR')
btn_MIN = types.InlineKeyboardButton(
    text='Миннесота Тимбервулз', callback_data='MIN')
btn_OKC = types.InlineKeyboardButton(
    text='Оклахома-Сити Тандер', callback_data='OKC')
btn_DEN = types.InlineKeyboardButton(
    text='Денвер Наггетс', callback_data='DEN')
btn_UTA = types.InlineKeyboardButton(
    text='Юта Джаз', callback_data='UTA')
btn_DAL = types.InlineKeyboardButton(
    text='Даллас Маверикс', callback_data='DAL')
btn_HOU = types.InlineKeyboardButton(
    text='Хьюстон Рокетс', callback_data='HOU')
btn_MEM = types.InlineKeyboardButton(
    text='Мемфис Гриззлис', callback_data='MEM')
btn_NOP = types.InlineKeyboardButton(
    text='Нью-Орлеан Пеликанс', callback_data='NOP')
btn_SAS = types.InlineKeyboardButton(
    text='Сан-Антонио Спёрс', callback_data='SAS')
btn_GSW = types.InlineKeyboardButton(
    text='Голден Стэйт Уорриорз', callback_data='GSW')
btn_LAC = types.InlineKeyboardButton(
    text='ЛА Клипперс', callback_data='LAC')
btn_LAL = types.InlineKeyboardButton(
    text='ЛА Лейкерс', callback_data='LAL')
btn_PHO = types.InlineKeyboardButton(
    text='Финикс Санз', callback_data='PHO')
btn_SAC = types.InlineKeyboardButton(
    text='Сакраменто Кингз', callback_data='SAC')
west_inl.add(
    btn_POR, btn_MIN, btn_OKC, btn_DEN, btn_UTA,
    btn_DAL, btn_HOU, btn_MEM, btn_NOP, btn_SAS,
    btn_GSW, btn_LAC, btn_LAL, btn_PHO, btn_SAC)

btn_main = types.KeyboardButton('Меню')
to_main = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(btn_main)

btn_east = types.InlineKeyboardButton(text='Восточная', callback_data='east')
btn_west = types.InlineKeyboardButton(text='Западная', callback_data='west')
conf_inl = types.InlineKeyboardMarkup().add(btn_east, btn_west)
