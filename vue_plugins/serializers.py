from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from vue_plugins.models import VuePlugin


class VuePluginSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    has_demo = serializers.BooleanField()
    has_meaningful_tests = serializers.BooleanField()
    has_example_code = serializers.BooleanField()
    has_api_documented = serializers.BooleanField()
    has_ci = serializers.BooleanField()

    score = serializers.DecimalField(coerce_to_string=False, decimal_places=1, max_digits=4)

    class Meta:
        model = VuePlugin
        fields = ('id', 'created_at', 'updated_at', 'name', 'description', 'repo_url', 'repo_readme', 'tags',
                  'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci', 'has_demo',
                  'last_release_tag_name', 'last_release_date', 'num_commits_recently', 'num_contributors',
                  'num_downloads_recently', 'num_stars', 'score', 'repo_num_open_issues', 'repo_license_name',
                  'downloads_per_day_recently'
                  )


class VuePluginListSerializer(VuePluginSerializer):
    class Meta:
        model = VuePlugin
        fields = ('id', 'created_at', 'updated_at', 'name', 'description', 'repo_url', 'tags',
                  'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci', 'has_demo',
                  'last_release_tag_name', 'last_release_date', 'num_commits_recently', 'num_contributors',
                  'num_downloads_recently', 'num_stars', 'score', 'repo_num_open_issues', 'repo_license_name',
                  )
