import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go  # Import Plotly graph objects
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import logging
import requests


def check_api_status():
    url = "https://api.binance.com/api/v3/ping"
    response = requests.get(url)
    if response.status_code == 200:
        return "API is up and running!"
    else:
        return "API is down or unreachable."

def main():
    st.markdown("<h1 style='text-align: center; color: white;'>💹 TijoriTrends: Binance Beacon 🌟</h1>", unsafe_allow_html=True)
    # Display the GIF
    st.image("https://media.giphy.com/media/iRIf7MAdvOIbdxK4rR/giphy.gif")


    # HTML and CSS for the fancy button
    button_html = """
    <div class="fancy-button hvr-bob">
        <div class="left-frills frills"></div>
        <div class="button">$</div>
        <div class="right-frills frills"></div>
    </div>
    """

    button_css = """
    <style>
        .fancy-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background-color: #ff4081;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .fancy-button:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        .hvr-bob {
            vertical-align: middle;
            -webkit-transform: translateY(-8px);
            transform: translateY(-8px);
            -webkit-animation: hvr-bob-float 1.5s ease-in-out infinite;
            animation: hvr-bob-float 1.5s ease-in-out infinite;
        }
        @-webkit-keyframes hvr-bob-float {
            0%, 100% {
                -webkit-transform: translateY(-8px);
            }
            50% {
                -webkit-transform: translateY(-4px);
            }
        }
        @keyframes hvr-bob-float {
            0%, 100% {
                transform: translateY(-8px);
            }
            50% {
                transform: translateY(-4px);
            }
        }
        .frills {
            position: absolute;
            background-color: #ff4081;
            height: 100%;
            width: 10px;
            top: 0;
        }
        .left-frills {
            left: -10px;
            border-radius: 5px 0 0 5px;
        }
        .right-frills {
            right: -10px;
            border-radius: 0 5px 5px 0;
        }
    </style>
    """

    # Render HTML and CSS
    st.markdown(button_css, unsafe_allow_html=True)
    st.markdown(button_html, unsafe_allow_html=True)
    
def check_api_status():
    url = "https://api.binance.com/api/v3/ping"
    response = requests.get(url)
    if response.status_code == 200:
        return "API is up and running!"
    else:
        return "API is down or unreachable."
    
# Setup logging configuration
logging.basicConfig(level=logging.INFO)
    
def safe_api_request(url, params=None, method='get'):
    """
    A safe API request function with error handling.
    """
    try:
        if method == 'get':
            response = requests.get(url, params=params)
        elif method == 'post':
            response = requests.post(url, json=params)
        else:
            logging.error(f"Unsupported method: {method}")
            return None

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API request resulted in an exception: {e}")
        return None


def fetch_candlestick_data(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines"
    params = {'symbol': symbol, 'interval': interval}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                                     'taker_buy_quote_asset_volume', 'ignore'])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df = df.astype({'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'float'})
    return df

def plot_candlestick_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(x=data['open_time'],
                                         open=data['open'], high=data['high'],
                                         low=data['low'], close=data['close'])])
    fig.update_layout(title=f'Candlestick Chart for {symbol}',
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def fetch_24hr_ticker_stats(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr"
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    return response.json()

import time

def measure_latency(symbol):
    url = f"https://api.binance.com/api/v3/ping"
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    return latency if response.status_code == 200 else None


def main():
    st.markdown("<h1 style='text-align: center; color: white;'>💹 TijoriTrends: Binance Beacon 🌟</h1>", unsafe_allow_html=True)
    st.image("https://media.tenor.com/T-zDRVK4XdQAAAAd/tradinggif.gif")
    
    # Navigation bar in sidebar
    st.sidebar.title("Navigation")
    selected_symbol = st.sidebar.selectbox("💼 Choose a symbol for the candlestick chart", 
                                           ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT", "ADAUSDT"], key='candlestick_symbol')

    interval = st.sidebar.selectbox("🕒 Select the time interval for the candlestick chart", 
                                    ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"], key='interval')

    if st.sidebar.button("📊 Fetch Candlestick Data"):
        data = fetch_candlestick_data(selected_symbol, interval)
        plot_candlestick_chart(data, selected_symbol)

    # Separate section for 24hr Ticker Price Change Statistics
    st.markdown("## 📈 24hr Ticker Price Change Stats")
    selected_symbol_stats = st.selectbox("📈 Choose a symbol for 24hr stats", 
                                         ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT", "ADAUSDT"], key='24hr_stats_symbol')

    if st.button("Fetch 24hr Stats", key='fetch_24hr_stats'):
        ticker_data = fetch_24hr_ticker_stats(selected_symbol_stats)
        # Debug: Print the data to check if it's correct
        st.write(ticker_data)  # Remove after confirming data structure
        plot_24hr_ticker_stats(ticker_data, selected_symbol_stats)

    # Sidebar section for Order Book Depth Chart
    st.sidebar.markdown("## 📊 Order Book Depth Chart")
    selected_symbol_order_book = st.sidebar.selectbox(
        "📖 Choose a symbol for the Order Book", 
        ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT", "ADAUSDT"],
        key='order_book_symbol'
    )

    if st.sidebar.button("Fetch Order Book", key='fetch_order_book'):
        order_book_data = fetch_order_book(selected_symbol_order_book)
        plot_order_book(order_book_data, selected_symbol_order_book)

    # Latency Measurement as a center section
    st.markdown("## ⏳ Latency Measurement")
    selected_symbol = st.selectbox("Choose a symbol to measure latency", 
                                   ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT", "ADAUSDT"],
                                   key='latency_symbol')
    if st.button("⚡ Measure Latency", key='measure_latency'):
        latency = measure_latency(selected_symbol)
        if latency is not None:
            st.write(f"The round-trip latency for {selected_symbol} is {latency:.2f} ms.")
        else:
            st.write("Failed to measure latency.")


def fetch_order_book(symbol, limit=500):
    url = f"https://api.binance.com/api/v3/depth"
    params = {'symbol': symbol, 'limit': limit}
    response = requests.get(url, params=params)
    data = response.json()
    return data

def plot_order_book(data, symbol):
    # Process asks and bids
    asks = pd.DataFrame(data['asks'], columns=['price', 'quantity'], dtype=float)
    bids = pd.DataFrame(data['bids'], columns=['price', 'quantity'], dtype=float)
    
    # Cumulative sums for plotting
    asks['cum_quantity'] = asks['quantity'].cumsum()
    bids['cum_quantity'] = bids['quantity'].cumsum()

    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=asks['price'], y=asks['cum_quantity'], fill='tozeroy', name='Asks'))  # fill down to xaxis
    fig.add_trace(go.Scatter(x=bids['price'], y=bids['cum_quantity'], fill='tozeroy', name='Bids'))  # fill to trace0 y

    # Update titles and layout
    fig.update_layout(title=f'Order Book Depth Chart for {symbol}', xaxis_title='Price', yaxis_title='Cumulative Quantity')

    st.plotly_chart(fig, use_container_width=True)


import plotly.express as px


def plot_24hr_ticker_stats(data, symbol):
    # Create a DataFrame for the radar chart
    categories = ['Price Change', 'Price Change Percent', 'Weighted Avg Price', 'Last Price', 'High Price', 'Low Price']
    values = [float(data['priceChange']), float(data['priceChangePercent']),
              float(data['weightedAvgPrice']), float(data['lastPrice']),
              float(data['highPrice']), float(data['lowPrice'])]
    # Normalize the values to be between 0 and 1 for better representation in radar chart
    max_value = max(values)
    min_value = min(values)
    normalized_values = [(value - min_value) / (max_value - min_value) for value in values]
    df = pd.DataFrame(dict(r=normalized_values, theta=categories))

    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    
    fig.update_traces(fill='toself')
    fig.update_layout(
        title=f'24hr Ticker Price Change Statistics Radar Chart for {symbol}',
        polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, 1]
            )),
        showlegend=False
    )
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True)



 
if __name__ == "__main__":
    main()

