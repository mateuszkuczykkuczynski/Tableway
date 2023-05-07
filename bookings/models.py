from django.db import models
from django.db.models import Sum
from datetime import date, datetime, timedelta
import datetime
from decimal import Decimal


from accounts.models import CustomUser
from payments.models import Tip


class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=400)
    restaurant_type = models.CharField(max_length=50, choices=CustomUser.RESTAURANT_TYPES)
    restaurant_tables = models.ManyToManyField("reservations.Table")
    restaurant_employees = models.ForeignKey("reservations.Employee", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    reservation_served = models.ForeignKey("reservations.Reservation", on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.CharField(max_length=28)
    tips_daily = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tips_monthly = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tips_overall = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def calc_tips(self):
        today = date.today()
        month_start = datetime(today.year, today.month, 1)

        sum_amount_daily = Tip.objects.filter(employee=self, date=today).aggregate(Sum('amount'))['amount__sum']
        tips_daily = Decimal(sum_amount_daily) if sum_amount_daily is not None else Decimal(0)

        sum_amount_monthly = Tip.objects.filter(employee=self, date__gte=month_start).aggregate(Sum('amount'))[
                           'amount__sum'] or 0
        tips_monthly = Decimal(sum_amount_monthly) if sum_amount_monthly is not None else Decimal(0)

        sum_amount_overall = Tip.objects.filter(employee=self).aggregate(Sum('amount'))['amount__sum'] or 0
        tips_overall = Decimal(sum_amount_overall) if sum_amount_overall is not None else Decimal(0)

        self.tips_daily = tips_daily
        self.tips_monthly = tips_monthly
        self.tips_overall = tips_overall
        self.save()


class Reservation(models.Model):
    reserved_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # minutes
    reserved_time_end = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    table_number = models.ForeignKey("reservations.Table", on_delete=models.CASCADE, related_name='table_reservations',
                                     null=True, blank=True)
    paid = models.BooleanField(default=False)

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
        if self.reservation.filter(reserved_time__lt=date_end, reserved_time_end__gt=date_start).exists():
            self.is_reserved = True
        else:
            self.is_reserved = False

#     def is_reserved_on_date(self, date_start, date_end):
#         if self.reservations:
#             if self.reservations.reserved_time < date_end and self.reservations.reserved_time_end > date_start:
#                 self.is_reserved = True
#             else:
#                 self.is_reserved = False
#         else:
#             self.is_reserved = False



