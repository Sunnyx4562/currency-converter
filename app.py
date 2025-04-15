import streamlit as st
import requests
import base64

# --- Streamlit page config ---
st.set_page_config(
    page_title="Currency Converter 💱",
    page_icon="💱",
    layout="centered"
)

# --- Background styling ---
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

add_bg_from_local("Untitled design.jpg")  # Use your background image

# --- Title Section ---
st.markdown(
    "<h1 style='text-align: center; color: #ffffff;'>💱 Currency Converter</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border-top: 2px solid #eee;'>", unsafe_allow_html=True)

# --- Fetching Currency Symbols ---
@st.cache_data
def get_currency_symbols():
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        if response.status_code == 200:
            return response.json()
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
    st.error("⚠️ Currency data couldn't be loaded. Please check your connection.")
    st.stop()

default_from = next((i for i, d in enumerate(currency_display) if "USD" in d), 0)
default_to = next((i for i, d in enumerate(currency_display) if "INR" in d), 1)

# --- Input Section ---
with st.container():
    st.markdown("### 🌍 Select Currencies")
    col1, col2 = st.columns(2)
    with col1:
        from_display = st.selectbox("From Currency", currency_display, index=default_from)
    with col2:
        to_display = st.selectbox("To Currency", currency_display, index=default_to)

    from_currency = currency_code_map[from_display]
    to_currency = currency_code_map[to_display]

    amount = st.number_input("💰 Enter Amount", min_value=0.0, value=1.0, step=0.1)

# --- Conversion Function ---
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"].get(to_currency, None)
    return None

# --- Conversion Result ---
st.markdown("### 💱 Convert")
convert_btn = st.button("💱 Convert Now", use_container_width=True)

if convert_btn:
    with st.spinner("Converting..."):
        result = convert_currency(amount, from_currency, to_currency)
        if result is not None:
            st.success(f" {amount} {from_currency} = **{result:.2f} {to_currency}**")
        else:
            st.error("❌ Conversion failed. Please try again.")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>Powered by <a href='https://www.frankfurter.app/' target='_blank'>Frankfurter API</a></p>",
    unsafe_allow_html=True
)
