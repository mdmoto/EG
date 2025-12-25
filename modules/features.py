import streamlit as st
import numpy as np
import pandas as pd
import time
import random
from gtts import gTTS
import os
import google.generativeai as genai
from io import BytesIO
from PIL import Image

def synthesize_voice(text, lang='zh-CN'):
    """
    Generates audio from text using gTTS.
    Returns bytes of the audio file.
    """
    try:
        mp3_fp = BytesIO()
        # 'zh-CN' is standard Chinese. 
        # Getting a "MOSS-like" emotionless voice is hard with gTTS (it's standard Google voice).
        # We can try to use text processing to make it sound more robotic (short sentences).
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.write_to_fp(mp3_fp)
        return mp3_fp
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def perform_calibration():
    """
    Simulates a biometric scan and generates a 'Waveform' chart.
    Returns a DataFrame for st.line_chart and a status dict.
    """
    # Simulate scanning
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    scan_steps = [
        "INITIALIZING GYROSCOPE...",
        "CAPTURING MICRO-TREMORS...",
        "ANALYZING PULSE VARIABILITY...",
        "SYNCING WEATHER SATELLITE (SEED: CLOUD_COVER)...",
        "FETCHING MARKET VOLATILITY INDEX...",
        "CALIBRATION COMPLETE."
    ]
    
    for i, step in enumerate(scan_steps):
        time.sleep(0.5)
        status_text.text(f"// {step}")
        progress_bar.progress((i + 1) / len(scan_steps))
        
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()
    
    # Generate Waveform Data
    # 3 Sine waves + Noise
    x = np.linspace(0, 100, 200)
    freq1 = random.uniform(0.1, 0.5)
    freq2 = random.uniform(0.5, 1.5)
    noise_level = random.uniform(0.1, 0.5)
    
    y = np.sin(x * freq1) + 0.5 * np.sin(x * freq2) + np.random.normal(0, noise_level, 200)
    
    df = pd.DataFrame(y, columns=["Entropy Fluctuation"])
    
    # Calculate Metrics
    volatility = np.std(y)
    mean_val = np.mean(y)
    
    metrics = {
        "volatility": "HIGH" if volatility > 0.6 else "LOW",
        "deviation": "POSITIVE" if mean_val > 0 else "NEGATIVE",
        "raw_vol": f"{volatility:.4f}",
        "raw_dev": f"{mean_val:.4f}"
    }
    
    return df, metrics

def identify_divination_type(api_key, image_file):
    """
    Step 1: Identify the object to determine the divination method.
    Returns: (Method Name, Object Name) e.g. ("Tasseography", "Coffee Cup")
    """
    if not api_key: return ("General", "Unknown")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Analyze this image and identify the main object relevant to divination.
    Classify into one of these types:
    - COFFEE (if cup, coffee grounds/foam) -> Return "COFFEE"
    - TAROT (if tarot cards) -> Return "TAROT"
    - PALM (if hand/palm) -> Return "PALM"
    - FACE (if human face) -> Return "FACE"
    - CLOUD (if sky/clouds) -> Return "CLOUD"
    - OTHER (anything else) -> Return "OTHER"
    
    Output format: STRICTLY only the category word.
    """
    
    try:
        img = Image.open(image_file)
        response = model.generate_content([prompt, img])
        category = response.text.strip().upper()
        
        map_name = {
            "COFFEE": ("Tasseography", "Coffee Residue"),
            "TAROT": ("Tarot Reading", "Tarot Spread"),
            "PALM": ("Palmistry", "Hand Lines"),
            "FACE": ("Physiognomy", "Facial Features"),
            "CLOUD": ("Aeromancy", "Cloud Formation"),
            "OTHER": ("Psychometry", "Object Soul")
        }
        return map_name.get(category, ("Psychometry", "Object Soul"))
    except Exception as e:
        print(f"Identify Error: {e}")
        return ("General", "Unknown")

def perform_specific_divination(api_key, image_file, method, lang='CN'):
    """
    Step 2: Perform the specific divination based on the method.
    """
    if not api_key: return "ERROR: CONNECTION LOST."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    language = "Chinese (Simplified)" if lang in ['CN', 'zh-CN'] else "English"
    
    prompts = {
        "Tasseography": f"You are a master Tasseographer. Analyze the shapes in this coffee/tea residue. Interpret user's fortune. Language: {language}. Tone: Mystical, Precognitive.",
        "Tarot Reading": f"You are a Tarot Grandmaster. Interpret these cards (Upright/Reversed) and their spread. Reveal the destiny. Language: {language}. Tone: Serious, Occult.",
        "Palmistry": f"You are an expert Palmist. Read the major lines (Heart, Head, Life, Fate) visible in this hand. Predict health and wealth. Language: {language}. Tone: Traditional, Insightful.",
        "Physiognomy": f"You are a Face Reader. Analyze the facial features (Eyes, Nose, Forehead) for destiny indicators. Language: {language}. Tone: Direct, Revealing.",
        "Aeromancy": f"You are a Cloud Reader. Interpret the shapes in the sky as omens. Language: {language}. Tone: Ethereal, Poetic.",
        "Psychometry": f"You are a Psychometrist. You can feel the energy/memories attached to this object. Tell me its story and what it brings to the owner. Language: {language}. Tone: Cyberpunk, Abstract."
    }
    
    system_prompt = prompts.get(method, prompts["Psychometry"])
    
    try:
        img = Image.open(image_file)
        response = model.generate_content([system_prompt, img])
        return response.text
    except Exception as e:
        return f"DIVINATION ERROR: {e}"

# Import Image here to avoid circular imports / missing import if put at top without checking
# from PIL import Image
