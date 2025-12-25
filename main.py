import sys
import os

# Ensure modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.data_ingestion import UserEntity
from modules.eastern import get_eastern_coordinates
from modules.western import get_western_coordinates
from modules.chaos import get_chaos_parameters

def main():
    print(f"--- INITIALIZING ENTROPY GOD CORE ---")
    
    # 1. Ingest Data (Mocked Input as per user request 'Neo')
    user = UserEntity(
        name="Neo",
        birth_year=1983,
        birth_month=11,
        birth_day=8,
        birth_hour=5,
        phone="13800138000"
    )
    
    print(f"Target Identity: {user.name}")
    print(f"Bio-Entropy Hash: {user.entropy_seed} (Anonymized)")
    
    # 2. Calculate Eastern Coordinates
    eastern = get_eastern_coordinates(user)
    print(f"\n[EASTERN COORDINATES]")
    print(f"BaZi: {eastern['full_string']}")
    print(f"Day Master: {eastern['day_master']}")
    print(f"Animal: {eastern['animal']}")
    
    # 3. Calculate Western Coordinates
    try:
        western = get_western_coordinates(user)
        print(f"\n[WESTERN COORDINATES]")
        print(f"Sun: {western['sun']}")
        print(f"Moon: {western['moon']}")
        print(f"Ascendant: {western['ascendant']}")
    except Exception as e:
        print(f"\n[WESTERN COORDINATES ERROR]: {e}")
        # Fallback if flatlib fails (e.g. no ephemeris files)
        western = {'sun': 'Unknown', 'moon': 'Unknown', 'ascendant': 'Unknown'}

    # 4. Chaos Parameters
    chaos = get_chaos_parameters(user.entropy_seed)
    print(f"\n[CHAOS PARAMETERS]")
    print(f"Fluctuation Index: {chaos['fluctuation_index']}")
    print(f"State: {chaos['entropy_state']}")
    print(f"Lucky Hex: {chaos['lucky_hex']}")
    
    # 5. Call the Prophet (Gemini API)
    from modules.prophet import generate_prediction
    
    # Using the user-provided key
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY not set. Please set environment variable.")
        return
    
    context_data = {
        'seed': user.entropy_seed,
        'eastern': f"{eastern['day_master']} (Day Master) / {eastern['full_string']}",
        'western': f"Sun {western['sun']}, Moon {western['moon']}, Asc {western['ascendant']}",
        'chaos': f"{chaos['entropy_state']} ({chaos['fluctuation_index']})"
    }
    
    print(f"\n[ESTABLISHING CONNECTION TO EVENT HORIZON...]")
    print("-" * 40)
    
    oracle_speech = generate_prediction(API_KEY, context_data)
    
    print(oracle_speech)
    print("-" * 40)
    print("Transmission Complete.")

if __name__ == "__main__":
    main()
