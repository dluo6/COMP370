from .API_key import API_KEY
import requests
from datetime import date, timedelta

def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    all_articles_url = 'https://newsapi.org/v2/everything'
    search_space = ' OR '.join(news_keywords)
    oldest_date = date.today() - timedelta(days=lookback_days)

    params = {
        'q': search_space,
        'language': 'en',
        'from': oldest_date,
        'apiKey': api_key
    }
    res = requests.get(url=all_articles_url, params=params)
    
    if (res.status_code != 200):
        return []

    text = res.json()
    articles = text['articles']
    return articles


if __name__ == '__main__':
    fetch_latest_news(API_KEY, ['mystical'], 1)