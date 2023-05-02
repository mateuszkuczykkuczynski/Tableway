from rest_framework import serializers
from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    table_number = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ("restaurant_name", "table_number", "capacity", "reservations")

    def get_restaurant_name(self, obj):
        return obj.location.name

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return ReservationSerializer(reservations, many=True).data

    def get_table_number(self, obj):
        if obj.id:
            return obj.id
        return None


class ReservationSerializer(serializers.ModelSerializer):
    table_list = TableSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("reserved_time", "duration", "reserved_time_end", "table_list")


class ReservationSerializerEditableFields(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("reserved_time", "duration")


class ReservationDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("reserved_time", "reserved_time_end", "table_number")


