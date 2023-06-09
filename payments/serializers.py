from rest_framework import serializers
from .models import Payment, Tip


class CreatePaymentForReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("reservation", "amount")


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
