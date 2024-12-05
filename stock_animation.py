import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Set the title of the Streamlit app
st.title("Stock Prices with Animation and Custom EMAs")

# Create input fields for stock symbols and moving averages
col1, col2, col3 = st.columns(3)
with col1:
    stock_input = st.text_input("Enter stock symbols (comma-separated)", "META, AAPL, GOOGL")
    period = st.selectbox("Select time period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

with col2:
    ma1_period = st.number_input("First Moving Average Period (max value =200)", min_value=1, max_value=200, value=20)
    ma1_type = st.selectbox("First MA Type", ["EMA", "SMA"], index=0, key='ma1_type')

with col3:
    ma2_period = st.number_input("Second Moving Average Period (max value =200)", min_value=1, max_value=200, value=50)
    ma2_type = st.selectbox("Second MA Type", ["EMA", "SMA"], index=0, key='ma2_type')

# Process the input string to get a list of stock symbols
stock_symbols = [symbol.strip().upper() for symbol in stock_input.split(",")]

# Create a selection box for choosing which stock to display
selected_stock = st.selectbox("Select stock to display", stock_symbols)

def calculate_ma(data, period, ma_type='EMA'):
    if ma_type == 'EMA':
        return data.ewm(span=period, adjust=False).mean()
    else:  # SMA
        return data.rolling(window=period).mean()

try:
    # Fetch stock data for the selected symbol
    stock = yf.Ticker(selected_stock)
    hist = stock.history(period=period)

    # Reset index to get 'Date' as a column
    hist.reset_index(inplace=True)

    # Calculate selected moving averages
    ma1_name = f"{ma1_type}{ma1_period}"
    ma2_name = f"{ma2_type}{ma2_period}"
    
    hist[ma1_name] = calculate_ma(hist['Close'], ma1_period, ma1_type)
    hist[ma2_name] = calculate_ma(hist['Close'], ma2_period, ma2_type)

    # Create the base figure
    fig = go.Figure()

    # Create frames for animation
    frames = [
        go.Frame(
            data=[
                go.Scatter(x=hist['Date'][:k+1], y=hist['Close'][:k+1], mode='lines', name='Close Price'),
                go.Scatter(x=hist['Date'][:k+1], y=hist[ma1_name][:k+1], mode='lines', 
                          name=f'{ma1_name}', line=dict(dash='dot')),
                go.Scatter(x=hist['Date'][:k+1], y=hist[ma2_name][:k+1], mode='lines', 
                          name=f'{ma2_name}', line=dict(dash='dash'))
            ],
            name=str(k)
        ) for k in range(len(hist))
    ]

    # Add the first frame manually to ensure the initial display
    fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist['Close'][:1], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist[ma1_name][:1], mode='lines', 
                            name=f'{ma1_name}', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist[ma2_name][:1], mode='lines', 
                            name=f'{ma2_name}', line=dict(dash='dash')))

    # Update the layout with frames and animation settings
    fig.update_layout(
        xaxis=dict(range=[hist['Date'].min(), hist['Date'].max()], title='Date'),
        yaxis=dict(range=[hist['Close'].min(), hist['Close'].max()], title='Price ($)'),
        title=f"{selected_stock} Share Prices with {ma1_name} and {ma2_name}",
        updatemenus=[dict(type="buttons", showactive=False,
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None, {"frame": {"duration": 20, "redraw": True},
                                                     "fromcurrent": True, "mode": "immediate"}])])],
        sliders=[{
            "steps": [{"args": [[str(k)], {"frame": {"duration": 20, "redraw": True}, "mode": "immediate"}],
                       "label": str(hist['Date'][k].date()), "method": "animate"} for k in range(len(hist))],
            "transition": {"duration": 0},
            "x": 0.1,
            "len": 0.9
        }]
    )

    # Add frames to the figure
    fig.frames = frames

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig)

    # Display additional stock information
    with st.expander("Stock Information"):
        info = stock.info
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
        st.write(f"**Market Cap:** ${info.get('marketCap', 'N/A'):,}")
        st.write(f"**52 Week High:** ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**52 Week Low:** ${info.get('fiftyTwoWeekLow', 'N/A')}")

    # Display moving average crossover analysis
    with st.expander("Moving Average Analysis"):
        # Calculate latest values
        latest_close = hist['Close'].iloc[-1]
        latest_ma1 = hist[ma1_name].iloc[-1]
        latest_ma2 = hist[ma2_name].iloc[-1]
        
        st.write(f"**Latest Values:**")
        st.write(f"Close Price: ${latest_close:.2f}")
        st.write(f"{ma1_name}: ${latest_ma1:.2f}")
        st.write(f"{ma2_name}: ${latest_ma2:.2f}")
        
        # Analyze crossovers
        if latest_ma1 > latest_ma2:
            st.write(f"🔼 The {ma1_name} is currently above the {ma2_name}, suggesting bullish momentum.")
        else:
            st.write(f"🔽 The {ma1_name} is currently below the {ma2_name}, suggesting bearish momentum.")

except Exception as e:
    st.error(f"Error fetching data for {selected_stock}. Please check the stock symbol and try again.")
    st.error(f"Error details: {str(e)}")