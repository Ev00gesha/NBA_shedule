import pytz
from datetime import datetime


Europe = pytz.timezone('Europe/Moscow')
USA = pytz.timezone('America/New_York')
time_now = datetime.now(tz=pytz.timezone('America/New_York'))
months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


