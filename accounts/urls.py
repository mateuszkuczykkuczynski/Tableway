from django.urls import path
# from .views import ListRetrieveUserViewSet, DestroyUpdateUserViewSet
from .views import UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'users', UserViewSet)
# router.register(r'users', ListRetrieveUserViewSet)
# router.register(r'users-test', DestroyUpdateUserViewSet, basename='user-change')

# urlpatterns = [
#     path('api/logout/', CustomLogoutView.as_view(), name='rest_logout')]

urlpatterns = router.urls

# urlpatterns = [
#     path('/all_users/', UserViewSet.as_view(), name='available_tables'),
#     path('/<id>/', AvailableTablesView.as_view(), name='available_tables'),
#     path('/update/<id>/', AvailableTablesView.as_view(), name='available_tables'),
#     path('/delete/<id>/', AvailableTablesView.as_view(), name='available_tables'),
#
# ]
