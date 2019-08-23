from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
# Create your models here.
from github import UnknownObjectException
from taggit.managers import TaggableManager

from external_apis.api_github import GithubApiClient
from external_apis.api_npm import NpmApiClient
from vue_plugins.validators import validate_zero_or_greater, validate_one_or_less


class VuePlugin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.TextField(max_length=512, null=False, blank=True)
    description = models.TextField(max_length=512, null=False, blank=True)

    npm_package_name = models.TextField(max_length=512, null=False, blank=True)

    repo_url = models.URLField(max_length=1024, blank=False, null=False, )
    tags = TaggableManager()

    # Manual Scoring Fields
    has_demo = models.IntegerField(validators=([validate_zero_or_greater, validate_one_or_less]),
                                   blank=False, null=False)

    has_meaningful_tests = models.IntegerField(validators=([validate_zero_or_greater, validate_one_or_less]),
                                               blank=False, null=False)
    has_example_code = models.IntegerField(validators=([validate_zero_or_greater, validate_one_or_less]), blank=False,
                                           null=False)
    has_api_documented = models.IntegerField(validators=([validate_zero_or_greater, validate_one_or_less]), blank=False,
                                             null=False)
    has_ci = models.IntegerField(validators=([validate_zero_or_greater, validate_one_or_less]), blank=False, null=False)

    # Automated Scoring Fields
    last_release_date = models.DateField(null=True, blank=True)
    # Commit count for last 3 months
    num_commits_recently = models.IntegerField(default=0)
    num_contributors = models.IntegerField(default=0)
    # Download count for last 30 days
    num_downloads_recently = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)

    # Score
    score = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    def __str__(self):
        return '{} - {}'.format(self.name, self.repo_url)

    def update_external_info(self):
        self._update_info_from_github()
        self._update_info_from_npm()

    def _update_info_from_npm(self):
        client = NpmApiClient()
        if self.npm_package_name:
            download_count = client.get_download_count(self.npm_package_name)
            self.num_downloads_recently = download_count
            self.save()

    def _update_info_from_github(self):
        client = GithubApiClient()
        repo = client.get_repo_info(self.repo_url)
        if repo:
            three_months_ago = datetime.now() - relativedelta(months=+3)

            if not self.name or self.name == '':
                self.name = repo.name

            self.description = repo.description

            try:
                latest_release = repo.get_latest_release()
                if latest_release:
                    self.last_release_date = latest_release.published_at
            except UnknownObjectException:
                print('Repo {} does not have any releases'.format(repo.name))
                self.last_release_date = None

            commits = repo.get_commits(since=three_months_ago)
            if commits:
                self.num_commits_recently = commits.totalCount

            contributors = repo.get_contributors()
            if contributors:
                self.num_contributors = contributors.totalCount

            self.num_stars = repo.stargazers_count

            package_json = client.get_package_json_content(repo)

            if package_json:
                npm_package_name = package_json.get('name', None)
                if npm_package_name:
                    self.npm_package_name = npm_package_name
            self.save()

