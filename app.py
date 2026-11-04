import streamlit as st
from kiteconnect import KiteConnect

st.set_page_config(layout="centered", page_title="Zerodha Fix")

API_KEY = "0p8jmlee4u8qm0ks"
API_SECRET = "yyfj06ipmy0o2tnyqayxlgmyjxmutctt"

st.title("⚡ Zerodha மொபைல் லாகின் தீர்வு")

try:
    kite = KiteConnect(api_key=API_KEY)
    login_url = kite.login_url()
    
    # 1. லாகின் பட்டன்
    st.link_button("🎯 மொபைலில் Zerodha லாகின் செய்ய கிளிக் செய்யவும்", login_url, use_container_width=True)
    
    st.write("")
    st.info("💡 **முக்கிய குறிப்பு:** லாகின் செய்த பிறகு உங்களுக்கு 'This site can’t be reached' என்று காட்டும். அந்தப் பக்கத்தின் மேலே இருக்கும் முகவரியை (URL) அப்படியே முழுமையாகக் காப்பி செய்து, கீழே உள்ள பாக்ஸில் பேஸ்ட் செய்யவும்.")
    
    # 2. முழு URL ஐப் பெற்று டோக்கனைப் பிரிக்கும் வசதி
    full_url = st.text_input("லாகின் செய்து பிழை காட்டிய அந்த முழு URL-ஐ இங்கே பேஸ்ட் செய்யவும்:")
    
    if st.button("அல்கோவை இணைக்கவும்", use_container_width=True):
        if full_url:
            # URL-ல் இருந்து request_token ஐத் தனியாக எடுக்கும் எளிய லாஜிக்
            try:
                if "request_token=" in full_url:
                    req_token = full_url.split("request_token=")[1].split("&")[0]
                    data = kite.generate_session(req_token, api_secret=API_SECRET)
                    st.success(f"வெற்றிகரமாக இணைக்கப்பட்டது! பயனர் ID: {data.get('user_id')}")
                else:
                    st.error("தவறான URL. இதில் request_token இல்லை.")
            except Exception as e:
                st.error(f"இணைப்பதில் பிழை: {e}")
        else:
            st.warning("தயவுசெய்து URL-ஐ உள்ளிடவும்.")

except Exception as e:
    st.error(f"அமைப்பில் பிழை: {e}")
