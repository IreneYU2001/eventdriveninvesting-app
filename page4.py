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
- **WRDS Financial Database** (Price and Volume Data)
- **Macroeconomic Indicators** (GDP, CPI, Unemployment Rate from FRED)
- **Event Data** (Earnings Announcements, Dividends, Mergers)
""")

st.header("3. Model Architecture")
st.image("resources/model/lstm_architecture.png", caption="Simplified LSTM Architecture", use_column_width=True)

st.header("4. Training Parameters")
training_params = {
    "Epochs": 100,
    "Batch Size": 64,
    "Optimizer": "Adam",
    "Loss Function": "MSE",
}
st.table(training_params)

st.header("5. Model Performance")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("MSE", "0.0007")
with col2:
    st.metric("MAE", "0.018")
with col3:
    st.metric("R² Score", "0.87")

st.header("6. Limitations & Considerations")
st.warning("""
- Model performance is validated only on S&P 500 companies.
- Highly volatile stocks or newly IPO'd stocks may result in lower prediction accuracy.
- External shocks (e.g., financial crises) are not explicitly modeled.
""")

st.divider()

# --- Display source code ---
with st.expander("📜 View Source Code of This Page"):
    current_file = os.path.basename(__file__)
    with open(current_file, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")

st.divider()

# --- Navigation ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page3.py")
with col2:
    st.write("")  # No next page after this
