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


class Reservation(models.Model):
    reserved_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # minutes
    reserved_time_end = models.DateTimeField(null=True, blank=True)
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
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='tables_reserved')

    def is_reserved_on_date(self, date_start, date_end):
        if self.reservation and self.reservation.reserved_time.date() <= date_start and date_end \
                <= self.reservation.reserved_time_end.date():
            # self.is_reserved = True
            return True
        else:
            return False
            # self.is_reserved = False
        # self.save()
        # return self.is_reserved
