import json

from urllib import request, parse


class NpmApiClient:
    def __init__(self):
        self.base_api = 'https://api.npmjs.org'

    def get_download_count(self, package, period='last-month'):
        """Returns a single download count for a package in a specified period: Full documentation:
        https://github.com/npm/registry/blob/master/docs/download-counts.md """

        url = '{}/downloads/point/{}/{}'.format(self.base_api, period, package)
        try:
            serialized_data = request.urlopen(url).read()
            data = json.loads(serialized_data)
            return data['downloads']
        except Exception as e:
            print('Could not process download data for package {} because {}. Requested url: {}'.format(package, str(e), url))
            return 0


    def get_downloads_per_day(self, package, period='last-month'):
        """Returns an array of downloads per day for a package in a specified period: Full documentation:
        https://github.com/npm/registry/blob/master/docs/download-counts.md """

        url = '{}/downloads/range/{}/{}'.format(self.base_api, period, package)
        try:
            serialized_data = request.urlopen(url).read()
            data = json.loads(serialized_data)
            downloads = data['downloads']
            downloads_array = list(map(lambda d: d['downloads'], downloads))
            return downloads_array
        except Exception as e:
            print('Could not process downloads per data for package {} because {}. Requested url: {}'.format(package, str(e), url))
            return 0


