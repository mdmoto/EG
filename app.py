import streamlit as st
import time
import sys
import os
from PIL import Image

import datetime

# Ensure modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.data_ingestion import UserEntity
from modules.eastern import get_eastern_coordinates
from modules.western import get_western_coordinates
from modules.chaos import get_chaos_parameters
from modules.prophet import generate_prediction
from modules.features import perform_calibration, synthesize_voice, identify_divination_type, perform_specific_divination
from modules.i18n import get_text
# from modules.storage import load_profile, save_profile # DEPRECATED: Filesystem storage is not multi-user safe
import extra_streamlit_components as stx
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Entropy God",
    page_icon="assets/logo.jpg",
    layout="centered",
    initial_sidebar_state="expanded"
)


# --- LOAD CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# --- ANDROID / PWA SUPPORT ---
from modules.android_support import inject_pwa_meta, show_install_instructions
inject_pwa_meta()

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'SPLASH'

if 'user_data' not in st.session_state:
    st.session_state.user_data = None

if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

# --- LANGUAGE SELECTOR ---
lang_option = st.sidebar.selectbox("LANGUAGE / 语言", ["中文", "English"], index=0)
LANG = "CN" if lang_option == "中文" else "EN"

# --- COOKIE MANAGER (Global) ---
# Initialize here to persist across re-runs and page changes
cookie_manager = stx.CookieManager()

# --- SCREEN TRANSLATIONS ---

# --- NAVIGATION FUNCTIONS ---
def go_to_calibration():
    st.session_state.page = 'CALIBRATION'
    st.rerun()

def go_to_radiant():
    st.session_state.page = 'RADIANT'
    st.rerun()

def go_to_revelation(result, audio=None):
    st.session_state.prediction_result = result
    st.session_state.audio_data = audio
    st.session_state.page = 'REVELATION'
    st.rerun()

def reset_app():
    st.session_state.page = 'SPLASH'
    st.session_state.user_data = None
    st.session_state.prediction_result = None
    st.session_state.audio_data = None
    st.rerun()

def screen_splash():
    st.markdown('<div class="glass-panel" style="text-align: center; margin-top: 5vh; padding: 40px 20px;">', unsafe_allow_html=True)
    
    try:
        st.image("assets/logo.jpg", width=150)
    except:
        st.write(get_text("splash_logo_missing", LANG))
    
    st.markdown(f'<h1 class="glitch-text" style="font-size: 3em; margin-top: 20px;">{get_text("splash_title", LANG)}</h1>', unsafe_allow_html=True)
    st.caption(get_text("splash_subtitle", LANG))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(get_text("splash_init_btn", LANG)):
        with st.spinner(get_text("loading_modules", LANG)):
            time.sleep(1.5)
        go_to_calibration()
    
    st.markdown("<br>", unsafe_allow_html=True)
    show_install_instructions(LANG)


def screen_calibration():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f'<h2>{get_text("cal_title", LANG)}</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load Profile from Cookie
    cookie_val = cookie_manager.get("user_profile")
    saved_profile = None
    if cookie_val:
        try:
           saved_profile = json.loads(cookie_val)
        except:
           pass
    
    # Defaults
    def_name = "Neo"
    def_phone = "13800138000"
    def_date = None
    
    if saved_profile:
        def_name = saved_profile.get("name", "Neo")
        def_phone = saved_profile.get("phone", "13800138000")
        try:
            def_date = datetime.date(saved_profile["dob_year"], saved_profile["dob_month"], saved_profile["dob_day"])
        except:
            def_date = None
        if saved_profile:
            user = UserEntity(saved_profile["name"], saved_profile["dob_year"], saved_profile["dob_month"], saved_profile["dob_day"], 12, saved_profile["phone"])
            st.session_state.user_data = user
            
            # Pre-calculate data
            with st.spinner(get_text("loading_data", LANG)):
                eastern = get_eastern_coordinates(user)
                western = get_western_coordinates(user, lang=LANG)

    with st.expander(get_text("cal_meta_label", LANG), expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(get_text("cal_name_label", LANG), value=def_name)
        with col2:
            phone = st.text_input(get_text("cal_phone_label", LANG), value=def_phone)
            
        d = st.date_input(get_text("cal_date_label", LANG), value=def_date, min_value=datetime.date(1901, 1, 1), max_value=datetime.date.today())
        h = 12 

    st.markdown('<div class="chaos-btn">', unsafe_allow_html=True)
    if st.button(get_text("cal_btn", LANG)):
        if not name or not phone or not d:
            st.error(get_text("cal_error_missing", LANG))
        else:
            with st.spinner(get_text("cal_syncing", LANG)):
                # Save Profile to Cookie (Expires in 30 days)
                profile_data = {
                    "name": name,
                    "phone": phone, 
                    "dob_year": d.year, 
                    "dob_month": d.month, 
                    "dob_day": d.day
                }
                # Fire and forget cookie set
                cookie_manager.set("user_profile", json.dumps(profile_data), expires_at=datetime.datetime.now() + datetime.timedelta(days=30))
                
                # Proceed immediately using Session State (Memory)
                user = UserEntity(name, d.year, d.month, d.day, h, phone)
                st.session_state.user_data = user
                go_to_radiant()
    st.markdown('</div>', unsafe_allow_html=True)


def screen_radiant():
    user = st.session_state.user_data
    
    eastern = get_eastern_coordinates(user)
    western = get_western_coordinates(user, lang=LANG)
    chaos = get_chaos_parameters(user.entropy_seed)
    
    # Header
    st.markdown('<div class="glass-panel" style="display: flex; justify-content: space-between; align-items: center;">', unsafe_allow_html=True)
    st.markdown(f'<div style="color: var(--order-blue);">{get_text("rad_connected", LANG)}: {user.name}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: var(--chaos-orange);">{get_text("rad_entropy_state", LANG)}: {chaos["entropy_state"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # MOBILE-OPTIMIZED GRID LAYOUT
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-box" style="border-color: var(--order-blue);">
            <div class="metric-label">{get_text('rad_day_master', LANG)}</div>
            <div class="metric-value-east">{eastern['day_master']}</div>
        </div>
        <div class="metric-box" style="border-color: var(--order-blue);">
            <div class="metric-label">{get_text('rad_animal', LANG)}</div>
            <div class="metric-value-east">{eastern['animal']}</div>
        </div>
        <div class="metric-box" style="border-color: var(--chaos-orange);">
            <div class="metric-label">{get_text('rad_sun', LANG)}</div>
            <div class="metric-value-west">{western['sun']}</div>
        </div>
        <div class="metric-box" style="border-color: var(--chaos-orange);">
            <div class="metric-label">{get_text('rad_moon', LANG)}</div>
            <div class="metric-value-west">{western['moon']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # TABS
    tab_void, tab_lens = st.tabs([get_text("rad_tab_void", LANG), get_text("rad_tab_lens", LANG)])
    
    with tab_void:
        query = st.text_input(get_text("void_input_label", LANG), placeholder=get_text("void_input_placeholder", LANG))

        st.markdown('<div class="chaos-btn">', unsafe_allow_html=True)
        if st.button(get_text("void_btn", LANG)):
            final_query = query if query else get_text("void_default_query", LANG)
            
            with st.status(get_text("void_processing", LANG), expanded=True) as status:
                st.write(f"{get_text('void_aligning', LANG)} {eastern['full_string']}...")
                time.sleep(1)
                st.write(get_text("void_compensating", LANG))
                time.sleep(1)
                
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                except:
                    # Fallback for local dev if not using secrets.toml correctly (though secrets.toml is recommended)
                    # Or tell user to set it.
                    api_key = os.getenv("GEMINI_API_KEY")
                
                # NOTE: We might want the prompt to request the response language matching LANG.
                # But current prompt logic in prophet.py is fixed to Chinese mainly.
                # Use query injection to specifying output language?
                
                context_data = {
                    'seed': user.entropy_seed,
                    'eastern': f"{eastern['day_master']} (Day Master) / {eastern['full_string']}",
                    'western': f"Sun {western['sun']}, Moon {western['moon']}, Asc {western['ascendant']}",
                    'chaos': f"{chaos['entropy_state']} ({chaos['fluctuation_index']})",
                    'query': final_query + (f" (Response strictly in {LANG} Language)" if LANG == "EN" else " (请用中文回答)")
                }
                
                try:
                    prediction = generate_prediction(api_key, context_data)
                    status.update(label=get_text("void_complete", LANG), state="complete")
                    
                    audio_bytes = synthesize_voice(prediction, lang='en' if LANG == 'EN' else 'zh-CN')
                    
                    time.sleep(0.5)
                    go_to_revelation(prediction, audio_bytes)
                except Exception as e:
                    st.error(f"{get_text('void_error_conn', LANG)}: {e}")
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_lens:
        st.info(get_text("lens_info", LANG))
        # CAMERA INPUT IS PRIMARY
        img_file = st.camera_input(get_text("lens_cam_label", LANG))
        
        if img_file:
            st.markdown('<div class="chaos-btn">', unsafe_allow_html=True)
            if st.button(get_text("lens_btn", LANG)):
                with st.status(get_text("lens_processing", LANG), expanded=True) as status:
                     try:
                        api_key = st.secrets["GEMINI_API_KEY"]
                     except:
                        api_key = os.getenv("GEMINI_API_KEY")

                     # STEP 1: IDENTIFY
                     # Reset buffer just in case
                     img_file.seek(0)
                     method, obj_name = identify_divination_type(api_key, img_file)
                     
                     st.write(f"👁️ ANALYSIS: **{obj_name}**")
                     st.write(f"🔮 PROTOCOL: **{method}**")
                     time.sleep(1)
                     
                     # STEP 2: DIVINATION
                     img_file.seek(0) # Reset buffer for second read
                     result = perform_specific_divination(api_key, img_file, method, lang=LANG)
                     
                     status.update(label=get_text("void_complete", LANG), state="complete", expanded=False)
                     
                     audio_bytes = synthesize_voice(result, lang='en' if LANG == 'EN' else 'zh-CN')
                     
                     go_to_revelation(result, audio_bytes)
                     
            st.markdown('</div>', unsafe_allow_html=True)


def screen_revelation():
    st.markdown('<div class="glass-panel" style="border-color: var(--chaos-orange);">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: var(--chaos-orange); text-align: center;">{get_text("rev_title", LANG)}</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    result = st.session_state.prediction_result
    audio = st.session_state.audio_data
    
    if audio:
        st.audio(audio, format='audio/mp3')
    
    st.markdown(f"""
    <div style="
        background: rgba(0,0,0,0.6); 
        border-left: 3px solid var(--chaos-orange); 
        padding: 20px; 
        font-family: 'Courier New', monospace; 
        color: #e0e0e0; 
        line-height: 1.6;
        white-space: pre-wrap;
        box-shadow: inset 0 0 20px rgba(0,0,0,1);">
        {result}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(get_text("rev_ack_btn", LANG)):
        reset_app()

# --- MAIN ROUTER ---
if st.session_state.page == 'SPLASH':
    screen_splash()
elif st.session_state.page == 'CALIBRATION':
    screen_calibration()
elif st.session_state.page == 'RADIANT':
    screen_radiant()
elif st.session_state.page == 'REVELATION':
    screen_revelation()
