import streamlit as st
from time import sleep
import requests
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string

st.header("**OpenWeatherMap Chatbot Deployment** 🤖")
st.caption("This is a PoC using OpenWeatherMap API.")
st.caption("Srujan B J")

# Set your API key
weather_api_key = st.secrets["OPENWEATHER_API_KEY"]


def extract_locations(user_input):
    """Extract potential location names from the input."""
    stop_words = set(stopwords.words('english'))
    cleaned_input = ' '.join(word for word in user_input.split() if word.lower() not in stop_words)
    return [word.strip(string.punctuation) for word in cleaned_input.split() if word]


def get_openweather_data(location):
    """Fetches weather data from OpenWeatherMap API for the given location."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        city = data["name"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return f"The weather in {city} is {description} with {temp}°C, {humidity}% humidity, and wind speed of {wind_speed} m/s."
    except Exception as e:
        return f"Error fetching weather data for {location}: {str(e)}"


def chatbot(user_input):
    locations = extract_locations(user_input)
    if not locations:
        return "Please include a location for weather updates."
    responses = [get_openweather_data(loc) for loc in locations]
    return "\n".join(responses)


# Initialize conversation history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Chat input and processing
prompt = st.chat_input("Ask the bot something (type 'quit' to stop)")
if prompt:
    if prompt.lower() == "quit":
        st.write("**Chatbot session ended. Refresh the page to start a new conversation.**")
    else:
        st.session_state["history"].append({"role": "user", "message": prompt})
        bot_response = chatbot(prompt)
        st.session_state["history"].append({"role": "bot", "message": bot_response})

# Display conversation history
for entry in st.session_state["history"]:
    if entry["role"] == "user":
        st.chat_message("user").write(entry["message"])
    elif entry["role"] == "bot":
        placeholder = st.chat_message("assistant").empty()
        streamed_text = ""
        for word in entry["message"].split():
            streamed_text += word + " "
            placeholder.write(f"**Bot:** {streamed_text}")
