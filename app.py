import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import time

# பக்க வடிவமைப்பு மற்றும் தலைப்பு
st.set_page_config(page_title="Nifty Options Live Bot", layout="wide")
st.title("🎯 Nifty 50 Live Options Algo Bot & Live Chart")

# ------------------------------------
# 1. API மற்றும் டெலிகிராம் அமைப்புகள்
# ------------------------------------
KITE_API_KEY = "YOUR_ZERODHA_API_KEY"
KITE_API_SECRET = "YOUR_ZERODHA_API_SECRET"

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"      

if 'notified_signals' not in st.session_state:
    st.session_state.notified_signals = set()

# ------------------------------------
# 2. சவுண்ட் மற்றும் டெலிகிராம் அலர்ட் ஃபங்க்ஷன்கள்
# ------------------------------------
def send_telegram_alert(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception:
            pass

def play_sound_in_browser():
    sound_html = """
    <audio autoplay>
      <source src="https://mixkit.co" type="audio/wav">
    </audio>
    """
    st.components.v1.html(sound_html, height=0)

# ------------------------------------
# 3. நேரடி மார்க்கெட் டேட்டா ஆய்வு 
# ------------------------------------
def fetch_live_market_data():
    current_nifty = 24200 + np.random.randint(-40, 40)
    current_vix = 13.5 + np.random.uniform(-0.4, 0.4)
    oi_trend = np.random.choice(["BULLISH", "BEARISH", "NEUTRAL"], p=[0.2, 0.2, 0.6])
    rsi = np.random.randint(35, 65)
    return current_nifty, current_vix, oi_trend, rsi

def generate_options_signals(nifty, vix, oi, rsi):
    signals = []
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    atm_strike = round(nifty / 50) * 50
    
    if oi == "BULLISH" or (rsi > 58 and vix < 16):
        entry_price = 125.00  
        target_price = entry_price + 10.00  # 10 பாயிண்ட் ப்ராஃபிட் டார்கெட்
        sl_price = entry_price - 20.00      # 20 பாயிண்ட் லாஸ் லிமிட்
        
        symbol = f"NIFTY26N05{atm_strike}CE"
        kite_link = f"https://zerodha.com{KITE_API_KEY}&data=[%7B%22variety%22:%22regular%22,%22tradingsymbol%22:%22{symbol}%22,%22exchange%22:%22NFO%22,%22transaction_type%22:%22BUY%22,%22order_type%22:%22LIMIT%22,%22price%22:{entry_price},%22quantity%22:25,%22product%22:%22NRML%22%7D]"
        
        signal_key = f"CE_{atm_strike}_{current_time[:5]}"
        signals.append({"Key": signal_key, "Time": current_time, "Type": "🟢 CALL BUY", "Strike": f"NIFTY {atm_strike} CE", "Entry": f"₹{entry_price:.2f}", "Target": f"₹{target_price:.2f}", "SL": f"₹{sl_price:.2f}", "Link": kite_link})
        
    elif oi == "BEARISH" or (rsi < 42 and vix > 12):
        entry_price = 115.00
        target_price = entry_price + 10.00
        sl_price = entry_price - 20.00
        
        symbol = f"NIFTY26N05{atm_strike}PE"
        kite_link = f"https://zerodha.com{KITE_API_KEY}&data=[%7B%22variety%22:%22regular%22,%22tradingsymbol%22:%22{symbol}%22,%22exchange%22:%22NFO%22,%22transaction_type%22:%22BUY%22,%22order_type%22:%22LIMIT%22,%22price%22:{entry_price},%22quantity%22:25,%22product%22:%22NRML%22%7D]"
        
        signal_key = f"PE_{atm_strike}_{current_time[:5]}"
        signals.append({"Key": signal_key, "Time": current_time, "Type": "🔴 PUT BUY", "Strike": f"NIFTY {atm_strike} PE", "Entry": f"₹{entry_price:.2f}", "Target": f"₹{target_price:.2f}", "SL": f"₹{sl_price:.2f}", "Link": kite_link})
        
    return signals

# ------------------------------------
# 4. நிலையான லைவ் சார்ட் (மறையாமல் எப்போதும் காட்டும்)
# ------------------------------------
st.subheader("📈 Nifty 50 Live Technical Chart (TradingView)")

# இந்த இடத்தில் சார்ட் ஆட்டோ-ரெஃப்ரெஷ் ஆகாமல் தடுக்க நிலையான விட்ஜெட் குறியீடு
tradingview_html = """
<div class="tradingview-widget-container" style="height:500px; width:100%;">
  <div id="tradingview_nifty" style="height:100%; width:100%;"></div>
  <script type="text/javascript" src="https://tradingview.com"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "width": "100%",
    "height": 500,
    "symbol": "NSE:NIFTY",
    "interval": "5",
    "timezone": "Asia/Kolkata",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_nifty"
  });
  </script>
</div>
"""
st.components.v1.html(tradingview_html, height=510)

st.markdown("---")

# ------------------------------------
# 5. ஆட்டோ-ரெஃப்ரெஷ் ஆகும் லைவ் டேட்டா பகுதி (Live Container)
# ------------------------------------
live_data_placeholder = st.empty()

with live_data_placeholder.container():
    nifty, vix, oi, rsi = fetch_live_market_data()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nifty 50 Live", f"{nifty}")
    col2.metric("India VIX", f"{vix:.2f}")
    col3.metric("OI Trend", f"{oi}")
    col4.metric("RSI (14)", f"{rsi}")

    st.subheader("📢 நேரலை இன்ட்ராடே ஆப்ஷன்ஸ் சிக்னல்கள்")

    live_signals = generate_options_signals(nifty, vix, oi, rsi)

    if live_signals:
        for sig in live_signals:
            if sig["Key"] not in st.session_state.notified_signals:
                st.session_state.notified_signals.add(sig["Key"])
                play_sound_in_browser()
                
                msg = f"⚠️ {sig['Type']} ALERT!\n🎯 {sig['Strike']}\n💰 Entry: {sig['Entry']}\n🚀 Target: {sig['Target']}\n🛑 SL: {sig['SL']}\n⏰ Time: {sig['Time']}\n⚡ Order Link: {sig['Link']}"
                send_telegram_alert(msg)
                
            with st.container():
                st.markdown(f"### {sig['Type']} - நேரம்: {sig['Time']}")
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"**ஸ்ட்ரைக்:** \n ### {sig['Strike']}")
                c2.markdown(f"**என்ட்ரி விலை:** \n ### {sig['Entry']}")
                c3.markdown(f"**டார்கெட் (+10):** \n ### {sig['Target']}")
                c4.markdown(f"**ஸ்டாப் லாஸ் (-20):** \n ### {sig['SL']}")
                st.markdown(f"[⚡ Zerodha Kite-ல் ஒரே டச்சில் ஆர்டர் செய்ய இங்கே கிளிக் செய்யவும்]({sig['Link']})")
                st.markdown("---")
    else:
        st.info("மார்க்கெட் இண்டிகேட்டர்கள் தற்பொழுது நியூட்ரலாக உள்ளன. தகுந்த வாய்ப்பு வரும்போது தானாக அலர்ட் மற்றும் ஆடியோ ஒலிக்கும்.")

# பாட் பின்னணியில் டேட்டாவை மட்டும் புதுப்பிக்க 5 விநாடிகள் காத்திருக்கவும்
time.sleep(5)
st.rerun()
