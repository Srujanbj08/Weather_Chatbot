
# OpenAI Weather Chatbot Deployment 🤖

## Overview
This project is a **Proof of Concept (PoC)** showcasing a weather chatbot built using **OpenAI GPT-3.5-turbo** and **OpenWeather API**, integrated into a **Streamlit** web application. The bot processes user input, extracts locations, and provides real-time weather updates in a human-readable format.

---

## Features
- **Real-Time Weather Data**: Fetches accurate weather data for one or more locations using OpenWeather API.
- **Natural Language Understanding**: Utilizes OpenAI's GPT-3.5-turbo for intelligent text parsing and response generation.
- **Streamlit Integration**: An intuitive web interface for seamless interaction with the bot.
- **Dynamic Streaming**: Bot responses are displayed dynamically for a conversational experience.

---

## Demo
![image](https://github.com/user-attachments/assets/5c9d66a6-e339-4e27-9264-4b2d7d1a4270)

![image](https://github.com/user-attachments/assets/29e9fd84-0c8e-4871-8806-1600202be728)
---

## Installation

### Prerequisites
1. Python 3.8 or later installed.
2. API keys for:
   - [OpenAI](https://platform.openai.com/)
   - [OpenWeatherMap](https://openweathermap.org/)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/openai-weather-chatbot.git
   cd openai-weather-chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download `nltk` stopwords (if not already installed):
   ```python
   import nltk
   nltk.download('stopwords')
   ```
4. Set your API keys in the code:
   - Replace `openai.api_key` and `weather_api_key` with your respective API keys in the script.

5. Run the application:
   ```bash
   streamlit run chatbot_app.py
   ```

---

## Usage
1. Open the application in your browser (usually at `http://localhost:8501`).
2. Enter a weather-related query (e.g., "What is the weather in Manila and Cebu?").
3. The bot responds with real-time weather details for the locations.

---

## Example Queries
- **Single Location**: "What is the weather in Manila?"
- **Multiple Locations**: "What's the weather in Manila and Cebu?"
- **Invalid Queries**: "Tell me a joke" *(The bot will politely decline unrelated topics.)*

---

## Technologies Used
- **Languages**: Python
- **Libraries**:
  - [Streamlit](https://streamlit.io/) for the web interface.
  - [OpenAI](https://openai.com/) for GPT-3.5-turbo integration.
  - [Requests](https://docs.python-requests.org/) for API calls.
  - [NLTK](https://www.nltk.org/) for text preprocessing.
- **APIs**:
  - [OpenWeatherMap API](https://openweathermap.org/) for weather data.
  - [OpenAI API](https://openai.com/) for natural language processing.

---

## Limitations
- Requires internet connectivity for API calls.
- Limited to the free tier rate limits of OpenAI and OpenWeather APIs.

---

## Future Improvements
- Add support for weather forecasts.
- Deploy on a public cloud platform (e.g., AWS, Google Cloud).
- Enhance natural language understanding for complex queries.

---

