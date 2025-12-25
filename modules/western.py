import os

# --- CONFIGURE ASTROLOGY DATA PATH ---
# Must be set BEFORE importing flatlib/pyswisseph objects that might init defaults
# We look for 'swefiles' in the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # Go up one level from 'modules'
swe_path = os.path.join(project_root, 'swefiles')

if os.path.exists(swe_path):
    os.environ["SE_EPHE_PATH"] = swe_path
# -------------------------------------

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

def get_western_coordinates(user: 'UserEntity'):
    """
    Calculates Sun, Moon, and Ascendant signs.
    """
    try:
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
    except Exception as e:
        print(f"Western Chart Error: {e}")
        # Fallback for when pyswisseph fails on cloud (missing ephemeris)
        return {
            'sun': 'Unknown',
            'moon': 'Unknown', 
            'ascendant': 'Unknown'
        }
