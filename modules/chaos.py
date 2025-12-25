import datetime
import random

def get_chaos_parameters(seed):
    """
    Generates 'Chaos' parameters based on the entropy seed and current day.
    """
    today = datetime.date.today().isoformat()
    
    # Combine user seed with daily seed
    daily_seed_str = f"{seed}-{today}"
    
    # Seed the random generator
    random.seed(daily_seed_str)
    
    fluctuation = random.uniform(0.1, 99.9)
    entropy_level = "STABLE"
    if fluctuation > 80:
        entropy_level = "CRITICAL_CHAOS"
    elif fluctuation > 50:
        entropy_level = "HIGH_VOLATILITY"
    
    return {
        'fluctuation_index': f"{fluctuation:.2f}%",
        'entropy_state': entropy_level,
        'lucky_hex': hex(random.randint(0, 16777215))[2:].upper()
    }
