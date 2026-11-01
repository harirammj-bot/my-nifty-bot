import streamlit as st

st.set_page_config(page_title="Hari Nifty Bot Test", layout="wide")
st.title("📊 Hari Smart Nifty Option Buying Bot")
st.markdown("---")

st.sidebar.header("🔑 Zerodha API Config")
api_key = st.sidebar.text_input("Enter API Key", type="password")
api_secret = st.sidebar.text_input("Enter API Secret", type="password")

if st.sidebar.button("Connect Zerodha"):
    st.sidebar.success("🟢 Zerodha Connected!")

st.write("🤖 Bot Screen is Active and Ready!")
