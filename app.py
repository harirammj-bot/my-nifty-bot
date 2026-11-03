import streamlit as st
from kiteconnect import KiteConnect

# 1. பக்க வடிவமைப்பு 
st.set_page_config(layout="wide", page_title="Nifty Live Options Algo Bot")

# 2. உங்கள் Zerodha API விவரங்கள்
API_KEY = "0p8jmlee4u8qm0ks"
API_SECRET = "yyfj06ipmy0o2tnyqayxlgmyjxmutctt"

# KiteConnect கிளையன்ட் தொடங்குதல்
try:
    kite = KiteConnect(api_key=API_KEY)
except Exception as e:
    st.error(f"Kite Connect தொடங்குவதில் பிழை: {e}")

st.title("📊 Nifty 50 வர்த்தக கட்டுப்பாட்டுப் பலகை")

# இரு பிரிவுகளாகப் பிரித்தல் (Layout Columns)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔐 Zerodha லாகின் மேலாண்மை")
    
    # பிழை தராத எளிய அசல் Streamlit லாகின் பட்டன் லிங்க்
    login_url = f"https://zerodha.com{API_KEY}&v=3"
    
    st.link_button("🎯 Zerodha-வுடன் இணைக்க இங்கே கிளிக் செய்யவும்", login_url, use_container_width=True)
    
    st.write("")
    # லாகின் செய்த பின் கிடைக்கும் Request Token-ஐ உள்ளிட பாக்ஸ்
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
    
    # மொபைலில் பிளாக் ஆகாத அசல் லிங்க் பட்டன்
    direct_chart_url = "https://tradingview.com"
    
    st.link_button("🖥️ Nifty 50 நேரடி வரைபடத்தைத் திறக்கவும்", direct_chart_url, use_container_width=True)

    st.write("")
    st.info("குறிப்பு: மேலே உள்ள பட்டனை அழுத்தினால் மொபைலில் TradingView சார்ட் தனியாகப் பிழையின்றித் திறக்கும்.")
