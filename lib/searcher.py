import requests
import json
import bs4

with open('config.json', 'r') as file:
    config = json.load(file)
    gh_user = config['gh-username']
    url = f'https://github.com/{gh_user}?tab=repositories'
