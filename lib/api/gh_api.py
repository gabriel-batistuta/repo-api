from requests import get
from github import Github
from github.Repository import Repository
from github import Auth
from typing import Union
import json
from os.path import basename
from magic import Magic

class GitHub_API_Handler:
    def __init__(self, gh_api:str, retry:int = 1) -> None:
        '''
        gh_api: github api token that you generated, please view the README for doc
        retry: number of retries to get data from github api, default=1

        official repository for this code: https://github.com/gabriel-batistuta/repo-api        
        if you like, please give a star or contribute with issues or pull requests :)
        
        this code is powered by PyGithub: https://github.com/PyGithub/PyGithub
        '''
        self.gh = Github(auth=Auth.Token(gh_api), retry=retry)
        self.repos = self.gh.get_user().get_repos()
        user = self.gh.get_user()
        self.current_user = {
            'name':user.name,
            'username':user.login,
            'id':user.id,
            'avatar':user.avatar_url,
            'api_url':user.url,
            'profile_url':user.html_url,
        }
    
    def close(self):
        '''
        close the connection with github api
        '''
        self.gh.close()

    def get_license(self, repo) -> Union[str, None]:
        '''
        returns the license of a repository if have
        if not returns None
        '''
        if repo._license.value:
            print(repo._license.value.name)
            return repo._license.value.name
        else:
            return None

    def _replace_repo_url(self, repo_url:Repository) -> str:
        '''
        change the domain of api.github.com to github.com to get data from unmapped api data
        '''
        return repo_url._url.value.replace('api.github.com/repos','github.com')

    def _get_repo_raw(self, repo_url:Repository, branch=None) -> str:
        '''
        returns a repository url without any files, ex:
        https://raw.githubusercontent.com/gabriel-batistuta/repo-api/
        
        it doesnt do nothing but return by used for another function
        
        if branch is None and the repo doesnt has README.md or .gitignore, the function will give a error 
        '''

        url = self._replace_repo_url(repo_url)
        repo_raw = url.replace('github.com','raw.githubusercontent.com')
        if branch is None:
            for i in ['main', 'master', 'origin']:
                for j in ['README.md', '.gitignore']:
                    url = f'{repo_raw}/{i}/{j}'
                    if get(url).status_code == 200:
                        return url.replace(f'/{j}', '')
            raise Exception('unable to find raw data, probally the user doesnt make any README or .gitignore, please try pass the branch. Aborting...')
        else:
            return repo_raw + '/' + branch

    def _get_file_content(self, file_raw_url) -> dict[str, Union[str, bytes]]:
        '''
        returns a dict where keys are strings and values strings or bytes
        - if is text writeble return *str*
        - if not return *bytes*

        the check is built with python magic for know if content is possible to read of just with interpretter
        '''
        def verify_type(raw_url):
            mime = Magic(mime=True)
            content = get(raw_url).content
            mime_type = mime.from_buffer(content)
            print(f'{mime_type}')
            return mime_type, content
        
        mime_type, content = verify_type(file_raw_url)
        if mime_type.startswith('text/'):
            return {
                'content':content.decode('utf-8'),
                'extension':basename(file_raw_url).split('.')[1]
            }
        else:
            return {
                'content':content,
                'extension':basename(file_raw_url).split('.')[1]
                }

    def get_file_content(self, file_name:str, repo_name:Repository, branch=None) -> dict:
        '''
            returns a dict with content and extension
            the content is text if content is text
            content type is bytes if is any other type
            
            response example: {
                'content': b'some text, image or any',
                'extension': 'txt, png, pdf or any'
            }

            using example:
                file_raw_url = 'https://raw.githubusercontent.com/gabriel-batistuta/repo-api/main/lib/api/gh_api.py'
                
                response = get_file_content(file_raw_url) 
                if type(response['content']) == str:
                    file = open(f'filename.{response["extension"]}', 'w')
                else:
                    file = open(f'filename.{response["extension"]}', 'wb')
                    
                file.write(response['content'])
                file.close()
        '''

        if branch is not None:
            raw_url = f'{self._get_repo_raw(repo_name, branch=branch)}/{file_name}'
        else:
            raw_url = f'{self._get_repo_raw(repo_name)}/{file_name}'

        return self._get_file_content(raw_url)

    def get_stars(self, repo):
        '''
        returns the number of stars of a repository
        '''
        return repo.stargazers_count
    
    def find_repo(self, full_name_or_id: int | str,
    lazy: bool = False):
        '''
        returns a repository by search
        '''
        if lazy:
            return self.gh.get_repo(full_name_or_id, lazy=lazy)
        else:
            return self.gh.get_repo(full_name_or_id)

    def get_repo_snippet(self, repo:Repository):
        '''
        returns the snippet of a repository
        with all main content of repo: 
            {name, url, readme, license, 
            description, language, etc...}
        '''
        return {
            'name':repo.name,
            'readme':api.get_file_content('README.md',repo)['content'],
            'stars':api.get_stars(repo),
            'license':api.get_license(repo),
            'description':repo.description,
            'language':repo.language,
            'forks':repo.forks_count,
            'url':repo.html_url,
            'tags':repo.get_topics(),
            'created_at':repo.created_at,
            'updated_at':repo.updated_at
        }

if __name__ == '__main__':
    with open('config.json') as file:
        gh_api_token = json.load(file)['gh-api-secret']

    api = GitHub_API_Handler(gh_api_token)
    for repo in api.repos:
        api.get_repo_snippet(repo)
        help(api._get_file_content)
        break
    api.close()