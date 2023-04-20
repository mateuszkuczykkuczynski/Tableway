from rest_framework import serializers
from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ("restaurant_name", "location", "capacity",
                  "is_reserved",)

    def get_restaurant_name(self, obj):
        return obj.location.name


class ReservationSerializerEditableFields(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("reserved_time", "duration", "reserved_time_range",)

