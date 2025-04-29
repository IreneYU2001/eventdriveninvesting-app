import streamlit as st

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .section-container-red {
        border: 2px solid #F5B7B1; 
        border-radius: 12px;
        margin-bottom: 30px;
        overflow: hidden;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    .section-title-red {
        background-color: #FADBD8; 
        padding: 15px;
        font-size: 26px;
        font-weight: bold;
        color: black;
        text-align: center;
    }

    .section-container-green {
        border: 2px solid #A9DFBF; 
        border-radius: 12px;
        margin-bottom: 30px;
        overflow: hidden;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    .section-title-green {
        background-color: #D5F5E3; 
        padding: 15px;
        font-size: 26px;
        font-weight: bold;
        color: black;
        text-align: center;
    }

    .section-content {
        background-color: #ffffff;
        padding: 20px;
        font-size: 18px;
        color: #333333;
        line-height: 1.6;
    }

    .final-section {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        font-size: 20px;
        text-align: center;
        color: black;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }

    /* Start Button */
    .start-button-container {
        display: flex;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 50px;
    }
    .start-button-container button {
        background-color: #58D68D;
        color: white;
        font-size: 26px;
        padding: 16px 50px;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .start-button-container button:hover {
        background-color: #45B39D;
    }
    </style>
""", unsafe_allow_html=True)

# --- Big Welcome Title ---
st.markdown('<h1 style="text-align:center; color:black;"> Welcome to the Event-Driven Investing App!</h1>', unsafe_allow_html=True)

st.markdown("---")

# --- About This App Section (Red) ---
st.markdown("""
<div class="section-container-red">
    <div class="section-title-red">📚 What This App Can Do</div>
    <div class="section-content">
        This application helps investors optimize their trading strategies by leveraging stock-related events. 
        We collect financial events linked to specific companies, including breaking news, corporate actions, macroeconomic changes etc. and use predictive modeling to forecast each stock’s 
        <strong>future trading volume</strong> and <strong>volatility</strong>. Based on these predictions, we provide strategic insights to support smarter investment decisions.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Understanding Volume and Volatility Section (Green) ---
st.markdown("""
<div class="section-container-green">
    <div class="section-title-green">📊 Why We Use Volume & Volatility</div>
    <div class="section-content">
        <strong>Volume</strong> measures the number of shares traded in a specific period. 
        Higher trading volume often signals stronger investor interest and higher market liquidity, meaning it's easier to enter or exit a position without affecting the stock price.
        <br><br>
        <strong>Volatility</strong> reflects how much the price of a stock moves over time.. 
        High volatility implies larger and more frequent price swings, which often indicate both greater investment opportunities and higher risk.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Our Prediction Model Section (Red) ---
st.markdown("""
<div class="section-container-red">
    <div class="section-title-red">🤖 How Prediction Works</div>
    <div class="section-content">
        To anticipate how stocks react after news events, we use a 
        <strong>Long Short-Term Memory (LSTM)</strong> neural network, which excel at recognizing time-series pattern. We train our model using historical datasets that combine financial events, stock prices, and trading volumes. By learning patterns from past events and market behaviors, the model can recognize time-series relationships and generate more accurate forecasts for future stock movements.
    </div>
</div>
""", unsafe_allow_html=True)


# --- Final Encouragement Section (No Border, White Background, No line break) ---
st.markdown("""
<div class="final-section" style="white-space: nowrap;">
    🚀 Let data-driven insights power your next investment move. Welcome aboard!
</div>
""", unsafe_allow_html=True)


# --- Start Now Button ---
st.markdown("---")
st.markdown("<h3 style='text-align:center;'>Ready to begin?</h3>", unsafe_allow_html=True)


# --- Centered big button ---
# Create empty space columns to center
col1, col2, col3 = st.columns([6, 8, 7])

with col2:
    start_now = st.button("👉Start Now ", use_container_width=True)

if start_now:
    st.switch_page("page1.py")