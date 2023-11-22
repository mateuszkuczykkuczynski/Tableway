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
from .tasks import send_feedback_email_after_tip_task, send_feedback_email_after_payment_task


class CreatePaymentView(CreateAPIView):
    """
    Allows creating a payment object with appropriate permissions.

    After a successful payment creation, a Celery task (`send_feedback_email_after_payment_task`) is triggered
    to handle asynchronous operations related to the payment, such as sending feedback emails.
    """
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
        # Working on passing variables into celery task in "the most efficient" way.
        send_feedback_email_after_payment_task.delay()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['reservations'] = self.get_queryset()
        return context


class CompletePaymentView(UpdateAPIView):
    """Allows completing a payment."""
    serializer_class = CompletePaymentSerializer
    permission_classes = (IsOwnerOrAdminOfPayment,)
    lookup_field = 'id'

    def get_queryset(self):
        return Payment.objects.all()


class AllRestaurantReservationsPaymentsView(ListAPIView):
    """Lists all payments for a restaurant's reservations."""
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant_payments = Payment.objects.filter(reservation__table_number__location=restaurant_id)
        return restaurant_payments


class AllUserReservationsPaymentsView(ListAPIView):
    """Lists all payments for a user's reservations."""
    serializer_class = PaymentsDetailsSerializer
    permission_classes = (IsOwnerOrAdminOfUserReservations,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(reservation__owner__id=user_id)


class TipEmployeeView(CreateAPIView):
    """
    Allows tipping an employee.

    After successfully tipping an employee, a Celery task (`send_feedback_email_after_tip_task`) is triggered
    to handle asynchronous operations related to the tip, such as sending feedback emails.
    """
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
        # Working on passing variables into celery task in "the most efficient" way.
        send_feedback_email_after_tip_task.delay()
        serializer.save(reservation=reservation)


class AllUserTipsView(ListAPIView):
    """Lists all tips given by a user."""
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
    """Lists all tips received by an employee."""
    serializer_class = AllEmployeeTipsSerializer
    permission_classes = (IsTipsOwnerOrAdmin,)

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        queryset = Tip.objects.filter(employee=employee_id)
        return queryset


class AllRestaurantTipsView(ListAPIView):
    """Lists all tips given in a restaurant."""
    serializer_class = AllRestaurantTipsSerializer
    permission_classes = (IsRestaurantOwnerOrAdmin,)

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        queryset = Tip.objects.filter(reservation__table_number__location=restaurant_id)
        return queryset
