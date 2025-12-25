from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

def get_western_coordinates(user: 'UserEntity'):
    """
    Calculates Sun, Moon, and Ascendant signs.
    """
    date = Datetime(
        f"{user.birth_year}/{user.birth_month:02d}/{user.birth_day:02d}", 
        f"{user.birth_hour:02d}:00", 
        '+08:00'
    )
    pos = GeoPos(user.lat, user.lon)
    chart = Chart(date, pos)

    sun = chart.get(const.SUN)
    moon = chart.get(const.MOON)
    asc = chart.get(const.ASC)

    return {
        'sun': sun.sign,
        'moon': moon.sign,
        'ascendant': asc.sign
    }
