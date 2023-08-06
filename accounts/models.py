from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    CustomUser extends the default AbstractUser model to include additional fields related to the user and restaurant
    details.

    It includes standard user fields like 'name' and 'surname', as well as fields specific to restaurants,
    such as 'restaurant_name', 'restaurant_address', and 'restaurant_type'.

    If a user is a restaurant ('is_restaurant' is True), these additional fields store the details of the restaurant.
    The 'two_seats_tables', 'four_seats_tables', and 'more_than_four_seats_tables' fields store the number of tables of
    each type in the restaurant.

    The 'restaurant_country' and 'restaurant_city' fields are foreign keys to the 'Country' and 'City' models from the
    'cities_light' app (library), respectively.
    """
    RESTAURANT_TYPES = [
        ('asian', 'Asian'),
        ('mexican', 'Mexican'),
        ('italian', 'Italian'),
        ('french', 'French'),
        ('greek', 'Greek'),
        ('american', 'American'),
        ('indian', 'Indian'),
        ('turkish', 'Turkish'),
        ('spanish', 'Spanish'),
        ('polish', 'Polish'),
    ]
    name = models.CharField(null=True, blank=True, max_length=100)
    surname = models.CharField(null=True, blank=True, max_length=100)
    is_restaurant = models.BooleanField(default=False)
    restaurant_name = models.CharField(null=True, blank=True, max_length=200)
    restaurant_country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    restaurant_city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    restaurant_address = models.CharField(null=True, blank=True, max_length=400)
    restaurant_type = models.CharField(null=True, blank=True, max_length=50, choices=RESTAURANT_TYPES)
    two_seats_tables = models.IntegerField(default=0, blank=True)
    four_seats_tables = models.IntegerField(default=0, blank=True)
    more_than_four_seats_tables = models.IntegerField(default=0, blank=True)
