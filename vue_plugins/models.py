from django.db import models

# Create your models here.
from taggit.managers import TaggableManager

from vue_plugins.validators import validate_zero_or_greater, validate_one_or_less


class VuePlugin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.TextField(max_length=512, null=False, blank=True)
    repo_url = models.URLField(max_length=1024, blank=False, null=False,)
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
    num_commits_recently = models.IntegerField(default=0)
    num_contributors = models.IntegerField(default=0)
    num_downloads = models.IntegerField(default=0)
    num_stars = models.IntegerField(default=0)

    # Score
    score = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    def __str__(self):
        return '{} - {}'.format(self.name, self.repo_url)

    def update_info_from_github(self):
        pass
