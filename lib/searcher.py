from email import header
import requests
import json
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
import re
from requests_html import HTMLSession

class RepositorySearcher:
    def __init__(self, url: str, gh_user:str) -> None:
        self.url = url
        self.gh_user = gh_user

    def __call__(self) -> None:
        init() # colorama
        print('Colorama initialized')

    def _req_url(self, url:str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        session = HTMLSession()
        response = session.get(url, headers=headers)
        response.html.render()
        content = response.html.html
        status_code = response.status_code
        req = requests.get(url, headers=headers)
        
        if status_code == 200:
            print(Fore.GREEN + 'requisition successfully: ' + Style.RESET_ALL + str(req.status_code))
            return content
        else:
            # raise Exception(f'ERROR in requisition: status code - {req.status_code}')
            print(f'ERROR in requisition: status code - {req.status_code}')
            return status_code

    def _to_bs4(self):
        self.page_repo = BeautifulSoup(self._req_url(self.url), 'html.parser')

    def get_repositories(self):
        repositories = [f'https://github.com/{self.gh_user}?tab=repositories']

        def crawl():
            pages = []
            next_page = self.page_repo.find('a', attrs={'rel':'next'}).get('href')
            # pattern_next_page = re.compile(r'next_page rgh-seen--\d+')
            pages.append('https://github.com' + str(next_page))
            print('https://github.com' + str(next_page))
            
            for i in range(3,15):
                page = f'https://github.com/{self.gh_user}?page={i}&tab=repositories'
                response = self._req_url(page)
                if type(response) == int:
                    break
                else:
                    page_bs4 = BeautifulSoup(response, 'html.parser')
                    with open('response.html','w') as file:
                        file.write(page_bs4.prettify())
                    print(response)
                    has_elements = page_bs4.find('ul', attrs={'data-filterable-for':'your-repos-filter'})
                    print(has_elements)
                    if has_elements is None:
                        break
                    else:
                        pages.append(page)
                        print(page)
            print(next_page)
        crawl()

        def scraping():

            repos = self.page_repo.find_all('li', class_='col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source')
            for repo in repos:
                name = repo.find('a', attrs={'itemprop':'name codeRepository'}).text.strip()
                url = 'https://github.com' + repo.find('a', attrs={'itemprop':'name codeRepository'}).get('href')
                description = repo.find('p', attrs={'itemprop':'description'}).text.strip()
                language = repo.find('span', attrs={'itemprop':'programmingLanguage'}).text.strip()
                stars = repo.find('svg', attrs={'aria-label':'star'}).text.strip()
                forks = repo.find('svg', attrs={'aria-label':'fork'}).text.strip()
                tags = repo.find_all('a', attrs={'data-octo-click':'topic_click'}).text.strip()
                if language is None:
                    license = repo.find('span', attrs={'class':'mr-3'}).text.strip()
                else:
                    license = None
                repositories.append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'language': language,
                    'stars': int(stars),
                    'forks': int(forks),
                    'tags': tags,
                    'license':license
                })
                print(Fore.GREEN + repo.text + Style.RESET_ALL)

if __name__ == '__main__':
    with open('config.json', 'r') as file:
        config = json.load(file)
        gh_user = config['gh-username']
        url = f'https://github.com/{gh_user}?tab=repositories'
    rs = RepositorySearcher(url, gh_user)
    rs._to_bs4()
    rs.get_repositories()