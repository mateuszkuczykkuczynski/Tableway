from django.db import models
import random


class Payment(models.Model):
    reservation = models.ForeignKey('bookings.Reservation', on_delete=models.SET_NULL, related_name='payments', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)

    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))


class Tip(models.Model):
    employee = models.ForeignKey('bookings.Employee', on_delete=models.SET_NULL, related_name='received_tips', null=True)
    reservation = models.ForeignKey('bookings.Reservation', on_delete=models.SET_NULL, related_name='tips', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)
    received = models.BooleanField(default=False)
    date = models.DateTimeField()  # To test!

    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))

    def save(self, *args, **kwargs):
        if self.reservation:
            self.date = self.reservation.reserved_time
        super().save(*args, **kwargs)
