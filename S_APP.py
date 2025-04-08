import streamlit as st
import psycopg
import pandas as pd
import os
import plotly.express as px

# Streamlit page config
st.set_page_config(page_title="Bitcoin Analysis", layout="wide")

# Page title and description
st.title("📈 Bitcoin Price Analysis")
st.markdown("Analyzing Bitcoin price trends using recent data.")

def get_data():
    """Fetch Bitcoin price data from the database."""

    # Try to get the DB connection string from Streamlit secrets, fallback to environment variable
    try:
        dbconn = st.secrets["DBCONN"]
    except Exception:
        st.warning("Using fallback DB connection string from environment variable.")
        dbconn = os.environ.get("DBCONN", "dbname=your_db user=your_user password=your_pass host=localhost port=5432")

    # Connect to the PostgreSQL database
    with psycopg.connect(dbconn) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT * FROM btc_price_last_month;''')
            data = cur.fetchall()

    # Convert the data into a pandas DataFrame
    data_df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    data_df['Date'] = pd.to_datetime(data_df['Date'])
    return data_df

# Fetch and display data
df = get_data()
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
