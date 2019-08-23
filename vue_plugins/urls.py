from rest_framework.routers import SimpleRouter

from vue_plugins.views import VuePluginViewSet

router = SimpleRouter()
router.register('vue_plugins', VuePluginViewSet, 'vue_plugins')
urlpatterns = router.urls