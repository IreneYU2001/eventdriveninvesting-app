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
        1. Tavares, Abel. 2024. *FinStockDash*. GitHub. https://github.com/abeltavares/FinStockDash.
        2. Wysocki, Peter. "Example Project." Streamlit App. Accessed April 29, 2025. https://example-project.streamlit.app/.
    </div>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Closing Line ---
st.markdown('<h3 style="text-align:center; color:gray; margin-top:50px;">Thank you for reading! 🚀</h3>', unsafe_allow_html=True)