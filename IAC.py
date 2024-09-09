import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker)
    return data

def add_ema(data, periods):
    for period in periods:
        data[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
    return data

def add_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def add_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data

st.title('Interactive Stock Chart with EMA, RSI, and MACD')

ticker = st.text_input('Enter Stock Ticker', 'GOOGL').upper()

data = load_data(ticker)

# Select time period
periods = st.slider('Select Time Period (in days)', 30, 365, 180)

# Select EMA
selected_emas = st.multiselect('Select EMA periods', [200, 50, 20], default=[200, 50, 20])

# Choose to add RSI or MACD
add_rsi_plot = st.checkbox('Add RSI Subplot')
add_macd_plot = st.checkbox('Add MACD Subplot')

# Prepare data with selected EMAs
data = add_ema(data, selected_emas)

# Filter data for the selected period
data_period = data[-periods:]

# Add RSI if selected
if add_rsi_plot:
    data_period = add_rsi(data_period)

# Add MACD if selected
if add_macd_plot:
    data_period = add_macd(data_period)

# Define the number of rows for subplots
rows = 1 + add_rsi_plot + add_macd_plot

# Calculate dynamic y-axis ranges
price_range = [data_period['Close'].min() * 0.95, data_period['Close'].max() * 1.05]
rsi_range = [0, 100]

# Initialize macd_range with default values
macd_range = [0, 0]

# Update macd_range if MACD data is present
if add_macd_plot:
    macd_range = [
        min(data_period['MACD'].min(), data_period['Signal Line'].min()) * 1.05,
        max(data_period['MACD'].max(), data_period['Signal Line'].max()) * 1.05
    ]

# Create subplots
fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.15, 
                    row_heights=[0.5] + [0.25] * (rows - 1),
                    subplot_titles=('Price', 'RSI', 'MACD')[:rows])

# Candlestick chart
fig.add_trace(go.Candlestick(x=data_period.index,
                             open=data_period['Open'],
                             high=data_period['High'],
                             low=data_period['Low'],
                             close=data_period['Close'],
                             name='Candlesticks'), row=1, col=1)

# Add EMAs to the chart
for period in selected_emas:
    fig.add_trace(go.Scatter(x=data_period.index, y=data_period[f'EMA_{period}'], mode='lines', name=f'EMA_{period}'), row=1, col=1)

current_row = 2
if add_rsi_plot:
    fig.add_trace(go.Scatter(x=data_period.index, y=data_period['RSI'], mode='lines', name='RSI'), row=current_row, col=1)
    fig.update_yaxes(range=rsi_range, row=current_row, col=1, title='RSI')
    current_row += 1

if add_macd_plot:
    fig.add_trace(go.Scatter(x=data_period.index, y=data_period['MACD'], mode='lines', name='MACD'), row=current_row, col=1)
    fig.add_trace(go.Scatter(x=data_period.index, y=data_period['Signal Line'], mode='lines', name='Signal Line'), row=current_row, col=1)
    fig.update_yaxes(range=macd_range, row=current_row, col=1, title='MACD')

# Update layout
fig.update_layout(
    title=f'{ticker} Stock Price and Indicators',
    xaxis_title='Date',
    yaxis_title='Price',
    height=400 + 200 * (rows - 1),
    margin=dict(l=50, r=50, t=50, b=50),
    legend=dict(x=0, y=1, traceorder='normal'),
    xaxis_rangeslider_visible=False,
    hovermode='x unified'  # Show hover information on x-axis
)

st.plotly_chart(fig)
