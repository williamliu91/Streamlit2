import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Streamlit application
st.set_page_config(page_title="Finance Data Dashboard", layout="wide")
st.title('Finance Data Dashboard')

# Sidebar for data type selection
st.sidebar.header('Select Data Type')
data_type = st.sidebar.radio('Choose data type', ['Stock', 'Forex'])

# Sidebar for chart template selection
st.sidebar.header('Select Chart Template')
if data_type == 'Stock':
    chart_templates = ['Candlestick with MA', 'Line Chart', 'Moving Averages Only', 'OHLC Chart']
else:
    chart_templates = ['Line Chart', 'OHLC Chart']  # Removed 'Candlestick Chart' for Forex

chart_template = st.sidebar.selectbox('Choose chart template', chart_templates)

# Date range selection
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input('Start date', pd.to_datetime('2023-01-01'))
end_date = col2.date_input('End date', pd.to_datetime('2024-07-30'))

# Function to create OHLC or Candlestick trace
def create_ohlc_candlestick(data, chart_type='ohlc'):
    return go.Ohlc(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='OHLC') if chart_type == 'ohlc' else go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Candlestick')

if data_type == 'Stock':
    # Stock selection
    stocks = {'Google': 'GOOGL', 'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Amazon': 'AMZN'}
    stock = st.sidebar.selectbox('Choose a stock', list(stocks.keys()))
    ticker = stocks[stock]
    
    # Fetch stock data
    data = yf.download(ticker, start=start_date, end=end_date)

    # Moving averages
    if chart_template in ['Candlestick with MA', 'Moving Averages Only']:
        st.sidebar.header('Moving Averages')
        short_window = st.sidebar.slider('Short window (days)', 5, 50, 20)
        long_window = st.sidebar.slider('Long window (days)', 50, 200, 100)

        # Calculate moving averages
        data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
        data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Plotting stock data
    st.header(f'{stock} Stock Chart')
    fig = go.Figure()

    if chart_template == 'Candlestick with MA':
        fig.add_trace(create_ohlc_candlestick(data, 'candlestick'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Short_MA'], mode='lines', name=f'Short {short_window}-day MA', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['Long_MA'], mode='lines', name=f'Long {long_window}-day MA', line=dict(color='red')))

    elif chart_template == 'Line Chart':
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

    elif chart_template == 'Moving Averages Only':
        fig.add_trace(go.Scatter(x=data.index, y=data['Short_MA'], mode='lines', name=f'Short {short_window}-day MA', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['Long_MA'], mode='lines', name=f'Long {long_window}-day MA', line=dict(color='red')))

    elif chart_template == 'OHLC Chart':
        fig.add_trace(create_ohlc_candlestick(data, 'ohlc'))

elif data_type == 'Forex':
    # Forex selection
    forex_pairs = {'USD/EUR': 'EURUSD=X', 'USD/JPY': 'JPY=X', 'GBP/USD': 'GBPUSD=X', 'USD/CHF': 'CHF=X'}
    forex_pair = st.sidebar.selectbox('Choose a forex pair', list(forex_pairs.keys()))
    ticker = forex_pairs[forex_pair]

    # Fetch forex data
    data = yf.download(ticker, start=start_date, end=end_date)

    # Plotting forex data
    st.header(f'{forex_pair} Forex Chart')
    fig = go.Figure()

    if chart_template == 'Line Chart':
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    elif chart_template == 'OHLC Chart':
        fig.add_trace(create_ohlc_candlestick(data, 'ohlc'))
    # Removed the Candlestick Chart option for Forex

# Customize layout
fig.update_layout(
    title=f'{stock if data_type == "Stock" else forex_pair} {"Stock Price" if data_type == "Stock" else "Exchange Rate"}',
    xaxis_title='Date',
    yaxis_title='Price' if data_type == 'Stock' else 'Exchange Rate',
    xaxis_rangeslider_visible=False,
    template='plotly_dark',
    height=600
)

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Display data table
if st.checkbox('Show raw data'):
    st.write(data)