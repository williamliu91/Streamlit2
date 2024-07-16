import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Interactive Stock Chart App", layout="wide")

# Define a dictionary mapping stock names to their ticker symbols
stocks = {
    "Google": "GOOGL",
    "Meta": "META",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA"
}

# Define a dictionary mapping color names to their hex codes for chart background
chart_color_map = {
    "White": "#FFFFFF",
    "Grey": "#808080",
    "Blue": "#0000FF",
    "Green": "#008000"
}

# Define a dictionary mapping color names to their hex codes for web page background
page_color_map = {
    "Light Green": "#E8F5E9",
    "Light Blue": "#E3F2FD",
    "Light Grey": "#F5F5F5"
}

# Sidebar for selecting time period
st.sidebar.header('Select Time Period')
time_period = st.sidebar.selectbox(
    'Time period',
    options=['1 month', '3 months', '6 months', '1 year', '3 years', '5 years'],
    index=5  # Default to '5 years'
)

# Sidebar for selecting web page background color
st.sidebar.header('Select Web Page Background Color')
page_bg_color_name = st.sidebar.selectbox(
    'Web Page Background Color',
    options=list(page_color_map.keys()),
    index=0  # Default to Light Green
)

# Convert selected page background color name to hex code
page_bg_color = page_color_map[page_bg_color_name]

# Sidebar for selecting chart background color
st.sidebar.header('Select Chart Background Color')
chart_bg_color_name = st.sidebar.selectbox(
    'Chart Background Color',
    options=list(chart_color_map.keys()),
    index=0  # Default to White
)

# Convert selected chart background color name to hex code
chart_bg_color = chart_color_map[chart_bg_color_name]

# Custom CSS for setting the web page background color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Page title and description
st.title('Interactive Stock Chart App')
st.write('Select a stock to view its chart:')

# Dropdown for selecting stock
selected_stock = st.selectbox('Stock', options=list(stocks.keys()))

# Fetch stock data
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)  # Default to 5 years
if time_period == '1 month':
    start_date = end_date - timedelta(days=30)
elif time_period == '3 months':
    start_date = end_date - timedelta(days=90)
elif time_period == '6 months':
    start_date = end_date - timedelta(days=180)
elif time_period == '1 year':
    start_date = end_date - timedelta(days=365)
elif time_period == '3 years':
    start_date = end_date - timedelta(days=3*365)

stock_data = yf.download(stocks[selected_stock], start=start_date, end=end_date)

# Create subplots
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                    subplot_titles=('Stock Price', 'RSI', 'Volume'), 
                    row_heights=[0.5, 0.2, 0.3])

# Add Stock Price trace
fig.add_trace(go.Candlestick(x=stock_data.index,
                             open=stock_data['Open'],
                             high=stock_data['High'],
                             low=stock_data['Low'],
                             close=stock_data['Close'],
                             name='Price'), row=1, col=1)

# Calculate RSI
delta = stock_data['Close'].diff(1)
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# Add RSI trace
fig.add_trace(go.Scatter(x=stock_data.index, y=rsi, mode='lines', name='RSI (14 days)'), row=2, col=1)

# Add Volume trace
fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Volume'), row=3, col=1)

# Set font and axis colors based on the selected chart background
if chart_bg_color == '#FFFFFF':
    font_color = 'black'
    axis_color = 'black'
    x_axis_color = 'black'  # Set x-axis color to black for white background
else:
    font_color = 'white'
    axis_color = 'white'
    x_axis_color = 'white'  # Set x-axis color to white for other backgrounds

# Customize chart layout
fig.update_layout(
    height=900,
    showlegend=True,
    paper_bgcolor=chart_bg_color,  # Use the selected chart background color
    plot_bgcolor=chart_bg_color,    # Set the background color of the plot area
    font=dict(color=font_color)  # Set text color based on background
)

# Update subplot axes titles and colors
fig.update_yaxes(title_text='Price', title_font_color=axis_color, row=1, col=1)
fig.update_yaxes(title_text='RSI', title_font_color=axis_color, row=2, col=1)
fig.update_yaxes(title_text='Volume', title_font_color=axis_color, row=3, col=1)
fig.update_xaxes(title_text='', title_font_color=axis_color, row=1, col=1)

# Update tick label colors to ensure they match the selected background
fig.update_yaxes(tickfont=dict(color=axis_color), row=1, col=1)
fig.update_yaxes(tickfont=dict(color=axis_color), row=2, col=1)
fig.update_yaxes(tickfont=dict(color=axis_color), row=3, col=1)

# Set x-axis date color based on the background
fig.update_xaxes(tickfont=dict(color=x_axis_color), row=1, col=1)
fig.update_xaxes(tickfont=dict(color=x_axis_color), row=2, col=1)
fig.update_xaxes(tickfont=dict(color=x_axis_color), row=3, col=1)

# Display the plotly chart
st.plotly_chart(fig)

# Export data as CSV
if st.button('Export Data as CSV'):
    csv_file = stock_data.to_csv(index=False)
    st.download_button(label='Download CSV', data=csv_file, file_name=f'{selected_stock}_data.csv', mime='text/csv')
