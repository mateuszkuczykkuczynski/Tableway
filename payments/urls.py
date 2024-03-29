from django.urls import path

from .views import (CreatePaymentView, AllRestaurantReservationsPaymentsView,
                    AllUserReservationsPaymentsView, CompletePaymentView,
                    TipEmployeeView, AllUserTipsView,
                    AllEmployeeTipsView, AllRestaurantTipsView)

# TODO Couple of fixes left

urlpatterns = [
    path('create/<int:restaurant_id>/', CreatePaymentView.as_view(), name='create_payment'),   # Tested (few fixes left)
    path('complete/<int:id>/', CompletePaymentView.as_view(), name='complete_payment'),    # Tested (one fix left)
    path('restaurant_all/<int:restaurant_id>/', AllRestaurantReservationsPaymentsView.as_view(),
         name='restaurant_all_payments'),   # Tested
    path('user_all/<int:user_id>/', AllUserReservationsPaymentsView.as_view(),
         name='user_all_payments'),     # Tested
    path('tips/create/<int:reservation_id>/', TipEmployeeView.as_view(),
         name='tip_employee'),  # Tested
    path('tips/user_all/<int:user_id>/', AllUserTipsView.as_view(),
         name='user_all_tips'),     # Tested
    path('tips/employee_all/<int:employee_id>/', AllEmployeeTipsView.as_view(),
         name='employee_all_tips'),     # Tested (one bugfix left)
    path('tips/restaurant_all/<int:restaurant_id>/', AllRestaurantTipsView.as_view(),
         name='restaurant_all_tips'),   # Tested
]
