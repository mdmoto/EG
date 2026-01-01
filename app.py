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
from modules.locations import LOCATIONS, get_coordinates

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="熵之预言",
    page_icon="assets/logo.jpg",
    layout="wide",
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

# --- LANGUAGE SELECTOR & GLOBAL STATE ---
if 'lang' not in st.session_state:
    st.session_state.lang = "CN"

# Helper to map display name to code
LANG_MAP = {
    "中文 (Chinese)": "CN",
    "English": "EN",
    "日本語 (Japanese)": "JP",
    "한국어 (Korean)": "KR",
    "Français (French)": "FR",
    "Español (Spanish)": "ES",
    "ไทย (Thai)": "TH",
    "Tiếng Việt (Vietnamese)": "VI"
}

# Reverse map for default index
CODE_TO_NAME = {v: k for k, v in LANG_MAP.items()}

LANG = st.session_state.lang

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
    st.markdown('<div style="text-align: center; margin-top: 5vh;">', unsafe_allow_html=True)
    
    # 1. LANGUAGE SELECTOR (First visual element)
    # Get current index
    current_name = CODE_TO_NAME.get(st.session_state.lang, "中文 (Chinese)")
    lang_names = list(LANG_MAP.keys())
    try:
        idx = lang_names.index(current_name)
    except:
        idx = 0
        
    selected_lang_name = st.selectbox("Please Select Language / 请选择语言", lang_names, index=idx)
    
    # Update state if changed
    new_lang_code = LANG_MAP[selected_lang_name]
    if new_lang_code != st.session_state.lang:
        st.session_state.lang = new_lang_code
        st.rerun()

    # 2. LOGO & TITLE
    try:
        st.image("assets/logo.jpg", use_container_width=True)
    except:
        st.write(get_text("splash_logo_missing", st.session_state.lang))
    
    st.markdown(f'<h1 class="glitch-text" style="font-size: 2.5em; margin-top: 20px;">{get_text("splash_title", st.session_state.lang)}</h1>', unsafe_allow_html=True)
    st.caption(get_text("splash_subtitle", st.session_state.lang))
    
    # 3. SCROLLING MATRIX TEXT
    scroll_text = get_text("splash_scroll_text", st.session_state.lang).replace("\n", "<br>")
    st.markdown(f"""
    <div class="splash-scroll-container">
        <div class="splash-scroll-content">
            {scroll_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(get_text("splash_init_btn", st.session_state.lang)):
        with st.spinner(get_text("loading_modules", st.session_state.lang)):
            time.sleep(1.5)
        go_to_calibration()
    
    # Removed install instructions as per previous request
    show_install_instructions(st.session_state.lang)


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
            # Lat/Lon persistence would ideally be here too, but for MVP falling back to default or re-entry is okay 
            # if we don't change cookie structure.
            # actually better to load it if we saved it, but schema might break old cookies. 
            # Let's simple init:
            user = UserEntity(saved_profile["name"], saved_profile["dob_year"], saved_profile["dob_month"], saved_profile["dob_day"], 12, saved_profile["phone"]) # Defaults lat/lon in class
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
            
        
    with st.expander(get_text("cal_region_label", LANG), expanded=True):
        d = st.date_input(get_text("cal_date_label", LANG), value=def_date, min_value=datetime.date(1901, 1, 1), max_value=datetime.date.today())
        h = 12 
        
        country_list = list(LOCATIONS.keys())
        # Default to China
        c_index = 0
        for i, c in enumerate(country_list):
            if "China" in c:
                c_index = i
                break
                
        sel_country = st.selectbox(get_text("cal_country", LANG), country_list, index=c_index)
        
        city_list = list(LOCATIONS[sel_country].keys())
        sel_city = st.selectbox(get_text("cal_city", LANG), city_list)
        
        # Get coords
        lat, lon = get_coordinates(sel_country, sel_city) 

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
                user = UserEntity(name, d.year, d.month, d.day, h, phone, lat=lat, lon=lon)
                st.session_state.user_data = user
                go_to_radiant()
    st.markdown('</div>', unsafe_allow_html=True)


def screen_radiant():
    user = st.session_state.user_data
    
    eastern = get_eastern_coordinates(user)
    western = get_western_coordinates(user, lang=LANG)
    chaos = get_chaos_parameters(user.entropy_seed)
    
    # 1. STATUS WIDGET (Top Right Floating)
    st.markdown(f"""
    <div class="status-widget">
        <div class="status-line">
            <span>{get_text("rad_connected", LANG)}:</span>
            <span style="color: #fff;">{user.name}</span>
        </div>
        <div class="status-line">
            <span>{get_text("rad_entropy_state", LANG)}:</span>
            <span style="color: var(--chaos-orange);">{chaos["entropy_state"]}</span>
        </div>
        <!-- Dynamic Waveform -->
        <div class="waveform">
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. EASTERN VECTOR (Tech Frame Cyan)
    st.markdown(f"""
    <div class="tech-frame tf-cyan">
        <div class="tech-header tf-cyan">{get_text("rad_west_title", LANG).replace("Western", "Eastern").replace("西方", "东方")}</div>
        <div class="metric-grid">
            <div class="metric-box" style="border: 1px solid var(--order-blue); box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.2);">
                <div class="metric-label">{get_text('rad_day_master', LANG)}</div>
                <div class="metric-value-east">{eastern['day_master']}</div>
            </div>
            <div class="metric-box" style="border: 1px solid var(--order-blue); box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.2);">
                <div class="metric-label">{get_text('rad_animal', LANG)}</div>
                <div class="metric-value-east">{eastern['animal']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CENTRAL LOGO (Visual Key)
    st.markdown('<div style="text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
    try:
        st.image("assets/logo.jpg", use_container_width=True) 
    except:
        pass
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. WESTERN VECTOR (Tech Frame Orange)
    st.markdown(f"""
    <div class="tech-frame tf-orange">
        <div class="tech-header tf-orange">{get_text("rad_west_title", LANG)}</div>
        <div class="metric-grid">
            <div class="metric-box" style="border: 1px solid var(--chaos-orange); box-shadow: inset 0 0 15px rgba(255, 107, 0, 0.2);">
                <div class="metric-label">{get_text('rad_sun', LANG)}</div>
                <div class="metric-value-west">{western['sun']}</div>
            </div>
            <div class="metric-box" style="border: 1px solid var(--chaos-orange); box-shadow: inset 0 0 15px rgba(255, 107, 0, 0.2);">
                <div class="metric-label">{get_text('rad_moon', LANG)}</div>
                <div class="metric-value-west">{western['moon']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # TABS
    tab_void, tab_lens = st.tabs([get_text("rad_tab_void", LANG), get_text("rad_tab_lens", LANG)])
    
    with tab_void:
        # 4. CRYSTAL ORB CONTAINER
        st.markdown('<div class="crystal-orb-container"><div class="orb-ring"></div>', unsafe_allow_html=True)
        query = st.text_input(get_text("void_input_label", LANG), placeholder=get_text("void_input_placeholder", LANG))
        st.markdown('</div>', unsafe_allow_html=True)

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
        
        # DUAL INPUT STRATEGY FOR MOBILE COMPATIBILITY
        # 1. Streamlit Camera Input (Works well on Desktop/modern browsers)
        cam_file = st.camera_input(get_text("lens_cam_label", LANG))
        
        # 2. File Uploader (Fallback: Triggers native OS camera picker on mobile)
        upload_file = st.file_uploader(get_text("lens_upload_label", LANG), type=['jpg', 'jpeg', 'png'])
        
        # Prioritize Camera, then Upload
        img_file = cam_file if cam_file else upload_file
        
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
