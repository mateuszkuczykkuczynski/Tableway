from django.db import models
import random

from reservations.models import Employee, Reservation


class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)

    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))


class Tips(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='received_tips', null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, related_name='tips', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)
    received = models.BooleanField(default=False)
    date = models.DateTimeField()  # TODO - Based on reservation instance!

    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))
