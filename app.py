from flask import Flask, render_template, request
from newsapi import NewsApiClient
import os
import requests  # add this import to test raw request

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print(f"Is NEWS_API_KEY loaded? {bool(NEWS_API_KEY)}")

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def test_raw_newsapi():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        print(f"Raw Response Status Code: {response.status_code}")
        print(f"Raw Response Text: {response.text[:300]}")  # first 300 chars
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching raw newsapi data: {e}")
        return None

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()
            news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy')
            articles = news.get('articles', [])[:100]
            return render_template("home.html", all_articles=articles, keyword=keyword)
        else:
            # Test raw request here to diagnose the issue
            raw_data = test_raw_newsapi()
            if not raw_data:
                raise Exception("Failed to fetch news data from NewsAPI.")
            
            articles = raw_data.get('articles', [])[:100]
            return render_template("home.html", all_headlines=articles)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return render_template("home.html", all_articles=[], error="Failed to fetch news.")

if __name__ == "__main__":
    app.run(debug=True)

