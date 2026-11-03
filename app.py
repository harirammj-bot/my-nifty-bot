import streamlit as st
import streamlit.components.v1 as components
from kiteconnect import KiteConnect

# Streamlit பக்க வடிவமைப்பு
st.set_page_config(layout="wide", page_title="Zerodha Trading Bot")

# 1. Zerodha API சான்றுகள் (Credentials)
API_KEY = "0p8jmlee4u8qm0ks"
API_SECRET = "yyfj06ipmy0o2tnyqayxlgmyjxmutctt"

# KiteConnect ஐத் தொடங்குதல்
try:
    kite = KiteConnect(api_key=API_KEY)
    st.sidebar.success("Zerodha API Key இணைக்கப்பட்டது!")
except Exception as e:
    st.sidebar.error(f"Kite Connect தொடங்குவதில் பிழை: {e}")

# Side bar-ல் பயனர் விவரங்கள் அல்லது Access Token பெறுவதற்கான வசதி
st.sidebar.title("கட்டுப்பாட்டுப் பலகை (Dashboard)")
request_token = st.sidebar.text_input("Enter Zerodha Request Token:")

if st.sidebar.button("Generate Session"):
    if request_token:
        try:
            data = kite.generate_session(request_token, api_secret=API_SECRET)
            kite.set_access_token(data["access_token"])
            st.sidebar.success("Session வெற்றிகரமாக உருவாக்கப்பட்டது!")
        except Exception as e:
            st.sidebar.error(f"Session உருவாக்குவதில் பிழை: {e}")
    else:
        st.sidebar.warning("தயவுசெய்து Request Token ஐ உள்ளிடவும்.")

# 2. TradingView Chart (Refused to Connect பிழையைத் தவிர்க்கும் அதிகாரப்பூர்வ விட்ஜெட்)
st.title("நிகழ்நேர வர்த்தக விளக்கப்படம் (Live Trading Chart)")

# TradingView HTML/JS கோட்
tradingview_html = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container" style="height:100%;width:100%">
  <div id="tradingview_chart"></div>
  <script type="text/javascript" src="https://tradingview.com"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "NSE:NIFTY",
    "interval": "5",
    "timezone": "Asia/Kolkata",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_chart"
  });
  </script>
</div>
<!-- TradingView Widget END -->
"""

# Streamlit பக்கத்தில் விளக்கப்படத்தைக் காண்பித்தல் (உயரம் மற்றும் அகலத்தை மாற்றி அமைக்கலாம்)
components.html(tradingview_html, height=600, scrolling=True)

# 3. உங்கள் விருப்பப்படி Trading Bot உத்திகள் (Strategies) மற்றும் Alerts-க்கான இடம்
st.subheader("வர்த்தக விழிப்பூட்டல்கள் மற்றும் ஆர்டர்கள் (Trading Alerts & Orders)")
st.write("இங்கு உங்களின் VIX, Open Interest மற்றும் Nifty 50 தரவுகளின் அடிப்படையிலான சிக்னல்கள் காண்பிக்கப்படும்.")
