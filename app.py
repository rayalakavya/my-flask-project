from flask import Flask, render_template, request
from newsapi import NewsApiClient
import os

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print(f"Is NEWS_API_KEY loaded? {bool(NEWS_API_KEY)}")  # Should print True

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()
            news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy')
            articles = news.get('articles', [])
            if not articles:
                return render_template("home.html", all_articles=[], error="No articles found for your search.")
            return render_template("home.html", all_articles=articles, keyword=keyword)
        else:
            top_headlines = newsapi.get_top_headlines(country='in')
            articles = top_headlines.get('articles', [])
            if not articles:
                return render_template("home.html", all_headlines=[], error="No top headlines found.")
            return render_template("home.html", all_headlines=articles)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return render_template("home.html", all_articles=[], error="Failed to fetch news.")

if __name__ == "__main__":
    app.run(debug=True)

