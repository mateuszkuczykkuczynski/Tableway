from django.urls import path
from .views import RestaurantAvailableTablesView, AllRestaurantsAvailableTablesView

urlpatterns = [
    path('restaurants/<str:restaurant>/tables/available/', RestaurantAvailableTablesView.as_view(),
         name='available_tables'),
    path('restaurants_all/tables/available/', AllRestaurantsAvailableTablesView.as_view(), name='all_available_tables')

]
