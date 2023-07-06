from django.urls import path

from .views import (CreatePaymentView, AllRestaurantReservationsPaymentsView,AllUserReservationsPaymentsView,
                    CompletePaymentView, TipEmployeeView, AllUserTipsView, AllEmployeeTipsView, AllRestaurantTipsView,
                    AllEmployeeTipsRestaurantOwnerView)
# TO DO check if works fine
urlpatterns = [
    path('create/<int:restaurant_id>/', CreatePaymentView.as_view(), name='create_payment'),   # To test
    path('complete/<int:payment_id>/', CompletePaymentView.as_view(), name='complete_payment'),    # To test
    path('restaurant_all/<int:restaurant_id>/', AllRestaurantReservationsPaymentsView.as_view(),
         name='restaurant_all_payments'),   # To test
    path('user_all/<int:user_id>/', AllUserReservationsPaymentsView.as_view(),
         name='user_all_payments'),     # To test
    path('tips/<int:reservation_id>/', TipEmployeeView.as_view(),
         name='tip_employee'),  # To test
    path('tips/user_all/<int:user_id>', AllUserTipsView.as_view(),
         name='user_all_tips'),     # To test
    path('tips/employee_all/<int:employee_id>', AllEmployeeTipsView.as_view(),
         name='employee_all_tips'),     # To test
    path('tips/restaurant_all/<int:restaurant_id>', AllRestaurantTipsView.as_view(),
         name='restaurant_all_tips'),   # To test
    path('tips/restaurant_employees/<int:employee_id>', AllEmployeeTipsRestaurantOwnerView.as_view(),
         name='restaurant_employees_all_tips'),     # To test
]
