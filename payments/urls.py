from django.urls import path
from .views import CreatePaymentView


urlpatterns = [
path('payments/create/<int:restaurant_id>/', CreatePaymentView.as_view(), name='create_payment')
]
# TODO urls paths for views
