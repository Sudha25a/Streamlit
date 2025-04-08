import streamlit as st
import pandas as pd
import plotly.express as px
# import psycopg

# Streamlit page config
st.set_page_config(page_title="Bitcoin Analysis", layout="wide")

st.title("📈 Bitcoin Price Analysis")
st.markdown("Analyzing Bitcoin price trends using recent data.")

# Load data (assumes btc_price_last_month.csv is in the same GitHub repo)
@st.cache_data
def load_data():
    df = pd.read_csv("btc_price_last_month.csv")
    return df

df = load_data()

# Rename columns for consistency
df = df.rename(columns={
    'date': 'Date',
    '1. open': 'Open',
    '2. high': 'High',
    '3. low': 'Low',
    '4. close': 'Close',
    '5. volume': 'Volume'
})

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
