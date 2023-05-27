from typing import Union
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Table, Reservation, Employee


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    table_number = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ("restaurant_name", "table_number", "capacity", "reservations")

    @extend_schema_field(Union[str, None])
    def get_restaurant_name(self, obj):
        return obj.location.name

    @extend_schema_field(Union[str, None])
    def get_reservations(self, obj):
        reservations = obj.reservation.all()
        return ReservationSerializer(reservations, many=True).data

    @extend_schema_field(Union[int, None])
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
        fields = ("reserved_time", "reserved_time_end", "table_number", "owner")


class ReservationPaymentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("paid",)


class RestaurantReservationsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("reserved_time", "reserved_time_end", "table_number")


class UserReservationsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("reserved_time", "reserved_time_end", "table_number")


class EmployeeSerializerEditableFields(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ("name", "surname", "account_number", "works_in", )


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("name", "surname", "account_number", "tips_daily", "tips_monthly", "tips_overall")


class EmployeesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ("name", "surname")


class EmployeeSerializerForAddingReservation(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ("reservation_served",)


class AddEmployeeToReservationSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Reservation
        fields = ("service",)
