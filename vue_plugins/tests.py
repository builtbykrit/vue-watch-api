import json

from dateutil import relativedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

# Create your tests here.
from vue_watch_api.test_helpers import create_vue_plugin
from vue_plugins.models import VuePlugin


class VuePluginScoreTests(TestCase):
    def test_manual_total(self):
        """ Each manual review item is worth 1 point except demo"""
        plugin = VuePlugin.objects.create(
            name='My Plugin 1',
            repo_url='github.com',
            has_example_code=False,
            has_api_documented=False,
            has_ci=False,
            has_demo=False,
            has_meaningful_tests=False
        )
        self.assertEqual(plugin.non_comparative_score_total, 0, 'initial score is 0')

        plugin.has_api_documented = True
        self.assertEqual(plugin.non_comparative_score_total, 1, 'api documented is worth 1 point')

        plugin.has_example_code = True
        self.assertEqual(plugin.non_comparative_score_total, 2, 'example code is worth 1 point')

        plugin.has_ci = True
        self.assertEqual(plugin.non_comparative_score_total, 3, 'ci integration is worth 1 point')

        plugin.has_meaningful_tests = True
        self.assertEqual(plugin.non_comparative_score_total, 4, 'tests is worth 1 point')

        plugin.has_demo = True
        self.assertEqual(plugin.non_comparative_score_total, 4, 'demo is not worth any')

    def test_last_release_date_score(self):
        """ The latest release within the last 12 months shoud"""
        plugin = VuePlugin.objects.create(
            name='My Plugin 1',
            repo_url='github.com',
            has_example_code=False,
            has_api_documented=False,
            has_ci=False,
            has_demo=False,
            has_meaningful_tests=False
        )

        plugin.last_release_date = timezone.now().date() - relativedelta.relativedelta(months=13)
        self.assertEqual(plugin.non_comparative_score_total, 0, 'no point for release date outside of a year')

        plugin.last_release_date = timezone.now().date() - relativedelta.relativedelta(months=11)
        self.assertEqual(plugin.non_comparative_score_total, 1, 'one point for release date within the last year')

    def test_num_commits(self):
        plugin = VuePlugin.objects.create(
            name='My Plugin 1',
            repo_url='github.com',
            has_example_code=False,
            has_api_documented=False,
            has_ci=False,
            has_demo=False,
            has_meaningful_tests=False
        )

        plugin.num_commits_recently = 2
        self.assertEqual(plugin.non_comparative_score_total, 0, 'no point for less than 6 recent commits')

        plugin.num_commits_recently = 3
        self.assertEqual(plugin.non_comparative_score_total, 1, 'one point for more than 5 commits')

    def test_num_contributors(self):
        plugin = VuePlugin.objects.create(
            name='My Plugin 1',
            repo_url='github.com',
            has_example_code=False,
            has_api_documented=False,
            has_ci=False,
            has_demo=False,
            has_meaningful_tests=False
        )

        plugin.num_contributors = 1
        self.assertEqual(plugin.non_comparative_score_total, 0, 'no point for only 1 contributor')

        plugin.num_contributors = 7
        self.assertEqual(plugin.non_comparative_score_total, 1, 'one point for more than 1 contributors')

        plugin.num_contributors = 8
        self.assertEqual(plugin.non_comparative_score_total, 2, 'additional point for more than 7 contributors')

class VuePluginListRetrieveTests(APITestCase):
    def setUp(self):
        self.plugin1 = create_vue_plugin(name='My Plugin1')
        self.plugin2 = create_vue_plugin(name='My Plugin2')
        self.plugin3 = create_vue_plugin(name='My Plugin3')

    def test_retrieve_list_of_plugins(self):
        """"Retrieving a list of plugins should all plugins"""
        response = self.client.get(reverse('vue_plugins-list'))

        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['results']), 3)
        self.assertEqual(response_json['count'], 3)
        self.assertIsNone(response_json['next'])
        self.assertIsNone(response_json['previous'])

        first_plugin = response_json['results'][0]

        self.assertNotIn('repo_readme', first_plugin, "Repo readmes should not be returned in a list")
        self.assertNotIn('downloads_per_day_recently', first_plugin, "Download count array should not be returned in a list")

        # Test sort order
        previous_score = 0
        previous_name = 'Z'
        for plugin in response_json["results"]:
            self.assertTrue(plugin["score"] >= previous_score)
            self.assertTrue(plugin["name"] <= previous_name)


    def test_find_plugin_by_name(self):
        """"Retrieving a list of plugins with search should return ones that have a partial name match"""

        url = '{}?search=plugin2'.format(reverse('vue_plugins-list'))
        response = self.client.get(url)

        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], self.plugin2.id)

    def test_find_plugin_by_description(self):
        """"Retrieving a list of plugins with search should also partial match the description field"""

        description = 'dhd44hdjdn3332n2kdnck11020a'
        plugin_to_find = create_vue_plugin('My Plugin4', description=description)
        url = '{}?search={}'.format(reverse('vue_plugins-list'), description[:12])
        response = self.client.get(url)

        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], plugin_to_find.id)

    def test_retrieve_plugin_by_id(self):
        """"Retrieving a plugin by id should return the plugin"""

        response = self.client.get(reverse('vue_plugins-detail', kwargs={'pk': self.plugin1.id}))

        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response_json["id"], self.plugin1.id)
        self.assertEqual(response_json["name"], self.plugin1.name)
        self.assertEqual(response_json["description"], self.plugin1.description)
        self.assertEqual(response_json["repo_url"], self.plugin1.repo_url)
        self.assertEqual(response_json["repo_readme"], self.plugin1.repo_readme)
        self.assertEqual(response_json["repo_num_open_issues"], self.plugin1.repo_num_open_issues)
        self.assertEqual(response_json["repo_license_name"], self.plugin1.repo_license_name)
        self.assertEqual(response_json["has_ci"], self.plugin1.has_ci == 1)
        self.assertEqual(response_json["has_meaningful_tests"], self.plugin1.has_meaningful_tests == 1)
        self.assertEqual(response_json["has_example_code"], self.plugin1.has_example_code == 1)
        self.assertEqual(response_json["has_api_documented"], self.plugin1.has_api_documented == 1)

        self.assertEqual(response_json["last_release_date"], self.plugin1.last_release_date)
        self.assertEqual(response_json["last_release_tag_name"], self.plugin1.last_release_tag_name)
        self.assertEqual(response_json["num_commits_recently"], self.plugin1.num_commits_recently)
        self.assertEqual(response_json["num_contributors"], self.plugin1.num_contributors)
        self.assertEqual(response_json["num_downloads_recently"], self.plugin1.num_downloads_recently)
        self.assertEqual(response_json["downloads_per_day_recently"], self.plugin1.downloads_per_day_recently)
        self.assertEqual(response_json["num_stars"], self.plugin1.num_stars)
        self.assertEqual(response_json["score"], self.plugin1.score)
        self.assertIn("tags", response_json)
        plugin_1_tag_names = self.plugin1.tags.names()
        self.assertEqual(len(response_json["tags"]), len(plugin_1_tag_names))

        for tag in response_json["tags"]:
            self.assertIn(tag, plugin_1_tag_names)
