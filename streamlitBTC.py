import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# Streamlit page config
st.set_page_config(page_title="Bitcoin Analysis", layout="wide")

st.title("📈 Bitcoin Price Analysis")
st.markdown("Analyzing Bitcoin price trends using recent data.")

# Function to fetch the latest Bitcoin data from Yahoo Finance
@st.cache_data
def load_data():
    # Download historical Bitcoin price data from Yahoo Finance
    df = yf.download('BTC-USD', period="30d", interval="1d")  # Fetch the last 30 days of data
    df.reset_index(inplace=True)  # Reset index to make 'Date' a column
    df.rename(columns={
        'Date': 'Date',
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume'
    }, inplace=True)
    return df

df = load_data()

# Show raw data
with st.expander("📄 Show Raw Data"):
    st.dataframe(df)

# Line chart of closing prices
st.subheader("📊 Closing Price Over Time")
fig_close = px.line(df, x='Date', y='Close', title="Bitcoin Closing Price")
st.plotly_chart(fig_close, use_container_width=True)

# Moving Average
st.subheader("🧮 Moving Average")
window = st.slider("Select Moving Average Window (Days):", 2, 14, 5)
df['MA'] = df['Close'].rolling(window=window).mean()

fig_ma = px.line(df, x='Date', y=['Close', 'MA'], title=f"Bitcoin with {window}-Day Moving Average")
st.plotly_chart(fig_ma, use_container_width=True)

# Summary statistics
st.subheader("📋 Summary Statistics")
st.write(df['Close'].describe())

# High/Low metrics
st.subheader("📌 Key Metrics")
col1, col2 = st.columns(2)
col1.metric("🔺 Highest Price", f"${df['High'].max():,.2f}")
col2.metric("🔻 Lowest Price", f"${df['Low'].min():,.2f}")
