from time import sleep


def update_plugins_info(plugins):
    """ Updates the info for all passed in plugins and returns a string of results"""
    error_count = 0
    for plugin in plugins:
        try:
            plugin.update_external_info()
        except Exception as e:
            # Log exception and continue
            error_count += 1
            import traceback
            traceback.print_exc()
            print('plugin {} failed for reason: {}'.format(plugin.repo_url, str(e)))

        # Make a max of 5 requests per second
        sleep(0.2)

    plugin_count = len(plugins)
    return "{} out of {} plugins(s) were updated!".format(plugin_count - error_count, plugin_count)

def update_scores():
    """Updates the scores for all plugins"""

    plugins = Plugin.objects.all()
