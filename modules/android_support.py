import streamlit as st
import base64
import json

def get_manifest_data_url():
    manifest = {
        "name": "Entropy God",
        "short_name": "EntropyGod",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#050508",
        "theme_color": "#050508",
        "icons": [
            {
                "src": "assets/logo.jpg",
                "sizes": "192x192",
                "type": "image/jpeg"
            },
             {
                "src": "assets/logo.jpg",
                "sizes": "512x512",
                "type": "image/jpeg"
            }
        ]
    }
    manifest_json = json.dumps(manifest)
    b64_manifest = base64.b64encode(manifest_json.encode()).decode()
    return f"data:application/manifest+json;base64,{b64_manifest}"

def inject_pwa_meta():
    """
    Injects PWA meta tags and manifest link into the Streamlit app.
    This makes the app installable on Android (Add to Home Screen).
    """
    manifest_url = get_manifest_data_url()
    
    # Meta tags for PWA
    meta_tags = f"""
    <!-- PWA Manifest -->
    <link rel="manifest" href="{manifest_url}">
    
    <!-- Android/Chrome -->
    <meta name="theme-color" content="#050508">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="application-name" content="Entropy God">
    
    <!-- iOS/Safari -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Entropy God">
    """
    
    st.markdown(meta_tags, unsafe_allow_html=True)

def show_install_instructions(lang="CN"):
    """
    Displays instructions on how to install the app on Android.
    """
    color = "#FF6B00" # chaos orange
    
    if lang == "CN":
        st.info("💡 **安装到手机**: 在 Chrome 浏览器菜单中点击 **'添加到主屏幕'** 即可像原生 App 一样使用。")
    else:
        st.info("💡 **Install App**: Tap browser menu -> **'Add to Home Screen'** to install as a native App.")
