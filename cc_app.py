import streamlit as st
import requests
class RealTimeCurrencyConverter():
    def __init__(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
            self.currencies = self.data.get('rates',{})
        except Exception as e:
            self.data = {}
            self.currencies = {}
            st.error(f"Error in fetching exchange rates{e}. Please Try Again Later!...")


    def convert(self, from_currency, to_currency, amount):
        if from_currency not in self.currencies or to_currency not in self.currencies:
            raise ValueError("Invalid currency code.")
        if from_currency != 'USD':
            amount /= self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount
st.set_page_config(page_title="Currency Converter", layout="centered",page_icon="💱")
st.title("💱 Currency Converter")
url = "https://open.er-api.com/v6/latest/USD"
converter = RealTimeCurrencyConverter(url)
if 'from_currency' not in st.session_state:
    st.session_state.from_currency = 'USD'
if 'to_currency' not in st.session_state:
    st.session_state.to_currency = 'INR'
if 'swap' not in st.session_state:
    st.session_state.swap = False
if st.session_state.swap:
    st.session_state.from_currency, st.session_state.to_currency = (st.session_state.to_currency, st.session_state.from_currency)
    st.session_state.swap = False
    st.rerun()
amount = st.number_input("Enter Amount:", min_value=0.0, step=0.01, format="%.2f")
current_list = list(converter.currencies.keys())
from_currency = st.selectbox("From:", current_list,index = current_list.index(st.session_state.from_currency),key='from_currency')
to_currency = st.selectbox("To:", current_list, index=current_list.index(st.session_state.to_currency),key='to_currency')
if amount is not None:
    try:
        result = converter.convert(from_currency, to_currency, amount)
        st.success(f"{amount} {from_currency} = {result} {to_currency}")
    except ValueError as e:
        st.error(str(e))
col1,col2 = st.columns(2)
with col1:
    if st.button("🔁 Swap Currencies"):
        st.session_state.swap = True
with col2:
    if st.button("Refresh Rates"):
        converter = RealTimeCurrencyConverter(url)
        st.success("Exchange rates Updated!")
        st.rerun()
last_updated = converter.data.get('time_last_update_utc','unknown')
st.caption(f"📅 Last updated: {last_updated}")

