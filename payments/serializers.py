from rest_framework import serializers

from .models import Payment, Tip
from bookings.models import Reservation


class CreatePaymentForReservationSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Payment
        fields = ("completed", "reservation", "amount",)


class CompletePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("completed",)


class TipEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tip
        fields = ("reservation", "amount",)


class AllUserTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received", "employee")


class AllEmployeeTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received",)


class AllRestaurantTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ("reservation", "amount", "date", "received", "secret")
