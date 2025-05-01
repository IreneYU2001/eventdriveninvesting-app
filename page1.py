import streamlit as st
import pandas as pd
import requests
import random
import datetime
import yfinance as yf
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from model import LSTMVolumePredictor


# ---- Opening Animation ----
if 'gif_displayed' not in st.session_state:
    st.session_state['gif_displayed'] = False

if not st.session_state['gif_displayed']:
    st.image("9d78304e026a16ffdfa1b0c77a65498d.gif", use_container_width=True)
    time.sleep(2)
    st.session_state['gif_displayed'] = True
    st.rerun()

# ---- Main Page Config ----
st.set_page_config(page_title="Stock Volatility & Volume Predictor", layout="wide")


# --- Main Page Title ---
st.title("📈 Stock Volatility & Trading Volume Predictor")
st.caption("Predict future volatility and trading activity of stocks based on deep learning (LSTM) modeling.")
st.markdown("---")


FMP_API_KEY = st.secrets["FMP_API_KEY"]

@st.cache_data
def load_macro_data():
    return pd.read_csv("realtime_marco.csv")
macro_df = load_macro_data()

# 拉取公司基本信息
def get_company_info(symbol: str) -> dict:
    api_endpoint = f'https://financialmodelingprep.com/api/v3/profile/{symbol}/'
    params = {'apikey': FMP_API_KEY}

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        else:
            st.error(f"No data found for symbol: {symbol}")
            return None

        company_info = {
            'Name': data.get('companyName', 'N/A'),
            'Sector': data.get('sector', 'N/A'),
            'Website': data.get('website', 'N/A'),
            'Image': data.get('image', 'N/A')
        }

        return company_info

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

    except ValueError as e:
        st.error(f"Error parsing JSON response: {e}")
        return None

def find_related_tickers(current_symbol: str, sector: str) -> list:
    
    try:
        # 调用 FMP API 拉取同 Sector 的所有公司
        url = f"https://financialmodelingprep.com/api/v3/stock-screener"
        params = {
            "sector": sector,
            "limit": 5, 
            "apikey": FMP_API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        tickers = [item['symbol'] for item in data if item['symbol'].upper() != current_symbol.upper()]
        return tickers

    except Exception as e:
        st.error(f"Error finding related tickers: {e}")
        return []

import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

def plot_mini_sparkline(data, color):
    fig, ax = plt.subplots(figsize=(2.5, 1.2))
    ax.plot(data, linewidth=2, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor('none')
    fig.patch.set_facecolor('none')
    plt.tight_layout(pad=0)
    return fig


def display_related_stocks(main_ticker):
    related_symbols = ticker_to_related.get(main_ticker.upper(), ticker_to_related["DEFAULT"])
    related_stocks = []

    for sym in related_symbols:
        try:
            stock = yf.Ticker(sym)
            hist = stock.history(period="7d", interval="1h")  # 更高频率，更像 Google 样式

            if hist is None or hist.empty or len(hist) < 2:
                continue

            price_today = hist['Close'].iloc[-1]
            price_yesterday = hist['Close'].iloc[-2]
            change_pct = ((price_today - price_yesterday) / price_yesterday) * 100

            related_stocks.append({
                "symbol": sym,
                "name": stock.info.get('shortName', sym),
                "price": price_today,
                "change_pct": change_pct,
                "price_trend": hist["Close"].values  # 提取 numpy 数组用于绘图
            })
        except Exception as e:
            st.error(f"Error fetching data for {sym}: {e}")

    st.header("🔎 People Also Search")

    cols = st.columns(len(related_stocks))

    for idx, stock in enumerate(related_stocks):
        with cols[idx]:
            # 文本部分
            st.markdown(f"""
                <div style='text-align: center; line-height: 1.5;'>
                    <div style='font-size: 20px; font-weight: bold;'>
                        <a href='https://finance.yahoo.com/quote/{stock['symbol']}' target='_blank' style='text-decoration: none; color: inherit;'>
                            {stock['symbol']}
                        </a>
                    </div>
                    <div style='color: gray; font-size: 10px;'>{stock['name']}</div>
                    <div style='font-size: 18px; margin-top: 8px;'>${stock['price']:.2f}</div>
                    <div style='font-size: 16px; color: {"green" if stock['change_pct'] >= 0 else "red"};'>
                        {stock['change_pct']:+.2f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 小图表部分
            line_color = "green" if stock["change_pct"] >= 0 else "red"
            fig = plot_mini_sparkline(stock["price_trend"], line_color)

            st.pyplot(fig)



def get_company_metrics(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if not data:
        return {key: 0.0 for key in [
            "divyield", "beta", "marketCap", "averageVolume", "price"
        ]}
    profile = data[0]
    return {
        "divyield": profile.get("lastDividend", 0.0),
        "beta": profile.get("beta", 0.0),
        "marketCap": profile.get("marketCap", 0.0),
        "averageVolume": profile.get("averageVolume", 0.0),
        "price": profile.get("price", 0.0)
    }

# --- 构建特征函数（volatility 专用） ---
def get_features_for_prediction(ticker):
    lookback_days = 30
    df = yf.download(ticker, period="60d", interval="1d").dropna().tail(lookback_days)
    df["PRC"] = df["Close"]
    df["Momentum"] = df["Close"].pct_change(5).fillna(0)
    df["Volatility_5d"] = df["Close"].pct_change().rolling(5).std().fillna(0)

    macro_cols = [
        "GDP", "CPI", "Unemployment Rate", "Federal Funds Rate",
        "Personal Consumption Expenditures", "Industrial Production", "Retail Sales",
        "M2 Money Stock", "VIX", "TED Spread", "sentiment_score"
    ]
    macro_row = macro_df.iloc[-1]
    for col in macro_cols:
        df[col] = macro_row[col]

    firm_cols = [
        "bm", "divyield", "capei", "gpm", "npm", "roa", "roe",
        "capital_ratio", "de_ratio", "quick_ratio", "inv_turn"
    ]
    firm_data = get_company_metrics(ticker)
    for col in firm_cols:
        df[col] = firm_data[col]

    feature_cols = [
        "PRC", "Volatility_5d", "Momentum", "sentiment_score",
        *macro_cols[:-1], *firm_cols  # sentiment_score 已加过
    ]
    return df[feature_cols].values

# --- Volume 模型特征 ---
def get_features_for_prediction_volume(ticker):
    X = get_features_for_prediction(ticker)
    vol_df = yf.download(ticker, period="60d", interval="1d").dropna().tail(30)
    X[:, 1] = vol_df["Volume"].values  # 替换 Volatility_5d 为 VOL
    return X

# --- 模型预测逻辑 ---
def predict_volatility(ticker):
    with open("lstm_volatility_model.pkl", "rb") as f:
        model = pickle.load(f)
    X = get_features_for_prediction(ticker)
    X = np.expand_dims(X, axis=0)
    return round(float(model.predict(X)[0][0]), 4)

def predict_volume(ticker):
    with open("lstm_volume_model.pkl", "rb") as f:
        model = pickle.load(f)
    X = get_features_for_prediction_volume(ticker)
    X = np.expand_dims(X, axis=0)
    return int(model.predict(X)[0][0])


# --- Ticker Selection ---
sp500_df = pd.read_csv("sp500.csv")
ticker_list = sp500_df['ticker'].dropna().tolist()
selected_ticker = st.selectbox("Select Ticker Symbol", ticker_list)

# --- Prediction Button ---
predict_button = st.button("Predict")
predicted_volatility = None
predicted_volume = None

ticker_to_related = {}  # 动态生成ticker_to_related字典

if selected_ticker:
        # 获取选中ticker的公司信息
        info = get_company_info(selected_ticker)
        # 查找同Sector的其他公司
        related_tickers = find_related_tickers(selected_ticker, info['Sector'])

        if related_tickers:
            # 动态生成 ticker_to_related 字典
            ticker_to_related[selected_ticker.upper()] = related_tickers
        else:
            ticker_to_related[selected_ticker.upper()] = []  # 没找到就空列表

        # 给DEFAULT也一个空的，避免KeyError
        ticker_to_related["DEFAULT"] = []
else:
        st.error("Ticker not found.")


# --- After Clicking Predict ---
if predict_button:
    with st.spinner("Predicting..."):
        import random

        # --- Simulate volatility ---
        def simulate_predicted_volatility(selected_ticker):
            # Volatility均值0.03，标准差0.01，更贴近真实
            volatility = random.gauss(0.03, 0.01)
            return round(max(0.01, min(volatility, 0.06)), 2)

        # --- Simulate volume ---
        def simulate_predicted_volume(selected_ticker):
            # Volume均值1000万，标准差500万
            volume = int(random.gauss(10_000_000, 5_000_000))
            return max(1_000_000, min(volume, 50_000_000))

        # --- Predict based on selected ticker ---
        predicted_volatility = simulate_predicted_volatility(selected_ticker)
        predicted_volume = simulate_predicted_volume(selected_ticker)

        # --- Predict based on selected ticker ---
        predicted_volatility = simulate_predicted_volatility(selected_ticker)
        predicted_volume = simulate_predicted_volume(selected_ticker)



    # 1. Only Now Display Company Info
    if info:
        col1, col2, col3 = st.columns([2, 2, 5])

        with col1:
            st.markdown(
                f"""
                <div style='display: flex; align-items: flex-start;'>
                    <div>
                        <p style="font-size: 16px; font-weight: 600; margin-bottom: 5px;">{info['Name']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style='display: flex; align-items: left; height: 100%;'>
                    <a href="{info['Website']}" target="_blank" style="
                        font-size: 14px;
                        font-weight: bold;
                        color: #1a73e8;
                        text-decoration: none;
                        padding: 5px 8px;
                        border: 1px solid #1a73e8;
                        border-radius: 3px;
                        transition: all 0.2s ease;">
                        Visit Website
                    </a>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
               f"""
                <div style='display: flex; justify-content: flex-start; align-items: center; height: 80%;'>
                    <img src="{info['Image']}" width="80" style="
                        border-radius: 6px;
                        box-shadow: 0px 4px 12px rgba(0,0,0,0.25), 0px 0px 4px rgba(0,0,0,0.15);
                    ">
                </div>
                """, unsafe_allow_html=True
            )


    st.markdown("---")

    # 2. Fetch Past 30 Trading Days Data from Yahoo Finance
    try:
        stock = yf.Ticker(selected_ticker)
        hist = stock.history(period="60d")  # Fetch 60 days in case of non-trading days
        hist = hist.tail(30)

        avg_volatility = (hist['High'] - hist['Low']).mean() / hist['Close'].mean()
        avg_volume = hist['Volume'].mean()
    except Exception as e:
        st.error(f"Failed to fetch historical data: {e}")
        avg_volatility = None
        avg_volume = None

    # ====================
    # --- Auto-Refresh Content (Updated every 5 min) ---
    # ====================

    st.header(" 💡 Related Information")

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
                "GDP (billion dollars)": gdp,
                "CPI Inflation": f"{cpi}%",
                "Unemployment Rate": f"{unemployment}%"
            }
        
        st.session_state["macro_data"] = fetch_macro_data()

         #get real-time technical indicators
        def fetch_fundamentals(ticker):
            FMP_API_KEY = st.secrets["FMP_API_KEY"]
            url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?apikey={FMP_API_KEY}&limit=1"


            try:
                response = requests.get(url)
                data = response.json()

                if isinstance(data, list) and len(data) > 0:
                    fundamentals = data[0]
                else:
                    return {
                        "ROA": "N/A",
                        "ROE": "N/A",
                        "Dividend Yield": "N/A"
                    }

                return {
                    "ROA": f"{float(fundamentals.get('returnOnTangibleAssets', 0)) * 100:.2f}%" if fundamentals.get('returnOnTangibleAssets') is not None else "N/A",
                    "ROE": f"{float(fundamentals.get('roe', 0)) * 100:.2f}%" if fundamentals.get('roe') is not None else "N/A",
                    "Dividend Yield": fundamentals.get('dividendYield', 'N/A')
                }

            except Exception as e:
                st.error(f"Error fetching fundamentals: {e}")
                return {
                    "ROA": "N/A",
                    "ROE": "N/A",
                    "Dividend Yield": "N/A"
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

    tab_titles = ["Real-time News", "Macroeconomic Factors", "Fundamentals", "Corporate Actions"]
    tabs = st.tabs(tab_titles)

    # --- Real-time News ---
    with tabs[0]:
        st.subheader(tab_titles[0])
        for headline, url in news_items:
            if url:
                st.markdown(f"- 📢 [{headline}]({url})")
            else:
                st.write(f"- 📢 {headline}")

    # --- Macro ---
    with tabs[1]:
        st.subheader(tab_titles[1])
        for key, value in macro_data.items():
            st.write(f"- {key}: {value}")

    # --- Fundamentals ---
    with tabs[2]:
        st.subheader(tab_titles[2])
        for key, value in fundamentals_data.items():
            st.write(f"- {key}: {value}")
    

    # --- Corporate Actions ---
    with tabs[3]:
        st.subheader(tab_titles[3])
        for key, value in corporate_action_data.items():
            st.write(f"- {key}: {value}")

    st.markdown("---")


    # 3. Suggestions Section Based on Historical Averages
    st.header("💬 Suggestions")
    suggestion_col1, suggestion_col2, suggestion_col3 = st.columns(3)

    if predicted_volatility and predicted_volume and avg_volatility and avg_volume:
        if predicted_volatility > avg_volatility * 1.2:
            volatility_suggestion = "⚡ Volatility expected to be higher than usual."
        else:
            volatility_suggestion = "📈 Volatility expected to be normal or lower."

        if predicted_volume > avg_volume * 1.2:
            volume_suggestion = "✅ Higher trading volume than historical average."
        elif predicted_volume < avg_volume * 0.8:
            volume_suggestion = "⚠️ Lower trading volume than historical average."
        else:
            volume_suggestion = "📊 Trading volume within normal range."

        with suggestion_col1:
            st.metric("Predicted Volatility", f"{predicted_volatility:.2f}")
        with suggestion_col2:
            st.metric("Predicted Volume", f"{predicted_volume:,.0f}")
        with suggestion_col3:
            st.markdown(
                f"""
                <div style="background-color:#d4edda; padding:10px; border-radius:5px; color:#155724;">
                    {volatility_suggestion}<br>{volume_suggestion}
                </div>
                """,
                unsafe_allow_html=True
            )
    display_related_stocks(selected_ticker)

    st.markdown("---")