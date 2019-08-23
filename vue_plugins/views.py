from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from vue_plugins.models import VuePlugin
from vue_plugins.serializers import VuePluginSerializer


class VuePluginViewSet(ReadOnlyModelViewSet):
    queryset = VuePlugin.objects.all()
    serializer_class = VuePluginSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

