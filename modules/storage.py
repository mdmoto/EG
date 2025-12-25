import json
import os
import datetime

PROFILE_FILE = "user_profile.json"

def save_profile(name, phone, year, month, day):
    data = {
        "name": name,
        "phone": phone,
        "dob_year": year,
        "dob_month": month,
        "dob_day": day
    }
    try:
        with open(PROFILE_FILE, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Save Profile Error: {e}")
        return False

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return None
    try:
        with open(PROFILE_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Load Profile Error: {e}")
        return None
