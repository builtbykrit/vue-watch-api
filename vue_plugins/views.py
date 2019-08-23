# Create your views here.
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from vue_plugins import serializers
from vue_plugins.models import VuePlugin


class VuePluginViewSet(ReadOnlyModelViewSet):
    queryset = VuePlugin.objects.all()

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VuePluginListSerializer
        return serializers.VuePluginSerializer