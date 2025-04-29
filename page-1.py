import streamlit as st

# --- Custom CSS Styling for Citation Page ---
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .section-container-red {
        background-color: #FADBD8;
        border: 2px solid #F5B7B1;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.06);
    }
    .section-container-green {
        background-color: #D5F5E3;
        border: 2px solid #A9DFBF;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.06);
    }
    .section-title {
        font-size: 30px;
        font-weight: bold;
        color: black;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-text {
        font-size: 18px;
        color: #333333;
        line-height: 1.8;
    }
    .divider {
        height: 2px;
        background-color: #cccccc;
        margin: 40px 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Big Page Title ---
st.markdown('<h1 style="text-align:center; color:black;">📖 Citations and Key Code</h1>', unsafe_allow_html=True)

st.markdown("---")

# --- Citation Section (Red) ---
st.markdown("""
<div class="section-container-red">
    <div class="section-title">📚 References and Citations</div>
    <div class="section-text">
        1. Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735–1780.<br><br>
        2. Yahoo Finance API Documentation.<br><br>
        3. Corporate Events Datasets (S&P Global, 2023).<br><br>
        4. "Stock Market Volatility Measurement," CFA Institute Research Foundation.
    </div>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Closing Line ---
st.markdown('<h3 style="text-align:center; color:gray; margin-top:50px;">Thank you for reading! 🚀</h3>', unsafe_allow_html=True)