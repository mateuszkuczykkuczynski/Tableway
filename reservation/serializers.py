from rest_framework import serializers
from .models import Table, Reservation


# class TableSerializer(serializers.ModelSerializer):
#     # reservations = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all(), many=True)
#     reservations = ReservationSerializer(many=True)
#     restaurant_name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Table
#         fields = ("restaurant_name", "location", "capacity",
#                   "is_reserved", "reservations", )
#
#     def get_restaurant_name(self, obj):
#         return obj.location.name


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ("restaurant_name", "capacity", "reservations")

    def get_restaurant_name(self, obj):
        return obj.location.name

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return ReservationSerializer(reservations, many=True).data


class ReservationSerializer(serializers.ModelSerializer):
    table_list = TableSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'


class ReservationSerializerEditableFields(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("reserved_time", "duration")


class ReservationDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("reserved_time", "reserved_time_end", "table_number")



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
