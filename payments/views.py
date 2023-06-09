from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from django.http import Http404

from bookings.models import Reservation
from .models import Payment, Tip
from .serializers import (CreatePaymentForReservationSerializer, PaymentsDetailsSerializer, CompletePaymentSerializer,
                          TipEmployeeSerializer, AllUserTipsSerializer, AllEmployeeTipsSerializer,
                          AllRestaurantTipsSerializer)
from .permissions import (IsReservationOwnerOrAdmin, IsRestaurantOwnerOrAdmin, IsTipsCreatorOrAdmin,
                          IsRestaurantOwnerWithTipsOrAdmin)


class CreatePaymentView(CreateAPIView):
    serializer_class = CreatePaymentForReservationSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Reservation.objects.filter(table_number__location_id=restaurant_id, paid=False)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        # user = self.request.user # For future usage

        try:
            reservation = Reservation.objects.get(
                table_number__location_id=restaurant_id,
                paid=False
            )
        except Reservation.DoesNotExist:
            raise Http404("Reservation not found or already paid")

        # if not user.is_employee or not user.employee.restaurant_id == restaurant_id:
        #     raise PermissionDenied("You are not authorized to create a payment for this reservation")

        serializer.save(reservation=reservation)


class AllRestaurantReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        payments = Payment.objects.filter(reservation__table_number__location=restaurant_id)
        if self.request.user == payments.reservation.owner:
            return payments
        else:
            raise PermissionDenied


class AllUserReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer

    def get_queryset(self):
        return Payment.objects.filter(owner=self.request.user)


class CompletePaymentView(UpdateAPIView):
    serializer_class = CompletePaymentSerializer
    permission_classes = IsReservationOwnerOrAdmin

    def get_queryset(self):
        payment_id = self.kwargs['payment_id']
        return Payment.objects.get(id=payment_id)


class TipEmployeeView(CreateAPIView):
    serializer_class = TipEmployeeSerializer
    permission_classes = IsReservationOwnerOrAdmin

    def get_queryset(self):
        reservation_id = self.kwargs['reservation_id']
        return Reservation.objects.get(id=reservation_id)

    def perform_create(self, serializer):
        reservation_id = self.kwargs['reservation_id']

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise Http404("Reservation not found.")

        serializer.save(reservation=reservation)


class AllUserTipsView(ListAPIView):
    serializer_class = AllUserTipsSerializer
    permission_classes = IsTipsCreatorOrAdmin

    def get_queryset(self):
        queryset = Tip.objects.filter(reservation__owner=self.request.user)
        if not queryset.exists():
            raise PermissionDenied("You are not authorized to access this resource.")
        return queryset


class AllEmployeeTipsView(ListAPIView):
    serializer_class = AllEmployeeTipsSerializer

    def get_queryset(self):
        queryset = Tip.objects.filter(employee=self.request.user)
        return queryset


class AllRestaurantTipsView(ListAPIView):
    serializer_class = AllRestaurantTipsSerializer
    permission_classes = IsRestaurantOwnerWithTipsOrAdmin

    def get_queryset(self):
        restaurant_id = self.kwargs['payment_id']
        queryset = Tip.objects.filter(reservation__table_number__location=restaurant_id)
        return queryset


class AllEmployeeTipsRestaurantOwnerView(ListAPIView):
    serializer_class = AllEmployeeTipsSerializer

    def get_queryset(self):
        queryset = Tip.objects.filter(employee=self.request.user)
        return queryset
