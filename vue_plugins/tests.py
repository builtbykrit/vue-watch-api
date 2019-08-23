import json

from django.urls import reverse
from rest_framework.test import APITestCase

# Create your tests here.
from vue_plugin_scoring.test_helpers import create_vue_plugin


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
        self.assertEqual(response_json["has_ci"], self.plugin1.has_ci == 1)
        self.assertEqual(response_json["has_meaningful_tests"], self.plugin1.has_meaningful_tests == 1)
        self.assertEqual(response_json["has_example_code"], self.plugin1.has_example_code == 1)
        self.assertEqual(response_json["has_api_documented"], self.plugin1.has_api_documented == 1)

        self.assertEqual(response_json["last_release_date"], self.plugin1.last_release_date)
        self.assertEqual(response_json["num_commits_recently"], self.plugin1.num_commits_recently)
        self.assertEqual(response_json["num_contributors"], self.plugin1.num_contributors)
        self.assertEqual(response_json["num_downloads_recently"], self.plugin1.num_downloads_recently)
        self.assertEqual(response_json["num_stars"], self.plugin1.num_stars)
        self.assertEqual(response_json["score"], self.plugin1.score)
        self.assertIn("tags", response_json)
        plugin_1_tag_names = self.plugin1.tags.names()
        self.assertEqual(len(response_json["tags"]), len(plugin_1_tag_names))

        for tag in response_json["tags"]:
            self.assertIn(tag, plugin_1_tag_names)
