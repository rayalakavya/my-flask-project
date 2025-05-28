from flask import Flask, render_template, request
from newsapi import NewsApiClient
import os
import requests

app = Flask(__name__)

# Load your API key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print(f"Is NEWS_API_KEY loaded? {bool(NEWS_API_KEY)}")  # Prints True or False in logs

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()
            news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy')
            articles = news.get('articles', [])[:100]
            return render_template("home.html", all_articles=articles, keyword=keyword)
        else:
            top_headlines = newsapi.get_top_headlines(country='in')
            articles = top_headlines.get('articles', [])[:100]
            return render_template("home.html", all_headlines=articles)
    except Exception as e:
        print(f"Error fetching news: {e}")  # Print error in logs
        return render_template("home.html", all_articles=[], error="Failed to fetch news.")

# New route to test NewsAPI connectivity from Render
@app.route("/test-newsapi")
def test_newsapi():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        resp = requests.get(url)
        print("Test NewsAPI status code:", resp.status_code)
        print("Test NewsAPI response text:", resp.text[:500])  # print first 500 chars
        return f"Status code: {resp.status_code}, Response: {resp.text[:200]}"
    except Exception as e:
        print(f"Error testing NewsAPI connectivity: {e}")
        return "Error testing NewsAPI connectivity."

if __name__ == "__main__":
    app.run(debug=True)

