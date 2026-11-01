import streamlit as st
import pandas as pd
import requests

# பக்கத்தின் கட்டமைப்பு
st.set_page_config(page_title="Hari Smart Nifty Bot with WhatsApp", layout="wide")
st.title("📊 Hari Smart Nifty Option Bot (WhatsApp Alert)")
st.markdown("---")

# 1. ஜெரோதா மற்றும் வாட்ஸ்அப் ஏபிஐ கான்பிகரேஷன்
st.sidebar.header("🔑 Configuration Keys")
api_key = st.sidebar.text_input("Enter Zerodha API Key", type="password", value="உங்களுடைய_உண்மையான_API_KEY")
api_secret = st.sidebar.text_input("Enter Zerodha API Secret", type="password", value="உங்களுடைய_உண்மையான_API_SECRET")

st.sidebar.markdown("---")
st.sidebar.header("💬 WhatsApp Configuration")
id_instance = st.sidebar.text_input("Enter Green API ID Instance")
api_token = st.sidebar.text_input("Enter Green API Token Instance", type="password")
your_phone = st.sidebar.text_input("Enter Your WhatsApp Number (e.g., 919876543210)")

# 2. வாட்ஸ்அப் மெசேஜ் அனுப்பும் எளிய பைதான் பங்க்ஷன்
def send_whatsapp_alert(instance, token, phone, message_text):
    url = f"https://green-api.com{instance}/sendMessage/{token}"
    payload = {
        "chatId": f"{phone}@c.us",
        "message": message_text
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except:
        return False

# 3. ஸ்ட்ரேட்டஜி செட்டிங்ஸ்
st.header("🎯 Strategy Settings")
col1, col2 = st.columns(2)
with col1:
    profit_target = st.number_input("Profit Target (Points)", value=15)
with col2:
    stop_loss = st.number_input("Stop Loss Limit (Points)", value=10)

# 4. லைவ் மார்க்கெட் டேட்டா (உதாரண தரவுகள்)
nifty_spot = 24230
live_vix = 14.50
nifty_pcr = 1.35
atm_strike = round(nifty_spot / 50) * 50

st.markdown("---")
st.header("💡 Live Option Buying Suggestion")

if st.button("🚀 Start Analysis & Send Test WhatsApp Alert", type="primary"):
    if 12 <= live_vix <= 18 and nifty_pcr >= 1.2:
        strike_to_buy = f"NIFTY {atm_strike} CE"
        trade_data = f'密{{"variety":"regular","tradingsymbol":"NIFTY26N05{atm_strike}CE","exchange":"NFO","transaction_type":"BUY","order_type":"MARKET","quantity":25,"product":"NRML"}}密'
        one_touch_url = f"https://zerodha.com{api_key if api_key else 'YOUR_API_KEY'}&data={trade_data}"
        
        # வாட்ஸ்அப் மெசேஜ் வடிவம்
        whatsapp_msg = (
            f"🚀 HARI ALGO TRADING ALERT 🚀\n\n"
            f"🟢 ACTION: BUY {strike_to_buy}\n"
            f"📈 TARGET: +{profit_target} Points\n"
            f"📉 STOP LOSS: -{stop_loss} Points\n\n"
            f"📝 காரணம்:\n"
            f"• Nifty Spot: {nifty_spot}\n"
            f"• India VIX: {live_vix} (சாதகமாக உள்ளது)\n"
            f"• PCR: {nifty_pcr} (வலுவான சப்போர்ட்)\n\n"
            f"👇 ஒரே கிளிக்கில் ஆர்டர் செய்ய கிளிக் செய்யவும்:\n"
            f"{one_touch_url}"
        )
        
        st.success(f"🟢 BUY SUGGESTION GENERATED FOR {strike_to_buy}")
        
        # மெசேஜ் அனுப்பும் முயற்சி
        if id_instance and api_token and your_phone:
            status = send_whatsapp_alert(id_instance, api_token, your_phone, whatsapp_msg)
            if status:
                st.balloons()
                st.success("📱 WhatsApp Alert Sent Successfully to your Mobile!")
            else:
                st.error("❌ WhatsApp Alert Failed. Check your Green API details.")
        else:
            st.warning("⚠️ Please fill WhatsApp Config details in Sidebar to receive alert on Mobile.")
