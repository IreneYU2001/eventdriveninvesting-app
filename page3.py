import streamlit as st
import os
import random

st.title("📈 Predict Volatility & Trading Volume")

# Simulate prediction (replace with your LSTM model later)
ticker = st.text_input("Enter a stock ticker for prediction:")

if ticker:
    predicted_volatility = round(random.uniform(0.02, 0.07), 4)
    predicted_volume = random.randint(1000000, 10000000)

    st.metric("Predicted Volatility", f"{predicted_volatility}")
    st.metric("Predicted Volume", f"{predicted_volume:,}")

st.divider()

# Display source code
with st.expander("📜 View Source Code of This Page"):
    current_file = os.path.basename(__file__)
    with open(current_file, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")

st.divider()

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page2.py")
with col2:
    if st.button("Next Page ➡️"):
        st.switch_page("page4.py")