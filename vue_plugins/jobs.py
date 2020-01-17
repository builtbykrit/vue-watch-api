from time import sleep

import numpy as np
from django.db import transaction

from vue_plugins.models import VuePlugin


def update_plugins_info(plugins):
    """ Updates the info for all passed in plugins and returns a string of results"""
    error_count = 0
    for plugin in plugins:
        try:
            plugin.update_external_info()
            plugin.save()
        except Exception as e:
            # Log exception and continue
            error_count += 1
            import traceback
            traceback.print_exc()
            print('plugin {} failed for reason: {}'.format(plugin.repo_url, str(e)))

        # Make a max of 5 requests per second
        sleep(0.2)

    update_plugins_scores()
    plugin_count = len(plugins)
    return "{} out of {} plugins(s) were updated!".format(plugin_count - error_count, plugin_count)


@transaction.atomic
def update_plugins_scores():
    """Updates the scores for all plugins"""

    plugins = VuePlugin.objects.all()

    download_counts = VuePlugin.objects.values_list('num_downloads_recently', flat=True)
    github_stars = VuePlugin.objects.values_list('num_stars', flat=True)

    download_count_90th_percentile = np.percentile(download_counts, 90)
    github_stars_90th_percentile = np.percentile(github_stars, 90)

    for plugin in plugins:

        # Is the download count in the last 30 days in the top 10% of plugins?
        plugin.has_recent_downloads = plugin.num_downloads_recently > download_count_90th_percentile
        # Is the Github star count in the top 10% of plugins?
        plugin.has_star_status = plugin.num_stars > github_stars_90th_percentile

        plugin.score = plugin.score_total
        plugin.save()
