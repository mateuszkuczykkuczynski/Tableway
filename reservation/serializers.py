from rest_framework import serializers
from .models import Table


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ("restaurant_name", "location", "capacity", "is_reserved", "reserved_time")

    def get_restaurant_name(self, obj):
        return obj.location.name


class TableSerializerEditableFields(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ("reserved_time",)

