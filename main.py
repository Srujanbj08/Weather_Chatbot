import streamlit as st
import requests
from transformers import pipeline

# Hugging Face Model (using free API)
HF_API_KEY = st.secrets["HF_API_KEY"]  # Get your key: https://huggingface.co/settings/tokens
WEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

st.header("🌦️ Weather Chatbot with Hugging Face LLM")
st.caption("Now with conversational AI! (Powered by Hugging Face)")

# Initialize Hugging Face pipeline (for local LLM) or use API
@st.cache_resource
def load_llm():
    return pipeline(
        "text-generation",
        model="HuggingFaceH4/zephyr-7b-beta",  # Lightweight model
        api_key=HF_API_KEY
    )

llm = load_llm()

def get_weather(location):
    """Fetch weather data from OpenWeatherMap."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        return {
            "city": response["name"],
            "temp": response["main"]["temp"],
            "description": response["weather"][0]["description"],
            "humidity": response["main"]["humidity"]
        }
    except:
        return None

def generate_response(user_input):
    """Use LLM to generate a conversational response with weather data."""
    # Step 1: Extract location using LLM
    prompt = f"""
    Extract the location from this user query. Return ONLY the city name:
    User: '{user_input}'
    Location: """
    location = llm(prompt, max_length=20, truncation=True)[0]["generated_text"].strip()
    
    # Step 2: Get weather data
    weather = get_weather(location)
    if not weather:
        return "Sorry, I couldn't fetch weather data for that location."
    
    # Step 3: Generate natural language response
    llm_prompt = f"""
    The user asked: '{user_input}'
    Weather data: {weather}
    Craft a friendly, concise response (1-2 sentences): """
    response = llm(llm_prompt, max_length=100)[0]["generated_text"]
    return response.split(":")[-1].strip()  # Clean output

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask about the weather (e.g., 'Should I wear a jacket in Paris?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Thinking..."):
        bot_response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.chat_message("assistant").write(bot_response)
