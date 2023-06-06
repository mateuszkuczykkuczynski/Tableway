from rest_framework import serializers
from .models import Payment


class ReservationPayment(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("reservation", "amount")


