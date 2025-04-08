import streamlit as st
import psycopg
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="Bitcoin Analysis", layout="wide")

# Page title and description
st.title("📈 Bitcoin Price Analysis")
st.markdown("Analyzing Bitcoin price trends using recent data.")

def get_data():
    """Fetch Bitcoin price data from the database."""
    dbconn = st.secrets["DBCONN"]


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
BTC_Data = get_data()
st.dataframe(BTC_Data)

# # Line chart of closing prices
# st.subheader("📊 Closing Price Over Time")
# fig_close = px.line(BTC_Data, x='Date', y='Close', title="Bitcoin Closing Price")
# st.plotly_chart(fig_close, use_container_width=True)

# Moving Average
st.subheader("🧮 Moving Average")
window = st.slider("Select Moving Average Window (Days):", 2, 14, 5)
BTC_Data['MA'] = BTC_Data['Close'].rolling(window=window).mean()

# fig_ma = px.line(BTC_Data, x='Date', y=['Close', 'MA'], title=f"Bitcoin with {window}-Day Moving Average")
# st.plotly_chart(fig_ma, use_container_width=True)

# Summary statistics
st.subheader("📋 Summary Statistics")
st.write(BTC_Data['Close'].describe())

# High/Low metrics
st.subheader("📌 Key Metrics")
col1, col2 = st.columns(2)
col1.metric("🔺 Highest Price", f"${BTC_Data['High'].max():,.2f}")
col2.metric("🔻 Lowest Price", f"${BTC_Data['Low'].min():,.2f}")
