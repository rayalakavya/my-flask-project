from flask import Flask, render_template, request
from newsapi import NewsApiClient
import time
import os

app = Flask(__name__)

# Replace with your actual key or set as environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "3df526a01f384d279b6a19ca5dfc40bd")
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_sources_and_domains():
    """Fetches top 10 sources and corresponding domains."""
    try:
        all_sources = newsapi.get_sources()['sources']
        sources = [e['id'] for e in all_sources[:10]]
        domains = [e['url'].replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0] for e in all_sources[:10]]
        return ", ".join(sources), ", ".join(domains)
    except Exception as e:
        print("Error getting sources/domains:", e)
        return "", ""

def fetch_news_with_retry(keyword, sources, domains, retries=3, delay=5):
    """Fetch news articles with retry on failure."""
    for attempt in range(retries):
        try:
            news = newsapi.get_everything(
                q=keyword,
                sources=sources or None,
                domains=domains or None,
                language='en',
                sort_by='relevancy'
            )
            if news.get('status') != 'ok':
                raise Exception(news.get('message', 'Unknown error'))
            return news
        except Exception as e:
            print(f"Attempt {attempt+1}: {e}")
            time.sleep(delay)
    return None

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        sources, domains = get_sources_and_domains()
        related_news = fetch_news_with_retry(keyword, sources, domains)

        if not related_news or not related_news.get('articles'):
            return render_template("home.html", all_articles=[], keyword=keyword, error="No news found.")

        articles = related_news.get('articles', [])[:100]
        return render_template("home.html", all_articles=articles, keyword=keyword)

    else:
        top_headlines = newsapi.get_top_headlines(country='in')
        articles = top_headlines.get('articles', [])[:100]
        return render_template("home.html", all_headlines=articles)

if __name__ == "__main__":
    app.run(debug=True)

