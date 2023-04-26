from rest_framework import serializers
from .models import Table, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    reservation = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = ("restaurant_name", "location", "capacity",
                  "is_reserved", "reservation", )

    def get_restaurant_name(self, obj):
        return obj.location.name


# class TableSerializer(serializers.ModelSerializer):
#     restaurant_name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Table
#         fields = ("restaurant_name", "location", "capacity",
#                   "is_reserved", "reservation", )
#
#     def get_restaurant_name(self, obj):
#         return obj.location.name


class ReservationSerializerEditableFields(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("reserved_time", "duration")


class ReservationDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("reserved_time", "reserved_time_end", "table_number")
