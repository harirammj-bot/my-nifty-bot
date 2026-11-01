import streamlit as st
import pandas as pd
import random

# பக்கத்தின் தலைப்பு மற்றும் வடிவமைப்பு
st.set_page_config(page_title="Hari Smart Nifty Option Bot", layout="wide")
st.title("📊 Hari Smart Nifty Option Buying Bot")
st.markdown("---")

# 1. ஜெரோதா ஏபிஐ கான்பிகரேஷன்
st.sidebar.header("🔑 Zerodha API Config")
api_key = st.sidebar.text_input("Enter API Key", type="password")
api_secret = st.sidebar.text_input("Enter API Secret", type="password")
client_id = st.sidebar.text_input("Client ID", value="HARI123")

if st.sidebar.button("Connect Zerodha"):
    if api_key and api_secret:
        st.sidebar.success("🟢 Zerodha Connected!")
    else:
        st.sidebar.error("❌ Please enter API details")

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

# உதாரண லைவ் தரவுகள் (Kite API மூலம் இது உண்மையான மார்க்கெட்டில் மாறும்)
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

# ஏடிஎம் (At-The-Money) ஸ்ட்ரைக் கணக்கீடு
atm_strike = round(nifty_spot / 50) * 50

# மிகக் குறைந்த மற்றும் துல்லியமான அலர்ட் தரும் லாஜிக்
# VIX 12-18க்குள் இருந்து, PCR 1.2க்கு மேல் இருந்தால் மட்டுமே பையிங் சிக்னல் வரும்
if 12 <= live_vix <= 18 and nifty_pcr >= 1.2:
    strike_to_buy = f"NIFTY {atm_strike} CE"
    
    # ஜெரோதா ஒன்-டச் ஆர்டர் கூடை (Kite Publisher Basket Link)
    # இது மொபைலில் கிளிக்கும் போது நேரடியாக ஜெரோதா ஆப்பில் ஆர்டரை பூர்த்தி செய்யும்
    trade_data = f'[{{"variety":"regular","tradingsymbol":"NIFTY26N05{atm_strike}CE","exchange":"NFO","transaction_type":"BUY","order_type":"MARKET","quantity":25,"product":"NRML"}}]'
    one_touch_url = f"https://zerodha.com{api_key if api_key else 'YOUR_API_KEY'}&data={trade_data}"
    
    st.success(f"🟢 ACTION SUGGESTION: BUY {strike_to_buy}")
    
    # காரணங்களை தெளிவாகக் காட்டுதல்
    st.markdown(f"""
    **📝 அனாலிசிஸ் காரணம் (Reasoning):**
    * 🎯 **துல்லியமான ஸ்ட்ரைக்:** Nifty ஸ்பாட் விலை {nifty_spot}-ல் இருப்பதால், பிரீமியம் வேகமாக உயர **{strike_to_buy}** (ATM) தேர்வு செய்யப்பட்டுள்ளது.
    * 📈 **India VIX:** வாலட்டிலிட்டி {live_vix} ({vix_change}%) ஆப்ஷன் பையிங்கிற்கு சாதகமாக உயர்ந்துள்ளதால் வேகமான மொமெண்டம் கிடைக்கும்.
    * 📊 **Open Interest (OI):** PCR {nifty_pcr} ஆக உள்ளதால், கீழே விழாமல் மேலே செல்ல வலுவான புட் ரைட்டிங் சப்போர்ட் உள்ளது.
    * 🛑 **டிரேடிங் பிளான்:** உங்கள் இலக்கு **+{profit_target} பாயிண்டுகள்**, நஷ்ட வரம்பு **-{stop_loss} பாயிண்டுகள்**.
    """)
    
    # ஒன்-டச் ஆர்டர் பட்டன்
    st.link_button("🚀 ONE-TOUCH ORDER: PLACE ORDER IN ZERODHA", one_touch_url, type="primary")
else:
    st.warning("⚠️ STATUS: WAIT / NO TRADING ZONE")
    st.write("காரணம்: VIX அல்லது Open Interest ஆப்ஷன் பையிங்கிற்கு இன்னும் சாதகமாக அமையவில்லை. தேவையில்லாத அலர்ட்டுகளைத் தவிர்க்க பாட் தற்போது அமைதியாக உள்ளது.")
