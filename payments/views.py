from django.http import Http404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound



from bookings.models import Reservation
from .models import Payment, Tip
from .serializers import (CreatePaymentForReservationSerializer, PaymentsDetailsSerializer, CompletePaymentSerializer,
                          TipEmployeeSerializer, AllUserTipsSerializer, AllEmployeeTipsSerializer,
                          AllRestaurantTipsSerializer)
from .permissions import (IsRestaurantEmployeeOrOwnerOrAdmin, IsOwnerOrAdminOfPayment, IsRestaurantOwnerOrAdmin,
                          IsTipsCreatorOrAdmin, IsOwnerOrAdminOfUserReservations,
                          CanPerformTipCreation, IsTipsOwnerOrAdmin)


class CreatePaymentView(CreateAPIView):
    serializer_class = CreatePaymentForReservationSerializer
    permission_classes = (IsRestaurantEmployeeOrOwnerOrAdmin,)

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


class CompletePaymentView(UpdateAPIView):
    serializer_class = CompletePaymentSerializer
    permission_classes = (IsOwnerOrAdminOfPayment,)
    lookup_field = 'id'

    def get_queryset(self):
        return Payment.objects.all()


class AllUserReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsOwnerOrAdminOfUserReservations,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(reservation__owner__id=user_id)


class AllRestaurantReservationsPaymentsView(ListAPIView):
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant_payments = Payment.objects.filter(reservation__table_number__location=restaurant_id)
        return restaurant_payments


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

        if Tip.objects.filter(reservation=reservation).exists():
            raise ValidationError("A tip for this reservation already exists.")
        serializer.save(reservation=reservation)


class AllUserTipsView(ListAPIView):
    serializer_class = AllUserTipsSerializer
    permission_classes = (IsTipsCreatorOrAdmin,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Tip.objects.filter(reservation__owner_id=user_id)
        return queryset

    # Second approach
    # def get_queryset(self):
    #    queryset = Tip.objects.filter(reservation__owner=self.request.user.id)
    #     return queryset


class AllEmployeeTipsView(ListAPIView):
    serializer_class = AllEmployeeTipsSerializer
    permission_classes = (IsTipsOwnerOrAdmin,)

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        queryset = Tip.objects.filter(employee=employee_id)
        return queryset


class AllRestaurantTipsView(ListAPIView):
    serializer_class = AllRestaurantTipsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        queryset = Tip.objects.filter(reservation__table_number__location=restaurant_id)
        return queryset


# class AllEmployeeTipsRestaurantOwnerView(ListAPIView):
#     serializer_class = AllEmployeeTipsSerializer
#
#     def get_queryset(self):
#         queryset = Tip.objects.filter(employee=self.request.user)
#         return queryset
