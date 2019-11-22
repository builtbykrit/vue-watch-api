# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from vue_plugins import serializers
from vue_plugins.models import VuePlugin


class VuePluginViewSet(ReadOnlyModelViewSet):
    queryset = VuePlugin.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
        tags = self.request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=[tags])

        return queryset