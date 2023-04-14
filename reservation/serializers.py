from rest_framework import serializers
from .models import Table, Restaurant


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ("location", "capacity", "is_reserved", "reserved_time")


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "address", "restaurant_type")
