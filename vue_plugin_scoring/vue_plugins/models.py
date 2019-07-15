from django.db import models

# Create your models here.
from vue_plugin_scoring.vue_plugins.validators import validate_zero_or_greater, validate_one_or_less


class VuePlugin(models.Model):
    name = models.TextField(max_length=512, null=False, blank=True)
    repo_url = models.TextField(max_length=1024, blank=False, null=False)

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

    def update_info_from_github(self):
        pass
