from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from cities_light.models import Country, City

from reservation.models import Restaurant, Table

User = get_user_model()


class CustomRegistration(RegisterSerializer):

    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    is_restaurant = serializers.BooleanField(required=False, default=False)
    restaurant_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    restaurant_address = serializers.CharField(required=False, allow_blank=True, max_length=400)
    restaurant_type = serializers.ChoiceField(required=False, allow_blank=True,
                                              choices=User.RESTAURANT_TYPES)
    restaurant_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    restaurant_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    two_seats_tables = serializers.IntegerField(required=False, default=0)
    four_seats_tables = serializers.IntegerField(required=False, default=0)
    more_than_four_seats_tables = serializers.IntegerField(required=False, default=0)

    def custom_signup(self, request, user):
        if request.POST.get("is_restaurant"):
            restaurant_name = request.POST.get("restaurant_name")
            restaurant_address = request.POST.get("restaurant_address")
            restaurant_type = request.POST.get("restaurant_type")
            restaurant_country = request.POST.get("restaurant_country")
            restaurant_city = request.POST.get("restaurant_city")
            two_seats_tables = request.POST.get("two_seats_tables")
            four_seats_tables = request.POST.get("four_seats_tables")
            more_than_four_seats_tables = request.POST.get("more_than_four_seats_tables")
            user.restaurant_name = restaurant_name
            user.restaurant_address = restaurant_address
            user.restaurant_type = restaurant_type
            user.restaurant_country = Country.objects.get(pk=restaurant_country)
            user.restaurant_city = City.objects.get(pk=restaurant_city)
            user.two_seats_tables = two_seats_tables
            user.four_seats_tables = four_seats_tables
            user.more_than_four_seats_tables = more_than_four_seats_tables
            user.is_restaurant = True
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        user.name = name
        user.surname = surname
        user.save()

    def validate(self, data):
        is_restaurant = data.get("is_restaurant", False)
        required_fields = ["restaurant_name", "restaurant_address", "restaurant_type",
                           "two_seats_tables", "four_seats_tables", "more_than_four_seats_tables"]
        if is_restaurant and not all(data.get(field_name) for field_name in required_fields):
            raise serializers.ValidationError(
                {field_name: f"{field_name}is required for restaurant accounts" for field_name in required_fields if
                 not data.get(field_name)}
            )
        elif not is_restaurant and any(data.get(field_name) for field_name in required_fields):
            raise serializers.ValidationError(
                {field_name: "Fields related to restaurant can only be provided if is_restaurant is True" for field_name
                 in required_fields if data.get(field_name)}
            )
        return data

    def create(self, validated_data):
        is_restaurant = validated_data.pop('is_restaurant')
        restaurant_name = validated_data.pop('restaurant_name', None)
        restaurant_address = validated_data.pop('restaurant_address', None)
        restaurant_type = validated_data.pop('restaurant_type', None)
        restaurant_country = validated_data.pop('restaurant_country', None)
        restaurant_city = validated_data.pop('restaurant_city', None)
        two_seats_tables = validated_data.pop('two_seats_tables', None)
        four_seats_tables = validated_data.pop('four_seats_tables', None)
        more_than_four_seats_tables = validated_data.pop('more_than_four_seats_tables', None)

        instance = super().create(validated_data)

        if is_restaurant:
            print("Creating restaurant and tables...")
            restaurant = Restaurant.objects.create(owner=instance,
                                                   name=restaurant_name,
                                                   address=restaurant_address,
                                                   restaurant_type=restaurant_type,
                                                   country=restaurant_country,
                                                   city=restaurant_city)
            for i in range(two_seats_tables):
                Table.objects.create(location=restaurant, capacity=2)
            for i in range(four_seats_tables):
                Table.objects.create(location=restaurant, capacity=4)
            for i in range(more_than_four_seats_tables):
                Table.objects.create(location=restaurant, capacity=6)
            print("Created restaurant and tables.")

        return instance

    # def custom_signup(self, request, user):
    #     if request.POST.get("is_restaurant"):
    #         user.is_restaurant = True
    #     user.is_restaurant = False
    #     name = request.POST.get("name")
    #     surname = request.POST.get("surname")
    #     restaurant_name = request.POST.get("restaurant_name")
    #     restaurant_address = request.POST.get("restaurant_address")
    #     restaurant_type = request.POST.get("restaurant_type")
    #     restaurant_country = request.POST.get("restaurant_country")
    #     restaurant_city = request.POST.get("restaurant_city")
    #     two_seats_tables = request.POST.get("two_seats_tables")
    #     four_seats_tables = request.POST.get("four_seats_tables")
    #     more_than_four_seats_tables = request.POST.get("more_than_four_seats_tables")
    #     user.restaurant_name = restaurant_name
    #     user.restaurant_address = restaurant_address
    #     user.restaurant_type = restaurant_type
    #     user.restaurant_country = Country.objects.get(pk=restaurant_country)
    #     user.restaurant_city = City.objects.get(pk=restaurant_city)
    #     user.two_seats_tables = two_seats_tables
    #     user.four_seats_tables = four_seats_tables
    #     user.more_than_four_seats_tables = more_than_four_seats_tables
    #     user.name = name
    #     user.surname = surname
    #     user.save()

    # def get_restaurant_country(self, obj):
    #     countries = Country.objects.all()
    #     return countries
    #
    # def get_restaurant_city(self, obj):
    #     cities = City.objects.all()
    #     return cities
