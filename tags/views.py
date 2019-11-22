from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from taggit.models import Tag


class TagsViewSet(ListModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Sort tag names alphabetically
        names = sorted(list(map(lambda t: t.name, queryset)))
        return Response(names)
