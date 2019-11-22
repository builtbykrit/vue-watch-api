from rest_framework.routers import SimpleRouter

from tags.views import TagsViewSet

router = SimpleRouter()
router.register('tags', TagsViewSet, 'tags')
urlpatterns = router.urls