from ast import Raise
import requests
import json
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

class RepositorySearcher:
    def __init__(self, url: str) -> None:
        self.url = url

    def __call__(self) -> None:
        init() # colorama
        print('Colorama initialized')

    def _req_url(self, url:str):
        req =  requests.get(url)
        if req.status_code == 200:
            print(Fore.GREEN + 'requisition successfully: ' + Style.RESET_ALL + str(req.status_code))
            return req.content
        else:
            raise Exception(f'ERROR in requisition: status code - {req.status_code}')

    def _to_bs4(self):
        self.page_repo = BeautifulSoup(self._req_url(self.url), 'html.parser')

if __name__ == '__main__':
    with open('config.json', 'r') as file:
        config = json.load(file)
        gh_user = config['gh-username']
        url = f'https://github.com/{gh_user}?tab=repositories'
    rs = RepositorySearcher(url)
    rs._to_bs4()
