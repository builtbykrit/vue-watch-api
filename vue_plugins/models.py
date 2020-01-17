import base64
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.postgres.fields import ArrayField
from django.db import models
# Create your models here.
from django.utils import timezone
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
    repo_readme = models.CharField(max_length=131072, blank=True, null=False)
    repo_license_name = models.CharField(max_length=256, blank=True, null=False)
    repo_num_open_issues = models.IntegerField(default=0)

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

    last_release_tag_name = models.CharField(max_length=256, blank=True)

    # Automated Scoring Attributes

    last_release_date = models.DateField(null=True, blank=True)
    # Commit count for last 30 days
    num_commits_recently = models.IntegerField(default=0, help_text='Commit count for last 30 days')
    num_contributors = models.IntegerField(default=0)
    # Download count for last 30 days
    num_downloads_recently = models.IntegerField(default=0, help_text='NPM download count for last 30 days')
    # Array of downloads per day in the last 30 days
    downloads_per_day_recently = ArrayField(models.IntegerField(), null=True, help_text='NPM download count per day for the last 30 days')
    num_stars = models.IntegerField(default=0)

    # Score
    score = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    # Automatic Scoring fields/props

    has_recent_downloads = models.BooleanField(default=False)
    has_star_status = models.BooleanField(default=False)

    @property
    def has_recent_release(self):
        """Has there a been a new release in the last year?"""
        if not self.last_release_date:
            return False
        return self.last_release_date + relativedelta(years=1) >= timezone.now().date()

    @property
    def has_recent_commits(self):
        """Has there been more than two commits in the last 30 days?"""
        return self.num_commits_recently > 2

    @property
    def has_multiple_contributors(self):
        """Is there more than one contributor on the project?"""
        return self.num_contributors > 1

    @property
    def has_many_contributors(self):
        """Are there more than seven contributors on the project?"""
        return self.num_contributors > 7

    def calculate_score(self):
        """ Sum up the scoring fields"""

        # Sum the manual review fields
        total = self.has_ci + self.has_meaningful_tests + self.has_example_code + self.has_api_documented

        # Has there a been a new release in the last year?
        total += int(self.has_recent_release)

        # Has there been more than two commits in the last 30 days?
        total += int(self.has_recent_commits)

        # Is there more than one contributor on the project?
        total += int(self.has_multiple_contributors)

        # Are there more than seven contributors on the project?
        total += int(self.has_many_contributors)

        # Is the download count in the last 30 days in the top 10% of plugins?
        total += int(self.has_recent_downloads)

        # Is the Github star count in the top 10% of plugins?
        total += int(self.has_star_status)

        return total

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
            downloads_array = client.get_downloads_per_day(self.npm_package_name)
            self.downloads_array = downloads_array

    def _update_info_from_github(self):
        client = GithubApiClient()
        repo = client.get_repo_info(self.repo_url)
        if repo:
            one_month_ago = datetime.now() - relativedelta(months=1)

            if not self.name or self.name == '':
                self.name = repo.name

            self.description = repo.description
            try:
                license_file_data = repo.get_license()
                license = license_file_data.license
                if license:
                    self.repo_license_name = license.name

            except UnknownObjectException:
                print('Repo {} does not have a license'.format(repo.name))

            try:
                readme = repo.get_readme()
                try:
                    decoded_readme = base64.b64decode(readme.content)
                    readme_string = decoded_readme.decode("utf-8")
                    self.repo_readme = readme_string
                except Exception as e:
                    print('Error decoding readme file from repo {} due to {}.'.format(repo.name, str(e)))
            except UnknownObjectException:
                print('Repo {} does not have a readme'.format(repo.name))

            try:
                issues = repo.get_issues(state='open')
                if issues:
                    self.repo_num_open_issues = issues.totalCount
            except UnknownObjectException:
                print('Repo {} does not have any issues'.format(repo.name))
                self.last_release_date = None

            try:
                latest_release = repo.get_latest_release()
                if latest_release:
                    self.last_release_date = latest_release.published_at
                    self.last_release_tag_name = latest_release.tag_name
            except UnknownObjectException:
                print('Repo {} does not have any releases'.format(repo.name))
                self.last_release_date = None

            commits = repo.get_commits(since=one_month_ago)
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
