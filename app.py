import streamlit as st
import requests

# ---------------- OPENROUTER API ----------------
OPENROUTER_API_KEY = "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"

def ask_ai(question):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    # DEBUG OUTPUT
    st.write(result)

    # SAFE CHECK
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return "API Error"


# ---------------- WEATHER API ----------------
def get_weather():

    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=17.3850&longitude=78.4867&current_weather=true"

    response = requests.get(weather_url)

    data = response.json()

    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    return f"Temperature: {temp}°C | Wind Speed: {wind} km/h"


# ---------------- NEWS API ----------------
NEWS_API_KEY = "a6ecc2c1514347c2a284d1d327ea84cc"

def get_news():

    news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

    response = requests.get(news_url)

    data = response.json()

    articles = data["articles"][:5]

    news_list = []

    for article in articles:
        news_list.append(article["title"])

    return news_list


# ---------------- STREAMLIT UI ----------------

st.title("Multi API AI Chatbot")

option = st.selectbox(
    "Choose Feature",
    [
        "AI Chat",
        "Weather",
        "Latest News"
    ]
)

# ---------- AI CHAT ----------
if option == "AI Chat":

    user_question = st.text_input("Ask AI")

    if st.button("Send"):

        answer = ask_ai(user_question)

        st.success(answer)


# ---------- WEATHER ----------
elif option == "Weather":

    if st.button("Get Weather"):

        weather = get_weather()

        st.success(weather)


# ---------- NEWS ----------
elif option == "Latest News":

    if st.button("Get News"):

        news = get_news()

        for item in news:
            st.write("•", item)
            