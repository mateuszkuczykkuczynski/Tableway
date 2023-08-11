from rest_framework import serializers

from .models import Payment, Tip
from bookings.models import Reservation


class CreatePaymentForReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a payment associated with a reservation.
    Validates the amount to ensure it's non-negative and not larger than eight digits.
    """
    reservation_choice = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.none())
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        if len(str(value)) > 8:
            raise serializers.ValidationError("Amount cannot be bigger than eight digits")
        return value

    class Meta:
        model = Payment
        fields = ['amount', 'reservation_choice']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_choice'].queryset = self.context['reservations']


class PaymentsDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer to provide details of a payment, including its completion status, associated reservation, and amount.
    """

    class Meta:
        model = Payment
        fields = ("completed", "reservation", "amount",)


class CompletePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to update the completion status of a payment.
    """
    class Meta:
        model = Payment
        fields = ("completed",)


class TipEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for tipping an employee.
    Validates the tip amount to ensure it's non-negative and not larger than eight digits.
    """
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        if len(str(value)) > 8:
            raise serializers.ValidationError("Amount cannot be bigger than eight digits")
        return value

    class Meta:
        model = Tip
        fields = ("reservation", "amount",)


class AllUserTipsSerializer(serializers.ModelSerializer):
    """
    Serializer to list all tips associated with a user, including details like reservation, amount, date, receipt status, and the employee who received the tip.
    """
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received", "employee")


class AllEmployeeTipsSerializer(serializers.ModelSerializer):
    """
    Serializer to list all tips received by an employee, including details like reservation, amount, date, and receipt status.
    """
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received",)


class AllRestaurantTipsSerializer(serializers.ModelSerializer):
    """
    Serializer to list all tips associated with a restaurant, including details like reservation, amount, date, receipt status, and a secret field.
    """
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received", "secret")
