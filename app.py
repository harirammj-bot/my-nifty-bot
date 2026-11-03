import streamlit as st
from kiteconnect import KiteConnect

# 1. பக்க வடிவமைப்பு 
st.set_page_config(layout="wide", page_title="Nifty Live Options Algo Bot")

# 2. உங்கள் Zerodha API விவரங்கள்
API_KEY = "0p8jmlee4u8qm0ks"
API_SECRET = "yyfj06ipmy0o2tnyqayxlgmyjxmutctt"

# KiteConnect கிளையன்ட்
try:
    kite = KiteConnect(api_key=API_KEY)
except Exception as e:
    st.error(f"Kite Connect தொடங்குவதில் பிழை: {e}")

st.title("📊 Nifty 50 வர்த்தக கட்டுப்பாட்டுப் பலகை")

# இரு பிரிவுகளாகப் பிரித்தல் (Layout Columns)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔐 Zerodha லாகின் மேலாண்மை")
    
    # மொபைல் பிரவுசரில் சிக்கல் தராத எளிய லாகின் பட்டன் லிங்க்
    login_url = f"https://zerodha.com{API_KEY}&v=3"
    st.markdown(f'''
        <a href="{login_url}" target="_blank">
            <button style="
                background-color: #e33e33; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                width: 100%;">
                🎯 Zerodha-வுடன் இணைக்க இங்கே கிளிக் செய்யவும்
            </button>
        </a>
    ''', unsafe_allowed_html=True)
    
    st.write("")
    # லாகின் செய்த பின் கிடைக்கும் Request Token-ஐ மேனுவலாக உள்ளிட எளிய பாக்ஸ்
    req_token = st.text_input("லாகின் செய்த பின் கிடைக்கும் Request Token-ஐ இங்கே பேஸ்ட் செய்யவும்:")
    
    if st.button("Access Token உருவாக்கு", use_container_width=True):
        if req_token:
            try:
                data = kite.generate_session(req_token, api_secret=API_SECRET)
                st.success("வாழ்த்துகள்! Zerodha வெற்றிகரமாக இணைக்கப்பட்டுவிட்டது.")
                st.json({"status": "Connected", "user_id": data.get("user_id")})
            except Exception as e:
                st.error(f"இணைப்பதில் பிழை: {e}. தயவுசெய்து புதிய டோக்கனைப் பயன்படுத்தவும்.")
        else:
            st.warning("தயவுசெய்து Request Token-ஐ உள்ளிடவும்.")

with col2:
    st.subheader("📈 TradingView விளக்கப்படம் (Chart)")
    st.warning("பிரவுசர் கட்டுப்பாடுகளால் மொபைலில் சார்ட் லோட் ஆகவில்லை என்றால், கீழே உள்ள லிங்க்கைப் பயன்படுத்தி புதிய டேபில் (New Tab) நேரடி வரைபடத்தைப் பார்க்கலாம்.")
    
    # மாற்று வழி: மொபைல் பிரவுசர்களில் பிளாக் ஆகாத அதிகாரப்பூர்வ மாற்று லிங்க்
    direct_chart_url = "https://tradingview.com"
    st.markdown(f'''
        <a href="{direct_chart_url}" target="_blank">
            <button style="
                background-color: #2962ff; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                width: 100%;">
                🖥️ Nifty 50 நேரடி வரைபடத்தைத் திறக்கவும்
            </button>
        </a>
    ''', unsafe_allowed_html=True)

    st.write("")
    # உள்ளமைக்கப்பட்ட மாற்று Iframe (பாதுகாப்பான சாண்ட்பாக்ஸ் உடன்)
    try:
        embed_url = "https://tradingview.com"
        st.components.v1.iframe(embed_url, height=450, scrolling=False)
    except:
        st.info("உங்களது மொபைல் பிரவுசர் iframe-ஐத் தடுக்கிறது.")
