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
        # ✅ FIX: use a valid OpenRouter model
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        result = response.json()

        # 🔴 DEBUG HELP (IMPORTANT)
        if response.status_code != 200:
            return f"API Error {response.status_code}: {result}"

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return f"Unexpected response: {result}"

    except Exception as e:
        return f"Request Error: {e}"


# ---------------- WEATHER API ----------------
def get_weather():

    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=17.3850&longitude=78.4867&current_weather=true"

    try:
        response = requests.get(weather_url, timeout=10)
        data = response.json()

        weather = data.get("current_weather", {})

        temp = weather.get("temperature", "N/A")
        wind = weather.get("windspeed", "N/A")

        return f"Temperature: {temp}°C | Wind Speed: {wind} km/h"

    except Exception as e:
        return f"Weather Error: {e}"


# ---------------- NEWS API ----------------
NEWS_API_KEY = "a6ecc2c1514347c2a284d1d327ea84cc"

def get_news():

    news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(news_url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return [f"News API Error: {data}"]

        articles = data.get("articles", [])

        if not articles:
            return ["No news found"]

        return [article.get("title", "No Title") for article in articles[:5]]

    except Exception as e:
        return [f"News Error: {e}"]


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Multi API AI Chatbot")

st.title("🤖 Multi API AI Chatbot")
st.write("Choose a feature below")

option = st.selectbox("Choose Feature", ["AI Chat", "Weather", "Latest News"])


# ---------- AI CHAT ----------
if option == "AI Chat":

    st.subheader("Ask AI")

    user_question = st.text_input("Enter your question")

    if st.button("Send"):

        if not user_question.strip():
            st.warning("Please enter a question")

        else:
            answer = ask_ai(user_question)
            st.success(answer)


# ---------- WEATHER ----------
elif option == "Weather":

    st.subheader("Current Weather")

    if st.button("Get Weather"):
        st.success(get_weather())


# ---------- NEWS ----------
elif option == "Latest News":

    st.subheader("Top Headlines")

    if st.button("Get News"):

        news = get_news()

        for item in news:
            st.write("•", item)
