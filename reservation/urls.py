from django.urls import path
from .views import AvailableTablesView, TableReservationView

urlpatterns = [
    path('tables/available/', AvailableTablesView.as_view(), name='available_tables'),
    path('tables/available/<int:pk>', AvailableTablesView.as_view(), name='table_details'),
    path('tables/available/reserv/<int:pk>', TableReservationView.as_view(), name='table_reservation'),
    path('tables/available/cancel_reserv/<int:pk>', TableReservationView.as_view(), name='cancel_table_reservation')
    # path('restaurants/<str:restaurant>/tables/available/', RestaurantAvailableTablesView.as_view(),
    #      name='available_tables'),
    # path('restaurants_all/available/', AllRestaurantsAvailableTablesView.as_view(),
    #      name='all_available_tables')

]
