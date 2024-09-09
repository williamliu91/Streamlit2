import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to calculate moving average and envelopes
def calculate_moving_average_envelope(df, window, envelope_pct):
    df['MA'] = df['Close'].rolling(window=window).mean()
    df['Upper Envelope'] = df['MA'] * (1 + envelope_pct / 100)
    df['Lower Envelope'] = df['MA'] * (1 - envelope_pct / 100)
    return df

# Function to create the plot
def plot_moving_average_envelope(df, ma_period, envelope_pct):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue', width=2)))
    
    if ma_period != 'None':
        df_ma = calculate_moving_average_envelope(df.copy(), ma_period, envelope_pct)
        
        # Plotting the moving average
        fig.add_trace(go.Scatter(x=df_ma.index, y=df_ma['MA'], mode='lines', name=f'MA {ma_period}', line=dict(color='orange', width=2, dash='dash')))
        
        # Plotting the upper envelope
        fig.add_trace(go.Scatter(x=df_ma.index, y=df_ma['Upper Envelope'], mode='lines', name='Upper Envelope', line=dict(color='green', width=2, dash='dash')))
        
        # Plotting the lower envelope
        fig.add_trace(go.Scatter(x=df_ma.index, y=df_ma['Lower Envelope'], mode='lines', name='Lower Envelope', line=dict(color='red', width=2, dash='dash')))
    
    fig.update_layout(
        title=f'Moving Average Envelope (MA {ma_period})' if ma_period != 'None' else 'Moving Average Envelope',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark'
    )
    
    return fig

# Streamlit app
def main():
    st.title("Moving Average Envelope Visualization")
    
    # User input for stock and dates
    ticker = st.text_input("Enter stock ticker:", "GOOGL")
    start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End date", pd.to_datetime("2024-01-01"))
    
    # User input for envelope percentage
    envelope_pct = st.number_input("Enter envelope percentage:", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    
    # Fetch and display data
    if ticker:
        data = fetch_stock_data(ticker, start_date, end_date)
        if data.empty:
            st.error(f"No data found for ticker {ticker}.")
        else:
            # User input for moving average period
            ma_options = ['None'] + [10, 20, 50, 100, 200]
            ma_period = st.selectbox("Select Moving Average Period:", ma_options)
            
            # Plot
            fig = plot_moving_average_envelope(data, ma_period, envelope_pct)
            st.plotly_chart(fig)
            
if __name__ == "__main__":
    main()
