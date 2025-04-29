import streamlit as st
import random
import time
import pandas as pd
import requests
import datetime
import streamlit.components.v1 as components
import yfinance as yf

# ====================
# --- PAGE CONFIG ---
# ====================
st.set_page_config(page_title="Stock Volatility & Volume Predictor", layout="wide")

# ====================
# --- SPLASH SCREEN ---
# ====================
import streamlit as st
import streamlit.components.v1 as components
import time

# ---- Set up session state to show splash screen only once ----
if "splash_shown" not in st.session_state:
    st.session_state["splash_shown"] = False

# ---- Display splash if not shown yet ----
if not st.session_state["splash_shown"]:
    components.html(
        """
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome</title>
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    overflow: hidden;
                }
                body {
                    background: url('https://i.ibb.co/0ymw3bD7/030862da29a5f0468107c4ac1ac7fa91.gif') no-repeat center center fixed;
                    background-size: cover;
                }
                .overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.4);
                    z-index: 1;
                }
                .typing {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    font-family: 'Roboto', sans-serif;
                    font-size: 2rem;
                    text-shadow: 2px 2px 4px #000000;
                    z-index: 2;
                }
            </style>
        </head>
        <body>
            <div class="overlay"></div>
            <div class="typing">Loading...</div>
        </body>
        </html>
        """,
        height=800
    )

    # Sleep for 3 seconds to let GIF play, then set flag to True
    time.sleep(3)
    st.session_state["splash_shown"] = True
    st.rerun()   


# --- Mapping Tickers to Similar Tickers
ticker_to_related = {
    "AAPL": ["MSFT", "GOOG", "NVDA", "META"],
    "MSFT": ["AAPL", "GOOG", "ORCL", "IBM"],
    "TSLA": ["NIO", "LCID", "F", "GM"],
    "AMZN": ["WMT", "SHOP", "BABA", "EBAY"],
    "GOOG": ["AAPL", "MSFT", "META", "AMZN"],
    "META": ["GOOG", "SNAP", "PINS", "TWTR"],
    "NVDA": ["AMD", "INTC", "TSM", "QCOM"],
    "JPM": ["BAC", "C", "WFC", "GS"],
    "NFLX": ["DIS", "ROKU", "WBD", "PARA"],
    # Default fallback: large tech
    "DEFAULT": ["AMZN", "TSLA", "GOOG", "META", "MSFT", "NVDA", "NFLX"]
}

def display_related_stocks(main_ticker):
    """
    Displays a 'People Also Search' section showing live stock data for related tickers dynamically.
    """
    # Get related symbols
    related_symbols = ticker_to_related.get(main_ticker.upper(), ticker_to_related["DEFAULT"])

    # Fetch live stock data
    related_stocks = []
    for sym in related_symbols:
        try:
            stock = yf.Ticker(sym)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                price_today = hist['Close'].iloc[-1]
                price_yesterday = hist['Close'].iloc[-2]
                change_pct = ((price_today - price_yesterday) / price_yesterday) * 100
            else:
                price_today = hist['Close'].iloc[-1]
                change_pct = 0.0

            related_stocks.append({
                "symbol": sym,
                "name": stock.info.get('shortName', sym),
                "price": price_today,
                "change_pct": change_pct
            })
        except Exception as e:
            st.error(f"Error fetching data for {sym}: {e}")

    # --- Streamlit display ---
    st.markdown("## 🔎 People Also Search")
    cols = st.columns(len(related_stocks))

    for idx, stock in enumerate(related_stocks):
        with cols[idx]:
            # Make the ticker clickable
            yahoo_link = f"https://finance.yahoo.com/quote/{stock['symbol']}"

            st.markdown(
                f"<a href='{yahoo_link}' target='_blank' style='text-decoration:none;'>"
                f"<strong style='font-size:20px;'>{stock['symbol']}</strong>"
                f"</a>",
                unsafe_allow_html=True
            )
            st.caption(stock['name'])
            st.markdown(f"<h3 style='margin-top: 0;'>{stock['price']:.2f}</h3>", unsafe_allow_html=True)

            color = "green" if stock['change_pct'] >= 0 else "red"
            st.markdown(
                f"<span style='color:{color}; font-size:18px;'> {stock['change_pct']:+.2f}%</span>",
                unsafe_allow_html=True
            )
# ====================
# --- MAIN PAGE ---
# ====================

st.title("📈 Stock Volatility & Trading Volume Predictor")
st.caption("Predict future volatility and trading activity of stocks based on deep learning (LSTM) modeling.")

st.markdown("---")

# ====================
# --- Ticker Selection ---
# ====================

# Read the csv file
sp500_df = pd.read_csv("sp500.csv")

# Extract the ticker column as a list
ticker_list = sp500_df['ticker'].dropna().tolist()

selected_ticker = st.selectbox("Select Ticker Symbol", ticker_list)

# ====================
# --- Prediction Button ---
# ====================

predict_button = st.button("Predict")

# Initialize placeholders
predicted_volatility = None
predicted_volume = None

# ====================
# --- After Clicking Predict ---
# ====================

if predict_button:
    with st.spinner("Predicting, please wait..."):
        time.sleep(2)  # Simulating computation delay, you can remove later
        # --- Placeholder for LSTM model prediction ---
        # Example: predicted_volatility, predicted_volume = predict_volatility_volume(selected_ticker)
        predicted_volatility = round(random.uniform(0.2, 0.8), 2)  # Mock random volatility
        predicted_volume = round(random.uniform(1e6, 5e6))  # Mock random trading volume

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Predicted Volatility", value=predicted_volatility)
    with col2:
        st.metric(label="Predicted Trading Volume", value=f"{predicted_volume:,}")

    st.markdown("---")

    # ====================
    # --- Auto-Refresh Content (Updated every 5 min) ---
    # ====================

    st.header(" 💡 Additional Insights")

    refresh_interval = 5 * 60  # 5 minutes in seconds
    last_refresh = st.session_state.get("last_refresh", 0)

    current_time = time.time()
    if current_time - last_refresh > refresh_interval:
        st.session_state["last_refresh"] = current_time
        # get real-time financial news 
        def fetch_real_time_news_finnhub(ticker):
            api_key = "cvt5it1r01qhup0ude90cvt5it1r01qhup0ude9g"  
            base_url = "https://finnhub.io/api/v1/company-news"

            today = datetime.date.today()
            seven_days_ago = today - datetime.timedelta(days=7)

            from_date = seven_days_ago.strftime("%Y-%m-%d")
            to_date = today.strftime("%Y-%m-%d")

            url = f"{base_url}?symbol={ticker}&from={from_date}&to={to_date}&token={api_key}"

            response = requests.get(url)
            if response.status_code == 200:
               data = response.json()
               if len(data) == 0:
                 return [("No recent news found.", None)]  
               news_list = [(article['headline'], article['url']) for article in data[:3]]
               return news_list
            else:
              return [("Error fetching news.", None)]       

        st.session_state["news_items"] = fetch_real_time_news_finnhub(selected_ticker)

        #get real-time macro data
        def fetch_macro_data():
            fred_api_key = "8e5a7198d8f2aa4127b994c6817400d5"
            base_url = "https://api.stlouisfed.org/fred/series/observations"

            # Example: Get GDP Growth, CPI Inflation, Unemployment Rate
            gdp_url = f"{base_url}?series_id=GDP&api_key={fred_api_key}&file_type=json"
            cpi_url = f"{base_url}?series_id=CPIAUCSL&api_key={fred_api_key}&file_type=json"
            unemployment_url = f"{base_url}?series_id=UNRATE&api_key={fred_api_key}&file_type=json"

            gdp = requests.get(gdp_url).json()["observations"][-1]["value"]
            cpi = requests.get(cpi_url).json()["observations"][-1]["value"]
            unemployment = requests.get(unemployment_url).json()["observations"][-1]["value"]

            return {
                "GDP Growth": f"{gdp}%",
                "CPI Inflation": f"{cpi}%",
                "Unemployment Rate": f"{unemployment}%"
            }
        
        st.session_state["macro_data"] = fetch_macro_data()

         #get real-time technical indicators
        def fetch_fundamentals(ticker):
            api_key = "Y16JFTL2T7VKTAEA"
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"

            response = requests.get(url)
            data = response.json()

            return {
                "ROA": f"{data.get('ReturnOnAssetsTTM', 'N/A')}%",
                "ROE": f"{data.get('ReturnOnEquityTTM', 'N/A')}%",
                "Quick Ratio": data.get('QuickRatio', 'N/A')
            }
        
        st.session_state["fundamentals_data"] = fetch_fundamentals(selected_ticker)
        
         #get real-time corporate actions data
        import requests
        import random

        def fetch_corporate_actions(ticker):
            api_key = "Y16JFTL2T7VKTAEA" 
            url = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={api_key}"

            response = requests.get(url)
            data = response.json()

            # Now data should be a list of dividend events
            if isinstance(data, list) and len(data) > 0:
                # Take the most recent dividend event
                latest_dividend = data[0]  # assuming the API returns sorted latest first
                dividend_amount = latest_dividend.get('dividend', "0.0")
            else:
                dividend_amount = "0.0"

            return {
                "Dividend Amount": f"${dividend_amount}",
                "Share Buyback": random.choice(["Ongoing", "None announced"])  # Still mock buyback info
            }

        # Then in your Streamlit refresh block:
        st.session_state["corporate_action_data"] = fetch_corporate_actions(selected_ticker)



    # Access refreshed data
    news_items = st.session_state.get("news_items", ["Loading..."])
    macro_data = st.session_state.get("macro_data", {})
    fundamentals_data = st.session_state.get("fundamentals_data", {})
    corporate_action_data = st.session_state.get("corporate_action_data", {})

    section_titles = ["Real-time Events/News", "Macroeconomic Factors", "Fundamentals", "Corporate Actions"]
    containers = st.columns(4)

    # --- Real-time News ---
    with containers[0]:
        st.subheader(section_titles[0])
        for headline, url in news_items:
            if url:
                st.markdown(f"- 📢 [{headline}]({url})")
        else:
                st.write(f"- 📢 {headline}")


    # --- Macroeconomic Data ---
    with containers[1]:
        st.subheader(section_titles[1])
        for key, value in macro_data.items():
            st.write(f"- {key}: {value}")

    # --- Fundamentals Data ---
    with containers[2]:
        st.subheader(section_titles[2])
        for key, value in fundamentals_data.items():
            st.write(f"- {key}: {value}")

    # --- Corporate Action Data ---
    with containers[3]:
        st.subheader(section_titles[3])
        for key, value in corporate_action_data.items():
            st.write(f"- {key}: {value}")

    st.markdown("---")

    # ====================
    # --- Suggestions Section ---
    # ====================

    st.subheader("💬 Suggestions Based on Forecast")

    suggestion_col1, suggestion_col2, suggestion_col3 = st.columns(3)

    if predicted_volatility and predicted_volume:
        if predicted_volatility > 0.5 and predicted_volume > 3e6:
            suggestion = "⚡ Very active market but risky — proceed with caution."
        elif predicted_volatility < 0.3 and predicted_volume > 3e6:
            suggestion = "✅ Active and relatively stable — favorable for trading."
        elif predicted_volatility > 0.5 and predicted_volume < 3e6:
            suggestion = "⚠️ Risky with lower liquidity — watch out for large price swings."
        else:
            suggestion = "🛌 Quiet market — low volatility and lower activity expected."

        with suggestion_col1:
            st.metric("Predicted Volatility", "High" if predicted_volatility > 0.5 else "Low")
        with suggestion_col2:
            st.metric("Predicted Volume", "High" if predicted_volume > 3e6 else "Low")
        with suggestion_col3:
            st.success(suggestion)
    st.markdown("---")
    display_related_stocks(main_ticker=selected_ticker)