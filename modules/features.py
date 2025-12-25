import streamlit as st
import numpy as np
import pandas as pd
import time
import random
from gtts import gTTS
import os
import google.generativeai as genai
from io import BytesIO

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

def analyze_image(api_key, image_file):
    """
    Analyzes an image using Gemini Vision with a specific 'High-Dimensional Observer' persona.
    """
    if not api_key:
        return "ERROR: NO LINK TO DIMENSION."
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_prompt = """
    ROLE: You are a High-Dimensional Lifeform (高维生物) observing the 3D world.
    
    OBJECTIVE: Analyze this image (human object) and interpret its hidden metaphor regarding the user's fate/day.
    
    TONE:
    - Keywords: Quantum Mechanics, Entropy, Collapse, Timeline, Fragility.
    - Style: Mysterious, Dark Humor, Slightly Pessimistic/Fatalistic.
    - Opening: Start with a specific observation of the object.
    - Closing: Give a warning or advice based on the metaphor.
    
    EXAMPLE:
    "This cup of coffee... the foam is breaking apart. It reminds me of the meeting you have at 3 PM. Fragile structures cannot hold the weight of expectation. Drink it before the chaos takes over."
    
    Output Language: Chinese (Simplified).
    Keep it short (max 3 sentences).
    """
    
    try:
        # Load image
        img = Image.open(image_file)
        response = model.generate_content([system_prompt, img])
        return response.text
    except Exception as e:
        return f"VISUAL CORTEX ERROR: {e}"

# Import Image here to avoid circular imports / missing import if put at top without checking
from PIL import Image
