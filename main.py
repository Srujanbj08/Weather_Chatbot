# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:04:01 2025

@author: ASHNER_NOVILLA
"""


import streamlit as st
from time import sleep
import os
import openai
import requests
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string

# print(openai.__version__)
# print(nltk.__version__)
# print(st.__version__)
# print(requests.__version__)


st.header("**OpenAI Weather Chatbot Deployment** 🤖")
st.caption("This is a LLM PoC using OpenAI and OpenWeather Inference.")
st.caption("Author: Ashner Novilla :sunglasses:")

# Set your OpenAI API key
# Retrieve the API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Set your Open Weather Map API Key
weather_api_key = st.secrets["OPENWEATHER_API_KEY"]

# Input text
# user_input = "What is the weather Abu Dhabi and Dubai and Philippines"
# user_input = "Tell me a joke about Manila"


def question_checker(user_input):
    # This part is to pull the list of country in the given text
    question_checker_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a weather bot. Respond only to weather-related inquiries. For unrelated topics or jokes, reply with 'This is an unrelated topic.'"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0,  # Set to 0 for deterministic output
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    question_checker = question_checker_response['choices'][0]['message']['content'].strip()
    
    return question_checker, user_input
    
 
def extract_location_in_sentence(question_checker, user_input):

    # This part is to pull the list of country in the given text
    city_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract all names of locations or countries mentioned in the given sentence. Separate them with commas. and convert to English name. If none, return 'No location or country found.'"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0,  # Set to 0 for deterministic output
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    
    
    # Extract the response content
    location = city_response['choices'][0]['message']['content'].strip()
    
    return location


def words_result_cleaning(result_location):
        
    stop_words = set(stopwords.words('english'))
    
    result_location_list = ' '.join(
        word for word in result_location.split() if word.lower() not in stop_words
    )
    
    result_location_list = result_location_list.split(',')
    
    result_location_list = [''.join(c for c in s if c not in string.punctuation) for s in result_location_list]
    
    result_location_list = list(map(str.strip, result_location_list))
    
    # location_weather = result_location_list[1]
    
    result_respond = []
    
    for location_weather in result_location_list:
    
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location_weather}&appid={weather_api_key}&units=metric"
        
        try:
            response = requests.get(base_url)
            response.raise_for_status()  # Raise an error for HTTP issues
            data = response.json()
        
            if data.get("cod") != 200:
                raise ValueError(data.get("message", "Error fetching weather data."))
        
            weather_description = data['weather'][0]['description']
            city = data["name"]
            temperature = data["main"]["temp"]
            weather = data['weather'][0]['description']
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            feels_like = data["main"]["feels_like"]
            high_temp = data["main"]["temp_max"]
            low_temp = data["main"]["temp_min"]
            humidity = data['main']['humidity']
        
            weather_result = f'''The weather is {weather} in {city}, a temperature of {temperature}°C that feels like {feels_like}, a high of {high_temp}°C, a low of {low_temp}°C, and a humidity level of {humidity}%.'''
            
            result_respond.append(weather_result)            
            
        except Exception as e:
            str(e)
    
    result_respond = " ".join(result_respond)   
    
    return result_respond


def clean_result_fun(result_respond):
    # This part is to pull the list of country in the given text
    clean_result_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Make the response human like in English Language"
            },
            {
                "role": "user",
                "content": result_respond
            }
        ],
        temperature=0,  # Set to 0 for deterministic output
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    
    clean_result = clean_result_response['choices'][0]['message']['content'].strip()
    
    return clean_result


def chatbot(user_input):

    question_checker_result, user_input = question_checker(user_input)
    
    if question_checker_result in("This is an unrelated topic"):
        print("I'm here to provide weather updates. Please ask me questions related to weather or temperature.")
        clean_result = "I'm here to provide weather updates. Please ask me questions related to weather or temperature."
    
    else:
        location_result = extract_location_in_sentence(question_checker_result, user_input)
        
        if location_result in("No location or country found."):
            print("I'm here to provide weather updates. Please ask me questions related to weather or temperature.")
            clean_result = "I'm here to provide weather updates. Please ask me questions related to weather or temperature."

        else:
            words_result_cleaning_result = words_result_cleaning(location_result)
            clean_result = clean_result_fun(words_result_cleaning_result)
            
            print(clean_result)
        
    
    return clean_result

# Function to stream response
def stream_data(response_chat):
    """
    Stream response one word at a time.
    """
    for word in response_chat.split(" "):
        yield word + " "
        sleep(0.0002)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Chat input and processing
prompt = st.chat_input("Ask the bot something (type 'quit' to stop)")
if prompt:
    if prompt.lower() == "quit":
        st.write("**Chatbot session ended. Refresh the page to start a new conversation.**")
    else:
        # Add user message to history
        st.session_state["history"].append({"role": "user", "message": prompt})

        # Get bot response
        bot_response = chatbot(prompt)
        st.session_state["history"].append({"role": "bot", "message": bot_response})

# Display conversation history with streaming
for entry in st.session_state["history"]:
    if entry["role"] == "user":
        st.chat_message("user").write(entry["message"])
    elif entry["role"] == "bot":
        # Stream the bot's response dynamically
        placeholder = st.chat_message("assistant").empty()
        streamed_text = ""
        for chunk in stream_data(entry["message"]):
            streamed_text += chunk
            placeholder.write(f"**Bot:** {streamed_text}")
            
