import os
import swisseph as swe
from datetime import datetime, timedelta

# --- CONFIGURE ASTROLOGY DATA PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # Go up one level from 'modules'
swe_path = os.path.join(project_root, 'swefiles')

if os.path.exists(swe_path):
    os.environ["SE_EPHE_PATH"] = swe_path
    try:
        swe.set_ephe_path(swe_path)
    except:
        pass
else:
    # Set to a default if local not found, though this likely fails on cloud
    pass

# -------------------------------------

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_sign_name(lon):
    """Converts longitude (0-360) to Zodiac Sign name."""
    index = int(lon / 30)
    return ZODIAC_SIGNS[index % 12]

def get_western_coordinates(user: 'UserEntity'):
    """
    Calculates Sun, Moon, and Ascendant signs using DIRECT swisseph.
    Bypasses flatlib to avoid 'tuple index out of range' errors on Cloud.
    """
    try:
        # 1. Calculate Julian Day (JD)
        # Convert local time (UTC+8 default) to UTC
        dt_local = datetime(user.birth_year, user.birth_month, user.birth_day, user.birth_hour, 0)
        # Assuming input is China Time (+8), convert to UTC
        dt_utc = dt_local - timedelta(hours=8)
        
        # Calculate JD
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0)

        # 2. Calculate Sun & Moon
        # flags: SEFLG_SWIEPH (use Ephemeris), SEFLG_SPEED (calc speed)
        # If ephemeris missing, it naturally falls back to Moshier (unless we strictly enforce)
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        
        # SUN
        res_sun = swe.calc_ut(jd, swe.SUN, flags)
        # res_sun is usually (lon, lat, dist, speed, ...) or error
        if isinstance(res_sun, tuple) and len(res_sun) >= 1:
             # swisseph sometimes returns ((...), flag) or just (...)
             # In pyswisseph, calc_ut returns a tuple of 6 floats usually
             sun_lon = res_sun[0]
             if isinstance(sun_lon, tuple): sun_lon = sun_lon[0] # Handle nested
        else:
             sun_lon = 0

        # MOON
        res_moon = swe.calc_ut(jd, swe.MOON, flags)
        if isinstance(res_moon, tuple) and len(res_moon) >= 1:
             moon_lon = res_moon[0]
             if isinstance(moon_lon, tuple): moon_lon = moon_lon[0]
        else:
             moon_lon = 0


        # 3. Calculate Ascendant (Houses)
        # houses(jd, lat, lon, hsys) -> (cusps, ascmc)
        # ascmc[0] is Ascendant
        # 'P' = Placidus
        cusps, ascmc = swe.houses(jd, user.lat, user.lon, b'P') 
        asc_lon = ascmc[0]

        return {
            'sun': get_sign_name(sun_lon),
            'moon': get_sign_name(moon_lon),
            'ascendant': get_sign_name(asc_lon)
        }
        
    except Exception as e:
        print(f"Western Chart Error: {e}")
        # Debugging: Show the error in the UI
        return {
            'sun': f"ERR: {str(e)}",
            'moon': 'Unknown', 
            'ascendant': 'Unknown'
        }
