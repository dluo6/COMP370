import argparse
import bs4
import json
import requests
import os.path

base_url = 'https://montrealgazette.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


def get_article_data(all_articles):
    data = {'trending_article_info': []}

    for article in all_articles:
        link = article.find('a', attrs={'data-tb-link': True})['href']
        body = requests.get(base_url+link, headers=headers)
        new_soup = bs4.BeautifulSoup(body.content, 'html.parser')
        details = new_soup.find('div', attrs={'class': 'article-header__detail__texts'})

        data_point = {}

        data_point['title'] = details.find('h1', attrs={'class': 'article-title'}).text
        data_point['publication date'] = details.find('span', attrs={'class': 'published-date__since'}).text
        author = details.find('div', attrs={'class': 'published-by'})
        author = author.find('a').text if author else ""
        data_point['author'] = author
        data_point['blurb'] = details.find('p', attrs={'class': 'article-subtitle'}).text

        data['trending_article_info'].append(data_point)

    return data


def get_trending_articles(output):
    body = requests.get(base_url+'/category/news/', headers=headers)

    soup = bs4.BeautifulSoup(body.content, 'html.parser')
    trending = soup.find('div', attrs={'data-tb-region': 'Top trending'})
    trending = trending.find('ol').find_all('li')
    
    data = get_article_data(trending)

    with open(os.path.join(os.path.dirname(__file__), output), 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='Output file', required=True)
    args = parser.parse_args()
    get_trending_articles(args.o)


if __name__ == '__main__':
    main()