from rest_framework.mixins import RetrieveModelMixin, ListModelMixin,  DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from .mixins import PutOnlyMixin

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, PutOnlyMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
