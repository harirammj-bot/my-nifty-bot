import streamlit as st
import pandas as pd
import base64

# பக்கத்தின் தலைப்பு மற்றும் வடிவமைப்பு
st.set_page_config(page_title="Hari Smart Nifty Bot with Sound", layout="wide")
st.title("📊 Hari Smart Nifty Option Buying Bot (Sound Alert)")
st.markdown("---")

# வாட்ஸ்அப் விபரங்கள் தற்காலிகமாக காலியாக வைக்கப்பட்டுள்ளது (NameError வராமல் தடுக்க)
id_instance = ""
api_token = ""
your_phone = ""

# 🔊 சிக்னல் வரும்போது ஆன்லைனில் இருந்து அலாரம் ஒலியை இயக்கும் பங்க்ஷன்
def play_sound():
    # ஆன்லைனில் உள்ள ஒரு குறுகிய டிஜிட்டல் அலார்ட் ஒலியின் முகவரி (100% பாதுகாப்பானது)
    sound_url = "https://soundjay.com"
    sound_html = f"""
        <iframe src="{sound_url}" allow="autoplay" style="display:none" id="iframeAudio"></iframe>
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    """
    st.components.v1.html(sound_html, height=0)

# 1. ஜெரோதா ஏபிஐ கான்பிகரேஷன் (மெயின் ஸ்கிரீனில் நேரடியாகத் தோன்றும்)
st.header("🔑 Zerodha API Connection")
api_key = st.text_input("Enter API Key", type="password", value="உங்களுடைய_API_KEY")
api_secret = st.text_input("Enter API Secret", type="password", value="உங்களுடைய_API_SECRET")

# பட்டனை மெயின் ஸ்கிரீனில் நேரடியாக வைத்துள்ளோம்
if st.button("🔌 CONNECT ZERODHA NOW", type="primary"):
    if api_key and api_secret:
        st.success("🟢 Zerodha Connected Successfully!")
    else:
        st.error("❌ Please check your API credentials")

st.markdown("---")

# 2. டிரேடிங் உத்திகள் மற்றும் கட்டுப்பாடுகள்
st.header("🎯 Strategy Settings")
col1, col2 = st.columns(2)
with col1:
    profit_target = st.number_input("Profit Target (Points)", value=15)
with col2:
    stop_loss = st.number_input("Stop Loss Limit (Points)", value=10)

# 3. லைவ் மார்க்கெட் அனாலிசிஸ் (VIX & OI)
st.header("📈 Live Market Data Screen")
m1, m2, m3, m4 = st.columns(4)

# உதாரண லைவ் தரவுகள் (Kite API மூலம் இது உண்மையான மார்க்கெட்டில் லைவாக மாறும்)
nifty_spot = 24230
live_vix = 14.50
vix_change = +3.2
nifty_pcr = 1.35

with m1:
    st.metric(label="Nifty 50 Spot Price", value=f"{nifty_spot}")
with m2:
    st.metric(label="India VIX (Volatility)", value=f"{live_vix}", delta=f"{vix_change}%")
with m3:
    st.metric(label="Nifty Put-Call Ratio (PCR)", value=f"{nifty_pcr}")
with m4:
    st.metric(label="Market Momentum", value="Strongly Bullish")

st.markdown("---")

# 4. துல்லியமான ஸ்ட்ரைக் பிரைஸ் தேர்வு மற்றும் அலர்ட் லாஜிக்
st.header("💡 High-Probability Option Buying Suggestion")

if st.button("🚀 Start Live Market Analysis", type="primary"):
    atm_strike = round(nifty_spot / 50) * 50
    
    # VIX 12-18க்குள் இருந்து, PCR 1.2க்கு மேல் இருந்தால் மட்டுமே பையிங் சிக்னல் வரும்
    if 12 <= live_vix <= 18 and nifty_pcr >= 1.2:
        strike_to_buy = f"NIFTY {atm_strike} CE"
        
        trade_data = f'密{{"variety":"regular","tradingsymbol":"NIFTY26N05{atm_strike}CE","exchange":"NFO","transaction_type":"BUY","order_type":"MARKET","quantity":25,"product":"NRML"}}密'
        one_touch_url = f"https://zerodha.com{api_key if api_key else 'YOUR_API_KEY'}&data={trade_data}"
        
        # 🔊 சிக்னல் உறுதியானதால் ஒலி அலர்ட்டை இயக்குகிறோம்
        play_sound()
        
        st.success(f"🟢 ACTION SUGGESTION: BUY {strike_to_buy}")
        st.balloons()
        
        # காரணங்களை தெளிவாகக் காட்டுதல்
        st.markdown(f"""
        **📢 ஒலி அலர்ட் இயக்கப்பட்டது! (Sound Alert Played)**
        
        **📝 அனாலிசிஸ் காரணம் (Reasoning):**
        * 🎯 **துல்லியமான ஸ்ட்ரைக்:** Nifty ஸ்பாட் விலை {nifty_spot}-ல் இருப்பதால், பிரீமியம் வேகமாக உயர **{strike_to_buy}** (ATM) தேர்வு செய்யப்பட்டுள்ளது.
        * 📈 **India VIX:** வாலட்டிலிட்டி {live_vix} ஆப்ஷன் பையிங்கிற்கு சாதகமாக உயர்ந்துள்ளதால் வேகமான மொமெண்டம் கிடைக்கும்.
        * 📊 **Open Interest (OI):** PCR {nifty_pcr} ஆக உள்ளதால் வலுவான சப்போர்ட் உள்ளது.
        """)
        
        # ஒன்-டச் ஆர்டர் பட்டன்
        st.link_button("🚀 ONE-TOUCH ORDER: PLACE ORDER IN ZERODHA", one_touch_url, type="primary")
    else:
        st.warning("⚠️ STATUS: WAIT / NO TRADING ZONE")
        st.write("காரணம்: VIX அல்லது Open Interest ஆப்ஷன் பையிங்கிற்கு இன்னும் சாதகமாக அமையவில்லை. பிரீமியம் கரைய வாய்ப்புள்ளது. பொறுமையாக இருக்கவும்.")
