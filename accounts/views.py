from rest_framework.mixins import RetrieveModelMixin, ListModelMixin,  DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from .mixins import PutOnlyMixin

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, PutOnlyMixin, GenericViewSet):
    """
        UserViewSet is a DRF ViewSet for the User model. It supports the following operations:
        - Retrieve: Get a specific User.
        - List: Get all Users.
        - Destroy: Delete a User.
        - Put: Update a User.

        Permissions: Only the owner of a User or an admin can perform operations.

        URL pattern: '/users/{id}/' with 'user' as the base name.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
