import requests
# from bs4 import BeautifulSoup


class Wikipedia:

    def __init__(self, lang='en') -> None:
        self.url = f'https://{lang}.wikipedia.org/w/api.php'

    def set_lang(self, lang):
        self.url = f'https://{lang}.wikipedia.org/w/api.php'

    # TODO: get MOST revelant site via DPR/BM25

    def search(self, title) -> list:
        results = []
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': title
        }
        data = requests.get(self.url, params=params).json()
        for i in data['query']['search']:
            # , BeautifulSoup(i["snippet"], "html.parser").text, i["wordcount"]))
            results.append(i["title"])
        return results

    def open_search(self, title) -> list:
        results = []
        params = {
            'action': 'opensearch',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'search': title
        }
        response = requests.get(self.url, params=params).json()
        for i in range(len(response[1])):
            results.append((response[1][i], response[3][i]))
        return results

    def extract_page(self, title) -> str:
        result = ""
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
        for key in response:
            result = response[key]['extract']
            break
        return result
