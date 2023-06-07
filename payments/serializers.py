from rest_framework import serializers
from .models import Payment


class CreatePaymentForReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("reservation", "amount")


class CompletePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("completed",)
