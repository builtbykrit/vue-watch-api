from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.admin import ModelAdmin

from vue_plugins.forms import VuePluginForm
from vue_plugins.models import VuePlugin


class VuePluginAdminExtra(ModelAdmin):
    actions = ['update_plugin_info']
    list_display = ['repo_url', 'name', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    form = VuePluginForm

    add_fieldsets = (
            (_('Repository Info'), {'fields': ('name', 'repo_url', 'tags')}),
            (_('Manual Review Fields'),
             {'fields': ('has_demo', 'has_meaningful_tests', 'has_example_code', 'has_api_documented', 'has_ci',)}),
    )

    fieldsets = (
            (_('Repository Info'), {'fields': ('name', 'repo_url', 'tags')}),
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

    def update_plugin_info(self, request, queryset):
        for plugin in list(queryset):
            plugin.update_info_from_github()

        plugin_count = len(queryset)
        self.message_user(request, "%s plugins(s) were updated!" % plugin_count)


admin.site.register(VuePlugin, VuePluginAdminExtra)
