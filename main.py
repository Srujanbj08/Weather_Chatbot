import streamlit as st
import requests

# API Keys (store in Streamlit secrets)
HF_API_KEY = st.secrets["HF_API_KEY"]
WEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

st.header("🌦️ Weather Chatbot with Hugging Face LLM")
st.caption("Now with conversational AI! (Powered by Hugging Face API)")

# Hugging Face Inference API Helper
def query_huggingface(prompt, max_length=100):
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": max_length}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_weather(location):
    """Fetch weather data from OpenWeatherMap."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return None
        return {
            "city": response["name"],
            "temp": response["main"]["temp"],
            "description": response["weather"][0]["description"].capitalize(),
            "humidity": response["main"]["humidity"]
        }
    except Exception as e:
        st.error(f"Weather API Error: {str(e)}")
        return None

def generate_response(user_input):
    """Generate conversational response using Hugging Face API."""
    # Step 1: Extract location
    location_prompt = f"""Extract ONLY the city name from this query: '{user_input}'"""
    location_response = query_huggingface(location_prompt, max_length=20)
    location = location_response[0]["generated_text"].strip()

    # Step 2: Get weather data
    weather = get_weather(location)
    if not weather:
        return f"Sorry, I couldn't get weather data for {location}."
    
    # Step 3: Generate friendly response
    response_prompt = f"""The user asked: '{user_input}'. 
    Weather data: {weather}. 
    Reply conversationally in 1-2 sentences:"""
    bot_response = query_huggingface(response_prompt)
    
    # Clean and return the response
    return bot_response[0]["generated_text"].strip()

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input and chatbot responses
if prompt := st.chat_input("Ask about weather (e.g., 'Do I need an umbrella in Tokyo?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Checking weather..."):
        try:
            bot_response = generate_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.chat_message("assistant").write(bot_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
