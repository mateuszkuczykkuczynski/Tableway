from django.db import models
from accounts.models import CustomUser
from datetime import timedelta


class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=400)
    restaurant_type = models.CharField(max_length=50, choices=CustomUser.RESTAURANT_TYPES)
    restaurant_tables = models.ManyToManyField("reservation.Table")

    def __str__(self):
        return self.name


class Table(models.Model):
    location = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    reserved_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # minutes
    reserved_time_end = models.DateTimeField(null=True, blank=True)
    reserved_time_range = models.CharField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.duration and self.reserved_time:
            self.reserved_time_end = self.reserved_time + timedelta(minutes=self.duration)
            self.reserved_time_range = (self.reserved_time, self.reserved_time_end)
        super().save(*args, **kwargs)

