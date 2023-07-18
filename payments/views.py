from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from bookings.models import Reservation
from .models import Payment, Tip
from .serializers import (CreatePaymentForReservationSerializer, PaymentsDetailsSerializer, CompletePaymentSerializer,
                          TipEmployeeSerializer, AllUserTipsSerializer, AllEmployeeTipsSerializer,
                          AllRestaurantTipsSerializer)
from .permissions import (IsReservationOwnerOrAdmin, IsRestaurantOwnerOrAdmin, IsTipsCreatorOrAdmin,
                          IsRestaurantOwnerWithTipsOrAdmin, IsRestaurantEmployeeOrOwnerPermission,
                          IsReservationOwner, CanPerformTipCreation)


class CreatePaymentView(CreateAPIView):
    serializer_class = CreatePaymentForReservationSerializer
    permission_classes = (IsRestaurantEmployeeOrOwnerPermission,)

    def get_queryset(self):
        reservations = Reservation.objects.filter(
            table_number__location_id=self.kwargs['restaurant_id'],
            paid=False
        )
        if reservations.exists():
            return reservations
        else:
            raise NotFound("No reservations found.")

    def perform_create(self, serializer):
        reservation_id = serializer.validated_data['reservation_choice'].id
        amount = serializer.validated_data['amount']
        Payment.objects.create(reservation_id=reservation_id, amount=amount)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['reservations'] = self.get_queryset()
        return context

    # def create(self, request, *args, **kwargs):
    #     try:
    #         return super().create(request, *args, **kwargs)
    #     except NotFound:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

        # if not user.is_employee or not user.employee.restaurant_id == restaurant_id:
        #     raise PermissionDenied("You are not authorized to create a payment for this reservation")


class AllRestaurantReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant_payments = Payment.objects.filter(reservation__table_number__location=restaurant_id)
        return restaurant_payments
        # if self.request.user == payments.reservation.owner:
        #     return payments
        # else:
        #     raise PermissionDenied


class AllUserReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsReservationOwner,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(reservation__owner__id=user_id)


class CompletePaymentView(UpdateAPIView):
    serializer_class = CompletePaymentSerializer
    permission_classes = (IsReservationOwnerOrAdmin,)
    lookup_field = 'id'

    # def get_queryset(self):
    #     payment_id = self.kwargs['payment_id']
    #     return Payment.objects.get(id=payment_id)
    def get_queryset(self):
        return Payment.objects.all()


class TipEmployeeView(CreateAPIView):
    serializer_class = TipEmployeeSerializer
    permission_classes = (CanPerformTipCreation,)

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
