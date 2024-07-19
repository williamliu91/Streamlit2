import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Set the title of the Streamlit app
st.title("Meta (META) Share Prices with Animation and EMAs")

# Fetch META stock data
meta = yf.Ticker("META")
hist = meta.history(period="1y")

# Reset index to get 'Date' as a column
hist.reset_index(inplace=True)

# Calculate EMA 50 and EMA 20
hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()
hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()

# Create the base figure
fig = go.Figure()

# Create frames for animation
frames = [
    go.Frame(
        data=[
            go.Scatter(x=hist['Date'][:k+1], y=hist['Close'][:k+1], mode='lines', name='Close Price'),
            go.Scatter(x=hist['Date'][:k+1], y=hist['EMA50'][:k+1], mode='lines', name='EMA50'),
            go.Scatter(x=hist['Date'][:k+1], y=hist['EMA20'][:k+1], mode='lines', name='EMA20')
        ],
        name=str(k)
    ) for k in range(len(hist))
]

# Add the first frame manually to ensure the initial display
fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist['Close'][:1], mode='lines', name='Close Price'))
fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist['EMA50'][:1], mode='lines', name='EMA50'))
fig.add_trace(go.Scatter(x=hist['Date'][:1], y=hist['EMA20'][:1], mode='lines', name='EMA20'))

# Update the layout with frames and animation settings
fig.update_layout(
    xaxis=dict(range=[hist['Date'].min(), hist['Date'].max()], title='Date'),
    yaxis=dict(range=[hist['Close'].min(), hist['Close'].max()], title='Close Price'),
    title="Meta (META) Share Prices with Animation and EMAs",
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
