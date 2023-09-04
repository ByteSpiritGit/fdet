import requests
from bs4 import BeautifulSoup


class Wikipedia:

    def __init__(self, lang='en') -> None:
        self.url = f'https://{lang}.wikipedia.org/w/api.php'
        self.wiki_url = f'https://{lang}.wikipedia.org/wiki'

    def set_lang(self, lang):
        self.url = f'https://{lang}.wikipedia.org/w/api.php'
        self.wiki_url = f'https://{lang}.wikipedia.org/wiki/'

    def search(self, title) -> list:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': title
        }
        data = requests.get(self.url, params=params).json()
        return [{"title": i["title"], "snippet":BeautifulSoup(i["snippet"], "html.parser").text} for i in data['query']['search']]

    def open_search(self, title) -> list:
        params = {
            'action': 'opensearch',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'search': title
        }
        response = requests.get(self.url, params=params).json()
        return [{"keyword" :response[1][i], "url": response[3][i]} for i in range(len(response[1]))]

    def extract_page(self, title) -> str:
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'extracts',
                    "explaintext": "1",
                    'format': 'json',
                    'utf8': 1,
        }
        response = requests.get(self.url, params=params).json()[
            'query']['pages'] 
        return response[list(response.keys())[0]]['extract']
