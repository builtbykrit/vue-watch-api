from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from vue_plugins.models import VuePlugin


class VuePluginSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    has_demo = serializers.BooleanField()
    has_meaningful_tests = serializers.BooleanField()
    has_example_code = serializers.BooleanField()
    has_api_documented = serializers.BooleanField()
    has_ci = serializers.BooleanField()

    score = serializers.DecimalField(coerce_to_string=False, decimal_places=1, max_digits=4)

    class Meta:
        model = VuePlugin
        fields = '__all__'
