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
-The model shows limited predictive accuracy due to suboptimal feature selection, particularly missing key drivers of trading volume.

-Important factors influencing volume changes, such as intraday news flow, investor sentiment, or institutional activity, are not adequately captured.

-The model may underperform on stocks where volume is driven by context-specific factors not reflected in the input features
""")

st.divider()


# --- Navigation ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page2.py")
with col2:
    st.write("")  # No next page after this
