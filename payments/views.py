from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied
from django.http import Http404

from .models import Payment
from bookings.models import Reservation
from .serializers import CreatePaymentForReservationSerializer


class CreatePaymentView(CreateAPIView):
    serializer_class = CreatePaymentForReservationSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Reservation.objects.filter(table_number__location_id=restaurant_id, paid=False)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        user = self.request.user

        try:
            reservation = Reservation.objects.get(
                table_number__location_id=restaurant_id,
                paid=False
            )
        except Reservation.DoesNotExist:
            raise Http404("Reservation not found or already paid")

        if not user.is_employee or not user.employee.restaurant_id == restaurant_id:
            raise PermissionDenied("You are not authorized to create a payment for this reservation")

        serializer.save(reservation=reservation)


class AllUserReservationsPayments(ListAPIView):
    serializer_class = ReservationPayment

    def get_queryset(self):
        return Payment.objects.filter(reservation__table_number__location=)  # TO DO


class AllRestaurantReservationsPayments(ListAPIView):
    serializer_class = ReservationPayment

    def get_queryset(self):
        return Payment.objects.filter(owner=self.request.user)  # TO DO
