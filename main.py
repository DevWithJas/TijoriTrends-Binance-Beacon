import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging
import time

def coinbase_system_status():
    url = "https://api.pro.coinbase.com/products"
    response = requests.get(url)
    return "API is up and running!" if response.status_code == 200 else "API is down or unreachable."

def fetch_coinbase_candlestick_data(symbol, interval):
    interval_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "6h": 21600, "1d": 86400}
    granularity = interval_map.get(interval, 60)
    url = f"https://api.pro.coinbase.com/products/{symbol}/candles"
    params = {'granularity': granularity}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def fetch_kraken_24hr_ticker_stats(symbol):
    symbol_mapping = {
        "BTC-USD": "XXBTZUSD",
        "ETH-USD": "XETHZUSD",
    }
    kraken_symbol = symbol_mapping.get(symbol, symbol)
    url = "https://api.kraken.com/0/public/Ticker"
    params = {'pair': kraken_symbol}
    response = requests.get(url, params=params)
    data = response.json()
    if data['result'].get(kraken_symbol):
        return data['result'][kraken_symbol]
    else:
        return f"Data for {symbol} ({kraken_symbol}) not found in Kraken API."

def process_ticker_data_for_radar(ticker_data):
    radar_data = {}
    
    categories = ['Asks', 'Bids', 'Close', 'Volume', 'Low', 'High', 'Open']

    for key, category in zip(['a', 'b', 'c', 'v', 'l', 'h', 'o'], categories):
        if key in ticker_data:
            radar_data[category] = ticker_data[key][0]

    return radar_data

def plot_radar_chart(data, symbol):
    categories = list(data.keys())
    values = list(data.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=symbol
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values)]
            )),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def fetch_coinbase_order_book(symbol, level=2):
    url = f"https://api.pro.coinbase.com/products/{symbol}/book"
    params = {'level': level}
    response = requests.get(url, params=params)
    data = response.json()
    return data

def measure_latency():
    url = "https://api.pro.coinbase.com/products"
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    return latency if response.status_code == 200 else None

def plot_candlestick_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(x=data['time'],
                                         open=data['open'], high=data['high'],
                                         low=data['low'], close=data['close'])])
    fig.update_layout(title=f'Candlestick Chart for {symbol}',
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_order_book_depth_chart(data, symbol):
    asks = pd.DataFrame(data['asks'], columns=['price', 'size', 'num_orders'])
    bids = pd.DataFrame(data['bids'], columns=['price', 'size', 'num_orders'])
    asks[['price', 'size']] = asks[['price', 'size']].apply(pd.to_numeric)
    bids[['price', 'size']] = bids[['price', 'size']].apply(pd.to_numeric)
    asks = asks.sort_values('price', ascending=True)
    bids = bids.sort_values('price', ascending=True)
    asks['cumulative'] = asks['size'].cumsum()
    bids['cumulative'] = bids['size'].cumsum()

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.02)

    fig.add_trace(
        go.Bar(x=asks['price'], y=asks['size'], name='Asks', marker_color='red'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=bids['price'], y=bids['size'], name='Bids', marker_color='green'),
        row=1, col=2
    )

    fig.update_layout(
        title=f'Order Book Depth Chart for {symbol}',
        xaxis_title='Price (Asks)',
        xaxis2_title='Price (Bids)',
        yaxis_title='Size',
        plot_bgcolor='white',
        showlegend=False
    )

    fig.update_xaxes(type='category', row=1, col=1)
    fig.update_xaxes(type='category', row=1, col=2)
    fig.update_yaxes(type='linear', row=1, col=1)
    fig.update_xaxes(autorange="reversed", row=1, col=1)

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.markdown("<h1 style='text-align: center; color: white;'>💹 TijoriTrends: Binance Beacon 🌟</h1>", unsafe_allow_html=True)
    st.image("https://media.tenor.com/T-zDRVK4XdQAAAAd/tradinggif.gif")
    
    st.sidebar.title("Navigation")
    selected_nav = st.sidebar.radio("Choose a section", ["Home", "Candlestick Chart", "24hr Stats", "Order Book Depth Chart", "API Latency"])

    selected_symbol_candlestick = st.selectbox(
        "Choose a cryptocurrency pair",
        ["BTC-USD", "ETH-USD"],
        key="selected_symbol_candlestick"
    )

    if selected_nav == "Home":
        st.write(coinbase_system_status())
    elif selected_nav == "Candlestick Chart":
        st.header("Candlestick Chart 🕯️")
        selected_interval = st.selectbox(
            "Choose the time interval",
            ["1m", "5m", "15m", "1h", "6h", "1d"],
            key="selected_interval"
        )
        if st.button("Show Candlestick Chart", key="button_candlestick"):
            data = fetch_coinbase_candlestick_data(selected_symbol_candlestick, selected_interval)
            plot_candlestick_chart(data, selected_symbol_candlestick)
    elif selected_nav == "24hr Stats":
        st.header("24hr Ticker Price Change Statistics 📊")
        ticker_data = fetch_kraken_24hr_ticker_stats(selected_symbol_candlestick)
        radar_data = process_ticker_data_for_radar(ticker_data)
        st.write(ticker_data)
        plot_radar_chart(radar_data, selected_symbol_candlestick)
    elif selected_nav == "Order Book Depth Chart":
        st.header("Order Book Depth Chart 📚")
        if st.button("Fetch and Plot Order Book Depth Chart", key="button_plot_order_book"):
            order_book_data = fetch_coinbase_order_book(selected_symbol_candlestick, level=1)
            plot_order_book_depth_chart(order_book_data, selected_symbol_candlestick)
    elif selected_nav == "API Latency":
        st.header("API Latency Measurement ⏳")
        if st.button("Measure Latency", key="button_latency"):
            latency = measure_latency()
            if latency is not None:
                st.write(f"The API latency is {latency:.2f} ms.")
            else:
                st.write("Failed to measure latency.")

if __name__ == "__main__":
    main()

