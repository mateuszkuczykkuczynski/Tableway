from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
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
