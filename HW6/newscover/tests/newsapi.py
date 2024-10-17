import unittest
from ..newsapi import fetch_latest_news
import json
from datetime import date, timedelta, datetime
import os.path

class TestNewsFetchMethods(unittest.TestCase):

    with open(os.path.join(os.path.dirname(__file__), 'secrets.json'), 'r') as file:
        data = json.load(file)
    api_key = data['API']

    def test_no_keywords(self):
        self.assertEqual(fetch_latest_news(self.api_key, []), [])

    def test_lookback_days(self):
        days = 10
        articles = fetch_latest_news(self.api_key, ['disaster'], days)
        last_day = date.today() - timedelta(days=days)
        contains_out_of_timeframe = False
        for a in articles:
            day = a['publishedAt'][:10]
            if date(*map(int, day.split('-'))) < last_day:
                contains_out_of_timeframe = True
                break
        self.assertFalse(contains_out_of_timeframe)

    def test_non_alpha_keyword(self):
        self.assertEqual(fetch_latest_news(self.api_key, ['1234f']), [])

if __name__ == '__main__':
    unittest.main()