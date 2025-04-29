import streamlit as st
import pandas as pd
import requests
import datetime
import time
import yfinance as yf
import os
import random

# --- API Keys ---
FMP_API_KEY = st.secrets["FMP_API_KEY"]

# --- Helper Functions ---
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
    except Exception as e:
        st.error(f"Error fetching company info: {e}")
        return None

def find_related_tickers(current_symbol: str, sector: str) -> list:
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock-screener"
        params = {"sector": sector, "limit": 5, "apikey": FMP_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        tickers = [item['symbol'] for item in data if item['symbol'].upper() != current_symbol.upper()]
        return tickers
    except Exception as e:
        st.error(f"Error finding related tickers: {e}")
        return []

def display_related_stocks(main_ticker, ticker_to_related):
    related_symbols = ticker_to_related.get(main_ticker.upper(), ticker_to_related["DEFAULT"])
    related_stocks = []
    for sym in related_symbols:
        try:
            stock = yf.Ticker(sym)
            hist = stock.history(period="2d")
            if hist is None or hist.empty or len(hist) < 2:
                continue
            price_today = hist['Close'].iloc[-1]
            price_yesterday = hist['Close'].iloc[-2]
            change_pct = ((price_today - price_yesterday) / price_yesterday) * 100
            related_stocks.append({
                "symbol": sym,
                "name": stock.info.get('shortName', sym),
                "price": price_today,
                "change_pct": change_pct
            })
        except Exception as e:
            st.error(f"Error fetching data for {sym}: {e}")

    st.header(" 🔎 People Also Search")
    cols = st.columns(len(related_stocks))
    for idx, stock in enumerate(related_stocks):
        with cols[idx]:
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

# --- Page Content ---
st.title("🏢 Company Basic Information")

sp500_df = pd.read_csv("sp500.csv")
ticker_list = sp500_df['ticker'].dropna().tolist()
selected_ticker = st.selectbox("Select a Ticker Symbol", ticker_list)

predict_button = st.button("Select")

predicted_volatility = None
predicted_volume = None
ticker_to_related = {}

if selected_ticker:
    info = get_company_info(selected_ticker)
    related_tickers = find_related_tickers(selected_ticker, info['Sector']) if info else []
    ticker_to_related[selected_ticker.upper()] = related_tickers or []
    ticker_to_related["DEFAULT"] = []
else:
    st.error("Ticker not found.")

if predict_button:

    if info:
        col1, col2, col3 = st.columns([2, 2, 5])
        with col1:
            st.markdown(f"""<p style="font-size: 16px; font-weight: 600;">{info['Name']}</p>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <a href="{info['Website']}" target="_blank" style="
                    font-size: 14px; font-weight: bold; color: #1a73e8;
                    text-decoration: none; padding: 5px 8px; border: 1px solid #1a73e8;
                    border-radius: 3px; transition: all 0.2s ease;">
                    Visit Website
                </a>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <img src="{info['Image']}" width="80" style="
                    border-radius: 6px; box-shadow: 0px 4px 12px rgba(0,0,0,0.25), 0px 0px 4px rgba(0,0,0,0.15);">
                """, unsafe_allow_html=True)

    st.markdown("---")
    display_related_stocks(selected_ticker, ticker_to_related)

    try:
        stock = yf.Ticker(selected_ticker)
        hist = stock.history(period="60d").tail(30)
        avg_volatility = (hist['High'] - hist['Low']).mean() / hist['Close'].mean()
        avg_volume = hist['Volume'].mean()
    except Exception as e:
        st.error(f"Failed to fetch historical data: {e}")
        avg_volatility = None
        avg_volume = None

    st.header(" 💡 Related Information")

    # ============ Real-Time Data Sections ============

    # 1. Real-time News
    def fetch_real_time_news(ticker):
        api_key = "your_finnhub_api_key"
        base_url = "https://finnhub.io/api/v1/company-news"
        today = datetime.date.today()
        seven_days_ago = today - datetime.timedelta(days=7)
        url = f"{base_url}?symbol={ticker}&from={seven_days_ago}&to={today}&token={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                return [("No recent news found.", None)]
            news_list = [(article['headline'], article['url']) for article in data[:3]]
            return news_list
        else:
            return [("Error fetching news.", None)]

    # 2. Macroeconomic Data
    def fetch_macro_data():
        fred_api_key = "your_fred_api_key"
        base_url = "https://api.stlouisfed.org/fred/series/observations"
        gdp_url = f"{base_url}?series_id=GDP&api_key={fred_api_key}&file_type=json"
        cpi_url = f"{base_url}?series_id=CPIAUCSL&api_key={fred_api_key}&file_type=json"
        unemployment_url = f"{base_url}?series_id=UNRATE&api_key={fred_api_key}&file_type=json"
        gdp = requests.get(gdp_url).json()["observations"][-1]["value"]
        cpi = requests.get(cpi_url).json()["observations"][-1]["value"]
        unemployment = requests.get(unemployment_url).json()["observations"][-1]["value"]
        return {
            "GDP (Billion Dollars)": gdp,
            "CPI Inflation Rate": f"{cpi}%",
            "Unemployment Rate": f"{unemployment}%"
        }

    # 3. Fundamentals
    def fetch_fundamentals(ticker):
        try:
            url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?apikey={FMP_API_KEY}&limit=1"
            response = requests.get(url)
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                fundamentals = data[0]
                return {
                    "ROA": f"{float(fundamentals.get('returnOnTangibleAssets', 0)) * 100:.2f}%" if fundamentals.get('returnOnTangibleAssets') else "N/A",
                    "ROE": f"{float(fundamentals.get('roe', 0)) * 100:.2f}%" if fundamentals.get('roe') else "N/A",
                    "Dividend Yield": fundamentals.get('dividendYield', 'N/A')
                }
            else:
                return {}
        except Exception as e:
            st.error(f"Error fetching fundamentals: {e}")
            return {}

    # 4. Corporate Actions
    def fetch_corporate_actions(ticker):
        try:
            api_key = "your_alpha_vantage_api_key"
            url = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                latest_dividend = data[0]
                dividend_amount = latest_dividend.get('dividend', "0.0")
            else:
                dividend_amount = "0.0"
            return {
                "Dividend Amount": f"${dividend_amount}",
                "Share Buyback": random.choice(["Ongoing", "None announced"])
            }
        except Exception as e:
            st.error(f"Error fetching corporate actions: {e}")
            return {}

    # Fetch all real-time data
    news_items = fetch_real_time_news(selected_ticker)
    macro_data = fetch_macro_data()
    fundamentals_data = fetch_fundamentals(selected_ticker)
    corporate_action_data = fetch_corporate_actions(selected_ticker)

    tab_titles = ["Real-time News", "Macroeconomic Factors", "Fundamentals", "Corporate Actions"]
    tabs = st.tabs(tab_titles)

    # --- Tabs content ---
    with tabs[0]:
        st.subheader(tab_titles[0])
        for headline, url in news_items:
            if url:
                st.markdown(f"- 📢 [{headline}]({url})")
            else:
                st.write(f"- 📢 {headline}")

    with tabs[1]:
        st.subheader(tab_titles[1])
        for key, value in macro_data.items():
            st.write(f"- {key}: {value}")

    with tabs[2]:
        st.subheader(tab_titles[2])
        for key, value in fundamentals_data.items():
            st.write(f"- {key}: {value}")

    with tabs[3]:
        st.subheader(tab_titles[3])
        for key, value in corporate_action_data.items():
            st.write(f"- {key}: {value}")

    st.markdown("---")

# --- Display source code ---
with open(__file__, "r", encoding="utf-8") as f:
    lines = f.readlines()

functions_only = []
inside_function = False
buffer = []

for line in lines:
    if line.strip().startswith("def "):
        if buffer:
            functions_only.append("".join(buffer))
            buffer = []
        inside_function = True
    if inside_function:
        if line.strip() == "":  # 遇到空行，函数结束
            inside_function = False
            functions_only.append("".join(buffer))
            buffer = []
        else:
            buffer.append(line)

# 如果最后还有没加进去的函数
if buffer:
    functions_only.append("".join(buffer))

# 合并所有函数
functions_code = "\n\n".join(functions_only)

# Display
with st.expander("📜 View Function Code"):
    st.code(functions_code, language="python")


# --- Navigation Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page1.py")
with col2:
    if st.button("Next Page ➡️"):
        st.switch_page("page3.py")
