import streamlit as st
import requests
class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency not in self.currencies or to_currency not in self.currencies:
            raise ValueError("Invalid currency code.")
        if from_currency != 'USD':
            amount /= self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount
st.set_page_config(page_title="Currency Converter", layout="centered",page_icon="💱")
st.title("💱 Currency Converter")
url = "https://api.exchangerate-api.com/v4/latest/USD"
converter = RealTimeCurrencyConverter(url)
if converter.currencies:
    amount = st.number_input("Enter Amount:", min_value=0.0, step=0.01, format="%.2f")
    from_currency = st.selectbox("From:", list(converter.currencies.keys()), index=list(converter.currencies.keys()).index('USD'))
    to_currency = st.selectbox("To:", list(converter.currencies.keys()), index=list(converter.currencies.keys()).index('INR'))
    if st.button("Convert"):
        try:
            result = converter.convert(from_currency, to_currency, amount)
            st.success(f"{amount} {from_currency} = {result} {to_currency}")
        except ValueError as e:
            st.error(str(e))
