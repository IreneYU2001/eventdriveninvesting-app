import streamlit as st
import os

st.markdown("""
<h1 style='line-height:1.4;'>
Model Overview:<br>
LSTM-Based Architecture for Financial Time Series Prediction
</h1>
""", unsafe_allow_html=True)

st.header("1. Model Introduction")
st.write("""
Built on Long Short-Term Memory (LSTM) Recurrent Neural Network (RNN), our model captures time-dependent patterns in financial markets,
combining deep learning with structured and unstructured data for enhanced short-term volatility and trading volume prediction.
""")

st.header("2. Training Data Sources")
st.markdown("""
- **Financial Database** (Price, Volume, Financial Statement and Earnings Announcements Data from WRDS)
- **Fundamental Data** (e.g., ROE, ROA, P/E Ratio, etc. from WRDS)
- **Technical Indicators** (e.g., Moving Averages, Bollinger Bands, etc. from WRDS)
- **Market Data** (e.g., VIX, SP500, etc. from WRDS)
- **Corporate Actions** (e.g., Stock Splits, Dividends, etc. from  WRDS)
- **Macroeconomic Indicators** (e.g., GDP, CPI, Unemployment Rate etc. using FRED API)
- **Financial News** (Company news using BENZINGA API → Sentiment Score through FinBERT)
""", unsafe_allow_html=True)

st.header("3. Dataset Description")
st.image("dataset description.png", caption="What Does Our Dataset Look Like", use_container_width=True)

st.header("4. Model Architecture")
st.image("model_fold1.png", caption="**LSTM_Volume Architecture**", use_container_width=True)
# Volume model section
st.markdown("""
<p style='font-size:25px'><b>Features used for training the model include:</b></p>

- **Input 1**: Sequential log volume [lag_1 to lag_10 (log-transformed volume from the previous 1 to 10 days per sticker) ] → Bi-LSTM → Multi-Head Attention  
- **Input 2**: Calendar (e.g., weekday, month, is_month_end, etc.) + rolling features(e.g., 7-day moving average/stdev of raw volume) → Dense(32) + Dropout  
- **Concatenated → Dense(64) + Dropout → Output: predicted log_volume (log_volume)**
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)

st.image("model_architecture.png", caption="**LSTM_Volatility Architecture**", use_container_width=True)

# Volatility model section
st.markdown("""
<p style='font-size:25px'><b>Features used for training the model include:</b></p>

- **Input 1**: Numerical features (e.g., PRC, Log_Return, GDP, VIX, ROE, etc.) → Dense(64) + ReLU → Dropout(0.2)  
- **Input 2**: Categorical features (execid, distcd) → Embedding layers → Flatten  
- **Input 3**: Sentiment feature (sentiment_score) → Dense(16) + ReLU  
- **Concatenated → Dense(64) + ReLU → Dropout(0.2) → Output: Predicted 5-day volatility (Volatility_5d)**
""", unsafe_allow_html=True)       

st.header("5. Model Summary")
st.image("volume.png", caption="Model Summary for Volume Prediction", use_container_width=True)
st.image("Volatility.png", caption="Model Summary for Volatility Prediction", use_container_width=True)


st.header("6. Limitations & Considerations")
st.warning("""
-The model shows limited predictive accuracy due to suboptimal feature selection, particularly missing key drivers of trading volume.

-Important factors influencing volume changes, such as intraday news flow, or institutional activity other than dividends, are not adequately captured.

-The model may underperform on stocks where volume is driven by context-specific factors not reflected in the input features
""")

st.header("7. Future Work")
st.markdown("""
- **Feature Engineering**: Explore additional features like intraday trading patterns, order book data, and alternative data sources (e.g., social media sentiment).
- **Model Enhancement**: Experiment with advanced architectures like Transformer-based models or hybrid models combining LSTM with CNNs for better feature extraction.
- **Hyperparameter Tuning**: Optimize hyperparameters using techniques like grid search or Bayesian optimization to improve model performance.
- **Ensemble Learning**: Combine predictions from multiple models to enhance robustness and accuracy.""", unsafe_allow_html=True)

st.divider()


# --- Navigation ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page2.py")
with col2:
    st.write("")  # No next page after this
