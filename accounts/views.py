from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin,  DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_auth.views import LogoutView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


# from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from .mixins import PutOnlyMixin

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, PutOnlyMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ['destroy', 'update']:
    #         permission_classes = [IsOwnerOrAdmin]
    #     return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     if self.action in ['list', 'retrieve']:
    #         return User.objects.all()
    #     else:
    #         if self.request.user.is_superuser:
    #             return User.objects.all()
    #         else:
    #             return User.objects.filter(id=self.request.user.id)

    # def update(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     if user.id != request.user.id:
    #         print(user.id)
    #         print(self.request.user.id)
    #     return super().update(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     if user.id != request.user.id:
    #         print("Beka")
    #     return super().destroy(request, *args, **kwargs)

# class ListRetrieveUserViewSet(ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class DestroyUpdateUserViewSet(DestroyModelMixin, PutOnlyMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     permission_classes = [IsOwnerOrAdmin]
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return User.objects.all()
#         else:
#             return User.objects.filter(id=self.request.user.id)






