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

            restaurant = Restaurant.objects.create(owner=user,
                                                   name=restaurant_name,
                                                   address=restaurant_address,
                                                   restaurant_type=restaurant_type,
                                                   country=user.restaurant_country,
                                                   city=user.restaurant_city)

            if user.two_seats_tables.isdigit():
                for i in range(int(user.two_seats_tables)):
                    Table.objects.create(location=restaurant, capacity=2)
            else:
                user.two_seats_tables = 0

            if user.four_seats_tables.isdigit():
                for i in range(int(user.four_seats_tables)):
                    Table.objects.create(location=restaurant, capacity=4)
            else:
                user.four_seats_tables = 0

            if user.more_than_four_seats_tables.isdigit():
                for i in range(int(user.more_than_four_seats_tables)):
                    Table.objects.create(location=restaurant, capacity=6)
            else:
                user.more_than_four_seats_tables = 0

        name = request.POST.get("name")
        surname = request.POST.get("surname")
        user.name = name
        user.surname = surname
        user.save()

    def validate(self, data):
        is_restaurant = data.get("is_restaurant", False)
        required_fields = ["restaurant_name", "restaurant_address", "restaurant_type"]
        if is_restaurant and not all(data.get(field_name) for field_name in required_fields):
            raise serializers.ValidationError(
                {field_name: f"{field_name}is required for restaurant accounts" for field_name in required_fields if
                 not data.get(field_name)}
            )
        elif not is_restaurant and any(data.get(field_name) for field_name in required_fields):
            raise serializers.ValidationError(
                {field_name: "Fields related to restaurant. Can only be provided if you are running a restaurant" for
                 field_name in required_fields if data.get(field_name)}
            )
        return data


