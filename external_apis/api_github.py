import base64
import json
import os

from github import Github

from external_apis.utils import parse_github_url


class GithubApiClient:

    def __init__(self):
        self.client = Github(os.environ['GITHUB_API_KEY'])

    def get_repo_info(self, repo_url):
        repo_string = parse_github_url(repo_url)
        if repo_string:
            return self.client.get_repo(repo_string)
        return None

    def get_package_json_content(self, repo):
        content_file = repo.get_contents('package.json')
        if content_file:
            try:
                decoded_content = base64.b64decode(content_file.content)
                return json.loads(decoded_content)
            except Exception as e:
                print('Error decoding package json file from repo {} due to {}.'.format(repo.name, str(e)))
        return None




