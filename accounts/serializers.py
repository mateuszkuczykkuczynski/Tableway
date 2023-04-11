from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomRegistration(RegisterSerializer):
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    is_restaurant = serializers.BooleanField(required=False, default=False)
    restaurant_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    restaurant_address = serializers.CharField(required=False, allow_blank=True, max_length=400)
    restaurant_type = serializers.ChoiceField(required=False, allow_blank=True,
                                              choices=User.RESTAURANT_TYPES)
    two_seats_tables = serializers.IntegerField(required=False, default=0)
    four_seats_tables = serializers.IntegerField(required=False, default=0)
    more_than_four_seats_tables = serializers.IntegerField(required=False, default=0)

    def custom_signup(self, request, user):
        if request.POST.get("is_restaurant"):
            restaurant_name = request.POST.get("restaurant_name")
            restaurant_address = request.POST.get("restaurant_address")
            restaurant_type = request.POST.get("restaurant_type")
            two_seats_tables = request.POST.get("two_seats_tables")
            four_seats_tables = request.POST.get("four_seats_tables")
            more_than_four_seats_tables = request.POST.get("more_than_four_seats_tables")
            user.restaurant_name = restaurant_name
            user.restaurant_address = restaurant_address
            user.restaurant_type = restaurant_type
            user.two_seats_tables = two_seats_tables
            user.four_seats_tables = four_seats_tables
            user.more_than_four_seats_tables = more_than_four_seats_tables
            user.is_restaurant = True
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        user.name = name
        user.surname = surname
        user.save()
