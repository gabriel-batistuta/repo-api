from requests import get
from github import Github
from github import Auth
from typing import Union
import json

with open('config.json') as file:
    gh_api = json.load(file)['gh-api-secret']
    auth = Auth.Token(gh_api)

# Public Web Github
g = Github(auth=auth, retry=1)

def get_license(repo) -> Union[str, None]:
    if repo._license.value:
        print(repo._license.value.name)
        return repo._license.value.name
    else:
        return None

def _get_repo_url(repo_url) -> str:
    return repo_url._url.value.replace('api.github.com/repos','github.com')

def _get_repo_raw(repo_url, branch=None) -> str:
    '''
    returns a repository url without any files, ex:
    https://raw.githubusercontent.com/gabriel-batistuta/repo-api/
    
    it doesnt do nothing but return by used for another function
    
    if branch is None and the repo doesnt has README.md or .gitignore, the function will give a error 
    '''

    repo_url = _get_repo_url(repo_url)
    repo_raw = repo_url.replace('github.com','raw.githubusercontent.com')
    if branch is None:
        for i in ['main', 'master', 'origin']:
            for j in ['README.md', '.gitignore']:
                url = f'{repo_raw}/{i}/{j}'
                if get(url).status_code == 200:
                    return url.replace(f'/{j}', '')
        raise Exception('unable to find raw data, probally the user doesnt make any README or .gitignore, please try pass the branch. Aborting...')
    else:
        return repo_raw + '/' + branch

def _get_file_content(file_raw_url) -> Union[str, bytes]:
    '''
        returns the text if content is text
        return bytes if is anything other 
    '''

    return get(file_raw_url).content

def get_file_content(file_name, repo_name, branch=None)Union[str, bytes]:
    '''
        returns a content of file 
    '''

    if branch is not None:
        
        return f'{_get_repo_raw(repo_name, branch=branch)}/{file_name}'
    else:
        return f'{_get_repo_raw(repo_name)}/{file_name}'

def get_stars(repo):
    return repo.stargazers_count

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.raw_data)
    print(repo.name)
    print(_get_repo_url(repo))
    print(get_stars(repo))
    print(get_license(repo))
    print(repo.description)
    print(repo.language)
    print(repo.forks_count)
    print(repo.git_url)
    print(repo.get_topics())
    print(repo.created_at)
    print(g.get_user())
    break

# To close connections after use
g.close()