from django.forms import ModelForm, CharField, IntegerField, BooleanField

from vue_plugins.jobs import update_plugins_scores
from vue_plugins.models import VuePlugin


class VuePluginForm(ModelForm):
    """
     Custom form when adding a vue plugin in Django admin
    """
    name = CharField(required=False)
    repo_url = CharField(required=True)
    has_demo = IntegerField(required=True)
    has_meaningful_tests = IntegerField(required=True)
    has_example_code = IntegerField(required=True)
    has_api_documented = IntegerField(required=True)
    has_ci = IntegerField(required=True)

    class Meta:
        model = VuePlugin
        fields = (
            'name',
            'repo_url',
            'has_demo',
            'has_meaningful_tests',
            'has_example_code',
            'has_api_documented',
            'has_ci'
        )

    def save(self, commit=True):
        vue_plugin = super(ModelForm, self).save(commit=False)
        # Remove trailing slashes
        vue_plugin.repo_url = vue_plugin.repo_url.rstrip('/')

        # Update info from github and npm
        vue_plugin.update_external_info()
        vue_plugin.save()

        # Rescore the plugins
        update_plugins_scores()
        vue_plugin.refresh_from_db()
        return vue_plugin
