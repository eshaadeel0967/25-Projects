import streamlit as st
import requests
import plotly.express as px
import os

# Secure API Key Handling
API_KEY = os.getenv("WEATHER_API_KEY", "673fe59e65e472a329dabf72421af1c8")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# Function to fetch current weather data
def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Function to fetch AQI data
def get_aqi(city):
    weather_data = get_weather(city)
    if "coord" in weather_data:
        lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
        params = {"lat": lat, "lon": lon, "appid": API_KEY}
        response = requests.get(AQI_URL, params=params)
        return response.json()
    return None

# Function for dressing recommendations
def get_dressing_recommendation(temp):
    if temp < 10:
        return "🥶 Wear a heavy jacket, gloves, and a scarf! 🧥🧤"
    elif 10 <= temp < 20:
        return "🧥 A light sweater or hoodie should be fine."
    elif 20 <= temp < 30:
        return "👕 T-shirt and jeans work well!"
    else:
        return "☀️ Stay cool with shorts and a breathable shirt! 🩳"

# Streamlit UI Customization
st.set_page_config(page_title="🌍 Advanced Weather App", page_icon="🌦️", layout="wide")

st.markdown(
    """
    <style>
        body {background-color: #e0f7fa;}
        .stButton>button {background-color: #0288D1; color: white; font-size: 20px; border-radius: 12px; padding: 10px 20px;}
        .stButton>button:hover {background-color: #0277BD;}
        .stTextInput>div>div>input {font-size: 18px;}
        .stMarkdown h1 {color: #1565C0; font-size: 36px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Advanced Weather Forecast App")
st.markdown("### Get real-time weather updates with insights and tips! 🌡️🌦️")

st.sidebar.header("⚙️ Settings")
st.sidebar.subheader("Choose Graph Style 🎨")
graph_style = st.sidebar.radio("Select Graph Type:", ["Bar Chart", "Line Chart", "Pie Chart"])

st.sidebar.subheader("Additional Features")
show_aqi = st.sidebar.checkbox("Show Air Quality Index (AQI) 🌫️", value=True)
show_dressing_tip = st.sidebar.checkbox("Show Dressing Recommendation 👕", value=True)
show_wind_speed = st.sidebar.checkbox("Show Wind Speed 💨", value=True)

city = st.text_input("🏙️ Enter city name:", "New York")

if st.button("🔍 Get Weather"):
    data = get_weather(city)
    if data.get("cod") == 200:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"].title()
        dressing = get_dressing_recommendation(temp)

        st.subheader(f"🌤️ Weather in {city}")
        st.write(f"**🌡️ Temperature:** {temp}°C")
        st.write(f"**💧 Humidity:** {humidity}%")
        if show_wind_speed:
            st.write(f"**💨 Wind Speed:** {wind_speed} m/s")
        st.write(f"**☁️ Condition:** {weather_desc}")
        if show_dressing_tip:
            st.write(f"**👗 Dressing Recommendation:** {dressing}")

        # Graphical Analysis - Customizable Charts
        if graph_style == "Bar Chart":
            fig = px.bar(
                x=["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)"],
                y=[temp, humidity, wind_speed],
                color=["Temperature", "Humidity", "Wind Speed"],
                title=f"📊 Weather Analysis for {city}",
                color_discrete_sequence=["#FF5733", "#33FF57", "#3357FF"]
            )
        elif graph_style == "Line Chart":
            fig = px.line(
                x=["Temperature", "Humidity", "Wind Speed"],
                y=[temp, humidity, wind_speed],
                title=f"📈 Weather Trends for {city}",
                markers=True,
                line_shape='spline',
                color_discrete_sequence=["#FF5733"]
            )
        else:
            fig = px.pie(
                names=["Temperature", "Humidity", "Wind Speed"],
                values=[temp, humidity, wind_speed],
                title=f"🎯 Weather Distribution for {city}",
                color_discrete_sequence=["#FF5733", "#33FF57", "#3357FF"]
            )
        st.plotly_chart(fig)

        # Display AQI if enabled
        if show_aqi:
            aqi_data = get_aqi(city)
            if aqi_data:
                aqi_value = aqi_data["list"][0]["main"]["aqi"]
                st.write(f"**🌫️ Air Quality Index (AQI):** {aqi_value}")
    else:
        st.error("❌ City not found! Please enter a valid city name.")

st.markdown("📌 Get accurate weather updates and tips for your day!")
st.write("🔹 Developed by Esha")
