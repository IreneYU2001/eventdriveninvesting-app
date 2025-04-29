import streamlit as st
import pandas as pd
import requests
import datetime
import time
import yfinance as yf
import os
import random

# --- API Keys ---
FMP_API_KEY = st.secrets.get("FMP_API_KEY", "")
FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", "")
FRED_API_KEY = st.secrets.get("FRED_API_KEY", "")
ALPHA_VANTAGE_API_KEY = st.secrets.get("ALPHA_VANTAGE_API_KEY", "")

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

        return {
            'Name': data.get('companyName', 'N/A'),
            'Sector': data.get('sector', 'N/A'),
            'Website': data.get('website', 'N/A'),
            'Image': data.get('image', 'N/A')
        }
    except Exception as e:
        st.error(f"Error fetching company info: {e}")
        return None

def find_related_tickers(current_symbol: str, sector: str) -> list:
    try:
        url = "https://financialmodelingprep.com/api/v3/stock-screener"
        params = {"sector": sector, "limit": 5, "apikey": FMP_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        tickers = [item['symbol'] for item in data if item['symbol'].upper() != current_symbol.upper()]
        return tickers
    except Exception as e:
        st.error(f"Error finding related tickers: {e}")
        return []

def display_related_stocks(main_ticker, related_symbols):
    st.header(" 🔎 People Also Search")
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

    if related_stocks:
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

def fetch_real_time_news(ticker):
    try:
        today = datetime.date.today()
        seven_days_ago = today - datetime.timedelta(days=7)
        url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={seven_days_ago}&to={today}&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) == 0:
            return [("No recent news found.", None)]
        return [(article['headline'], article['url']) for article in data[:3]]
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return [("Error fetching news.", None)]

def fetch_macro_data():
    try:
        base_url = f"https://api.stlouisfed.org/fred/series/observations"
        def get_value(series_id):
            url = f"{base_url}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
            resp = requests.get(url)
            obs = resp.json().get("observations", [])
            if obs:
                return obs[-1]["value"]
            return "N/A"
        return {
            "GDP (Billion Dollars)": get_value("GDP"),
            "CPI Inflation Rate": f"{get_value('CPIAUCSL')}%",
            "Unemployment Rate": f"{get_value('UNRATE')}%"
        }
    except Exception as e:
        st.error(f"Error fetching macro data: {e}")
        return {}

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
        return {}
    except Exception as e:
        st.error(f"Error fetching fundamentals: {e}")
        return {}

def fetch_corporate_actions(ticker):
    try:
        url = f'https://www.alphavantage.co/query?function=DIVIDEND_HISTORY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
        r = requests.get(url)
        data = r.json().get('data', [])
        if data:
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

# --- Page Content ---
st.title("🏢 Company Basic Information")

sp500_df = pd.read_csv("sp500.csv")
ticker_list = sp500_df['ticker'].dropna().tolist()
selected_ticker = st.selectbox("Select a Ticker Symbol", ticker_list)
predict_button = st.button("Select")

info = None
related_tickers = []

if selected_ticker:
    info = get_company_info(selected_ticker)
    if info:
        related_tickers = find_related_tickers(selected_ticker, info['Sector'])

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

    display_related_stocks(selected_ticker, related_tickers)

    st.header(" 💡 Related Information")

    news_items = fetch_real_time_news(selected_ticker)
    macro_data = fetch_macro_data()
    fundamentals_data = fetch_fundamentals(selected_ticker)
    corporate_action_data = fetch_corporate_actions(selected_ticker)

    tabs = st.tabs(["Real-time News", "Macroeconomic Factors", "Fundamentals", "Corporate Actions"])

    with tabs[0]:
        for headline, url in news_items:
            if url:
                st.markdown(f"- 📢 [{headline}]({url})")
            else:
                st.write(f"- 📢 {headline}")
    with tabs[1]:
        for k, v in macro_data.items():
            st.write(f"- {k}: {v}")
    with tabs[2]:
        for k, v in fundamentals_data.items():
            st.write(f"- {k}: {v}")
    with tabs[3]:
        for k, v in corporate_action_data.items():
            st.write(f"- {k}: {v}")

# --- Display source code (functions only) ---
try:
    import inspect
    all_functions = [
        get_company_info,
        find_related_tickers,
        display_related_stocks,
        fetch_real_time_news,
        fetch_macro_data,
        fetch_fundamentals,
        fetch_corporate_actions
    ]

    function_texts = []
    for func in all_functions:
        source = inspect.getsource(func)
        function_texts.append(source)

    with st.expander("📜 View Function Code"):
        for func_source in function_texts:
            st.code(func_source, language="python")

except Exception as e:
    st.error(f"Unable to display source code: {e}")


# --- Navigation Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous Page"):
        st.switch_page("page1.py")
with col2:
    if st.button("Next Page ➡️"):
        st.switch_page("page4.py")