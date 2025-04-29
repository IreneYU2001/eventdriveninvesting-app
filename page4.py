import streamlit as st
import os

st.title("🧠 Model Overview: LSTM-Based Stock Prediction")

st.header("1. Model Introduction")
st.write("""
Our model is based on a Long Short-Term Memory (LSTM) Recurrent Neural Network (RNN),
specially designed to capture sequential patterns in stock volatility and trading volume over time.
""")

st.header("2. Training Data Sources")
st.markdown("""
- **Financial Database** (Price, Volume, Financial Statement and Earnings Announcements Data from WRDS)
- **Macroeconomic Indicators** (GDP, CPI, Unemployment Rate etc. from FRED)
- **New** (Breaking Newa Related to Companies, Sentiment Analysis through FINBERT)
""")

st.header("3. Dataset Description")
st.image("dataset description.png", caption="What is Our Dataset Look Like", use_container_width=True)

st.header("4. Model Summary")
st.image("volume.png", caption="Model Summary for Volume Prediction", use_container_width=True)
st.image("Volatility.png", caption="Model Summary for Volatility Prediction", use_container_width=True)



st.header("6. Limitations & Considerations")
st.warning("""
- Model performance is validated only on S&P 500 companies.
- Highly volatile stocks or newly IPO'd stocks may result in lower prediction accuracy.
- External shocks (e.g., financial crises) are not explicitly modeled.
""")

st.divider()


# --- Navigation ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page2.py")
with col2:
    st.write("")  # No next page after this
