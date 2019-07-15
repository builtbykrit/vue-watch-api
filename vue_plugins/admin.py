from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.admin import ModelAdmin

from vue_plugins.forms import VuePluginForm
from vue_plugins.models import VuePlugin


class VuePluginAdminExtra(ModelAdmin):

    form = VuePluginForm

    add_fieldsets = (
            (_('Repository Info'), {'fields': ('name', 'repo_url',)}),
            (_('Manual Review Fields'),
             {'fields': ('has_demo', 'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci',)}),
    )

    fieldsets = (
            (_('Repository Info'), {'fields': ('name', 'repo_url',)}),
            (_('Manual Review Fields'),
             {'fields': ('has_demo', 'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci',)}),
            (_('Automatic Review Fields'),
             {'fields': ('last_release_date', 'num_commits_recently', 'num_contributors', 'num_downloads', 'num_stars',)}),
            (_('Score'),
             {'fields': ('score',)}),
    )

    readonly_fields = ('last_release_date', 'num_commits_recently', 'num_contributors', 'num_downloads', 'num_stars', 'score')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(VuePluginAdminExtra, self).get_fieldsets(request, obj)


admin.site.register(VuePlugin, VuePluginAdminExtra)
