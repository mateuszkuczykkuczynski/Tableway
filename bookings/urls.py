from django.urls import path

from .views import AvailableTablesView, TableReservationView, TableDetailsView, \
                    ReservationDetailsView, CancelTableReservationView, EmployeeCreateView, \
                    EmployeeDetailsView, ReservationAddServiceView, NowAvailableTablesView, \
                    AllRestaurantEmployeesView, AllRestaurantReservationsView, AllUserReservationsView, \
                    ReservationPaymentStatusView, AllEmployeeReservationsView


urlpatterns = [
    path('tables/available/', AvailableTablesView.as_view(), name='available_tables'),  # Tested
    path('tables/available/<int:pk>', TableDetailsView.as_view(), name='table_details'),    # Tested
    path('tables/now_available_all/', NowAvailableTablesView.as_view(),
         name='now_available_tables'),  # Tested
    path('tables/available/reserv/<int:pk>', TableReservationView.as_view(), name='table_reservation'), # Tested
    path('tables/available/cancel_reserv/<int:pk>', CancelTableReservationView.as_view(),
         name='cancel_table_reservation'),  # Tested
    path('tables/reservation_details/<int:pk>', ReservationDetailsView.as_view(), name='reservation_details'),  # Tested
    path('tables/reservation_payment_status/<int:pk>', ReservationPaymentStatusView.as_view(),
         name='reservation_payment_status'),    # Tested
    path('tables/reservation_add_service/<int:pk>', ReservationAddServiceView.as_view(),
         name='reserv_add_service'),    # To test
    path('tables/all_restaurant_reservations/<int:restaurant_id>', AllRestaurantReservationsView.as_view(),
         name='all_restaurant_reservations'),   # To test
    path('tables/all_user_reservation', AllUserReservationsView.as_view(),
         name='all_user_reservations'),     # To test
    path('employees/employee_create/', EmployeeCreateView.as_view(), name='employee_create'),   # To test
    path('employees/employee_details/<int:pk>', EmployeeDetailsView.as_view(), name='employee_details'),    # To test
    path('employees/all_restaurant_employees', AllRestaurantEmployeesView.as_view(), name='all_restaurant_employees'),  # To test
    path('employees/all_employee_reservations', AllEmployeeReservationsView.as_view(),
         name='all_employee_reservations')  # To test

]

