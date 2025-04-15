import streamlit as st
import requests
import base64
import os

# Set Streamlit page config
st.set_page_config(page_title="Currency Converter", page_icon="💱")

# Background image setup
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call this with your uploaded file path
add_bg_from_local("Untitled design.jpg")

# Title and info
st.title("💱 Currency Converter")

# Get currency symbols
@st.cache_data
def get_currency_symbols():
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except:
        return {}

symbols = get_currency_symbols()

currency_display = []
currency_code_map = {}

for code in sorted(symbols.keys()):
    name = symbols[code]
    display = f"{code} - {name}"
    currency_display.append(display)
    currency_code_map[display] = code

if not currency_display:
    st.error("Currency symbols could not be loaded. Please check your internet or try again later.")
    st.stop()

default_from = next((i for i, d in enumerate(currency_display) if "USD" in d), 0)
default_to = next((i for i, d in enumerate(currency_display) if "INR" in d), 1)

col1, col2 = st.columns(2)
with col1:
    from_display = st.selectbox("From Currency", currency_display, index=default_from)
with col2:
    to_display = st.selectbox("To Currency", currency_display, index=default_to)

from_currency = currency_code_map[from_display]
to_currency = currency_code_map[to_display]

amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount  # No conversion needed
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"].get(to_currency, None)


if st.button("Convert"):
    result = convert_currency(amount, from_currency, to_currency)
    if result is not None:
        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    else:
        st.error("Conversion failed. Please try again later.")
