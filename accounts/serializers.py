from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers, relations
from cities_light.models import Country, City

User = get_user_model()


class CustomRegistration(RegisterSerializer):
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    is_restaurant = serializers.BooleanField(required=False, default=False)
    restaurant_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    restaurant_address = serializers.CharField(required=False, allow_blank=True, max_length=400)
    restaurant_type = serializers.ChoiceField(required=False, allow_blank=True,
                                              choices=User.RESTAURANT_TYPES)
    restaurant_city = serializers.PrimaryKeyRelatedField( queryset=City.objects.all())
    restaurant_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    two_seats_tables = serializers.IntegerField(required=False, default=0)
    four_seats_tables = serializers.IntegerField(required=False, default=0)
    more_than_four_seats_tables = serializers.IntegerField(required=False, default=0)

    # def get_restaurant_country(self, obj):
    #     countries = Country.objects.all()
    #     return countries
    #
    # def get_restaurant_city(self, obj):
    #     cities = City.objects.all()
    #     return cities

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
