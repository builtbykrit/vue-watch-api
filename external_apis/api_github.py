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


