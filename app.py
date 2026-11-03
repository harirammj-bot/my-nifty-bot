import streamlit as st
import streamlit.components.v1 as components
from kiteconnect import KiteConnect
import os

# 1. பக்க வடிவமைப்பு (Wide screen)
st.set_page_config(layout="wide", page_title="Automated Trading Bot")

# 2. உங்கள் Zerodha API விவரங்கள் (தானாகவே லோட் ஆகும்படி சேமிக்கப்பட்டுள்ளது)
API_KEY = "0p8jmlee4u8qm0ks"
API_SECRET = "yyfj06ipmy0o2tnyqayxlgmyjxmutctt"

# டோக்கனைத் தற்காலிகமாகச் சேமிக்க ஒரு கோப்பு (File)
TOKEN_FILE = "access_token.txt"

@st.cache_resource
def get_kite_client():
    return KiteConnect(api_key=API_KEY)

kite = get_kite_client()

# செஷன் (Session) மேலாண்மை
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        saved_token = f.read().strip()
    if saved_token:
        kite.set_access_token(saved_token)
        st.sidebar.success("Zerodha கணக்கு தானாகவே இணைக்கப்பட்டது! (Access Token Loaded)")

# ஒருவேளை பழைய டோக்கன் வேலை செய்யவில்லை என்றால் மட்டும் Sidebar-ல் லாகின் செய்யலாம்
st.sidebar.title("Zerodha Auto Login")
login_url = kite.login_url()
st.sidebar.markdown(f"[இங்கே கிளிக் செய்து Zerodha லாகின் செய்யவும்]({login_url})")

# URL-ல் இருந்து Request Token ஐத் தானாகவே எடுக்கும் முறை
query_params = st.query_params
if "request_token" in query_params:
    req_token = query_params["request_token"]
    try:
        data = kite.generate_session(req_token, api_secret=API_SECRET)
        access_token = data["access_token"]
        kite.set_access_token(access_token)
        # நிரந்தரமாகச் சேமித்தல்
        with open(TOKEN_FILE, "w") as f:
            f.write(access_token)
        st.sidebar.success("புதிய Session உருவாக்கப்பட்டுச் சேமிக்கப்பட்டது!")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Login செய்வதில் பிழை: {e}")

# 3. TradingView Chart (வெற்றுப் பக்கமாகத் தெரிவதைத் தடுக்கும் புதிய Iframe முறை)
st.title("📊 Nifty 50 நேரடி விளக்கப்படம் (Live Chart)")

# உறுதியாக வேலை செய்யக்கூடிய எளிய Iframe Chart
chart_url = "https://tradingview.com"

# Streamlit-ல் Chart-ஐக் காண்பித்தல்
components.iframe(chart_url, height=650, scrolling=False)

# 4. Trading Bot சிக்னல்கள் (Signals Place)
st.subheader("🤖 வர்த்தக சிக்னல்கள் மற்றும் விழிப்பூட்டல்கள் (Trading Signals)")
st.info("இங்கு உங்களின் 20-point Target மற்றும் 10-point Stoploss உத்திகளின் சிக்னல்கள் தோன்றும்.")
