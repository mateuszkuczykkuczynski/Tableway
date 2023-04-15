from django.urls import path
from .views import AvailableTablesView

urlpatterns = [
    path('tables/available/', AvailableTablesView.as_view(), name='available_tables'),

    # path('restaurants/<str:restaurant>/tables/available/', RestaurantAvailableTablesView.as_view(),
    #      name='available_tables'),
    # path('restaurants_all/available/', AllRestaurantsAvailableTablesView.as_view(),
    #      name='all_available_tables')

]
