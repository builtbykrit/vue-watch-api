# Create your views here.
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from vue_plugins import serializers
from vue_plugins.models import VuePlugin


class VuePluginViewSet(ReadOnlyModelViewSet):
    queryset = VuePlugin.objects.all()

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['score', 'name']
    ordering = ['score', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VuePluginListSerializer
        return serializers.VuePluginSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # Filter by tags
        tags_string = self.request.query_params.get('tags', None)
        if tags_string:
            tags = [t for t in tags_string.split(',')]
            queryset = queryset.filter(tags__name__in=tags)

        return queryset