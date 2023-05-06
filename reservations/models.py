from django.db import models
from accounts.models import CustomUser
from datetime import timedelta
import datetime


class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=400)
    restaurant_type = models.CharField(max_length=50, choices=CustomUser.RESTAURANT_TYPES)
    restaurant_tables = models.ManyToManyField("reservation.Table")
    restaurant_employees = models.ForeignKey("reservation.Employee", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    reservation_served = models.ForeignKey("reservation.Reservation", on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.CharField(max_length=28)

    # tips_daily =
    # tips_monthly =
    # tips_overall =


class Reservation(models.Model):
    reserved_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # minutes
    reserved_time_end = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    table_number = models.ForeignKey("reservation.Table", on_delete=models.CASCADE, related_name='reservations',
                                     null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.duration and self.reserved_time:
            self.reserved_time_end = self.reserved_time + timedelta(minutes=self.duration)
            super().save(*args, **kwargs)


class Table(models.Model):
    location = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    reservation = models.ManyToManyField(Reservation, blank=True, related_name='tables_reserved')

    def is_reserved_on_date(self, date_start, date_end):
        if self.reservations.filter(reserved_time__lt=date_end, reserved_time_end__gt=date_start).exists():
            self.is_reserved = True
        else:
            self.is_reserved = False

#     def is_reserved_on_date(self, date_start, date_end):
#         if self.reservation:
#             if self.reservation.reserved_time < date_end and self.reservation.reserved_time_end > date_start:
#                 self.is_reserved = True
#             else:
#                 self.is_reserved = False
#         else:
#             self.is_reserved = False



