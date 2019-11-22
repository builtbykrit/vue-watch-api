import json

from django.urls import reverse
from rest_framework.test import APITestCase

from vue_watch_api.test_helpers import create_tag


class TagsListTests(APITestCase):
    def setUp(self):
        self.tag1 = create_tag('UI')
        self.tag2 = create_tag('Official')
        self.tag3 = create_tag('Table')

    def test_retrieve_list_of_plugins(self):
        """"Retrieving a list of plugins should all plugins"""
        response = self.client.get(reverse('tags-list'))

        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 3)

        self.assertEqual(response_json[0], self.tag2.name)
        self.assertEqual(response_json[1], self.tag3.name)
        self.assertEqual(response_json[2], self.tag1.name)