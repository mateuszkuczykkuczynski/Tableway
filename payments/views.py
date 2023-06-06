from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Payment
from .serializers import ReservationPayment


# class PayForReservationView(CreateAPIView):
#
#     def get_queryset(self):
#         # TO DO: Logic for ability to pay only for user reservations.
