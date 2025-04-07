import streamlit as st  
import psycopg
import pandas as pd
import matplotlib.pyplot as plt


#find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title = "My Webpage", page_icon = ":tada:", layout = "wide")

# Page title
st.title("📊 Bitcoin Price Dashboard")

# Upload the CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file, parse_dates=["date"])

    # Convert column names to lowercase and strip spaces
    df.columns = df.columns.str.lower().str.strip()

    st.success("Data Loaded Successfully!")
    
    # Show data preview
    st.subheader("📅 Data Preview")
    st.dataframe(df.head())

    # Select chart type
    st.subheader("📈 Choose a Chart")
    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart"])

    # Select price column to plot
    column = st.selectbox("Choose Price Type", ["1. open", "2. high", "3. low", "4. close", "5. volume"])

    # Ensure selected column exists
    if column not in df.columns:
        st.error(f"Column '{column}' not found in dataset!")
        st.stop()

    # Plotting
    fig, ax = plt.subplots()
    if chart_type == "Line Chart":
        ax.plot(df["date"], df[column], label=column.title(), color="orange")
    else:
        ax.bar(df["date"], df[column], label=column.title(), color="skyblue")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"Bitcoin {column.title()} Prices Over Time")
    ax.grid(True)
    st.pyplot(fig)

    # Show volume stats
    st.subheader("📦 Volume Summary")
    if "volume" in df.columns:
        st.write(f"Total Volume: {df['volume'].sum():,.0f}")
        st.line_chart(df.set_index("date")["volume"])
    else:
        st.warning("⚠️ 'Volume' column not found in dataset.")
else:
    st.info("Please upload a CSV file to begin.")

