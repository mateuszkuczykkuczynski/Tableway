from .views import UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()

"""Registers the UserViewSet under the 'users' prefix."""
router.register(r'users', UserViewSet,  basename='user')
urlpatterns = router.urls
