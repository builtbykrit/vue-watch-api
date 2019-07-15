from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from vue_plugin_scoring.vue_plugins.forms import VuePluginForm
from vue_plugin_scoring.vue_plugins.models import VuePlugin


class VuePluginAdminExtra(ModelAdmin):

    form = VuePluginForm
    fieldsets = (
        (None, {
            (_('Repository Info'), {'fields': ('name', 'repo_url',)}),
            (_('Manual Review Fields'),
             {'fields': ('has_demo', 'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci')}),

        }),
    )


admin.site.register(VuePlugin, VuePluginAdminExtra)
