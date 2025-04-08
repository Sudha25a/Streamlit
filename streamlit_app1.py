import streamlit as st
import psycopg2  # or the appropriate DB connector library

def get_data(city):
    # Ensure the secrets file is correctly loaded
    try:
        dbconn = st.secrets["DBCONN"]
        # Example of using the database connection string or individual values
        conn = psycopg2.connect(
            host=dbconn["host"],
            user=dbconn["username"],
            password=dbconn["password"],
            database=dbconn["database"]
        )
        cursor = conn.cursor()
        
        # Your logic for fetching data from the database
        query = f"SELECT * FROM weather WHERE city = '{city}'"
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Return the weather data (or any data from your DB)
        return result

    except KeyError as e:
        st.error(f"Missing secret: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred while connecting to the database: {e}")
        return None
    finally:
        # Always close the DB connection
        if conn:
            conn.close()

# Streamlit app code to get city and fetch data
city = st.text_input("Enter the city name:")

if city:
    weather_data = get_data(city)
    if weather_data:
        st.write("Weather Data:", weather_data)
