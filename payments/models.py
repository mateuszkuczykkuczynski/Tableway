from django.db import models
import random


class Payment(models.Model):
    """
    Represents a payment made for a reservation.

    Attributes:
        - reservation: The reservation for which the payment is made.
        - amount: The total amount of the payment.
        - secret: A unique secret code for the payment.
        - checkout_url: URL for the payment checkout (for future use).
        - completed: Indicates if the payment is completed or not.
    """
    reservation = models.ForeignKey('bookings.Reservation', on_delete=models.SET_NULL, related_name='payments',
                                    null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)  # For future usage
    completed = models.BooleanField(default=False)

    def generate_secret(self):
        self.secret = str(random.randint(10000, 999999))

    def update_reservation_paid_status(self):
        if self.completed and self.reservation:
            self.reservation.paid = True
            self.reservation.save()

    # def update_payment_status(self):
    #     if self.amount:
    #         self.completed = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_secret()
        # self.update_payment_status()
        super().save(*args, **kwargs)
        self.update_reservation_paid_status()


class Tip(models.Model):
    """
    Represents a tip given to an employee for a reservation.

    Attributes:
        - employee: The employee who received the tip.
        - reservation: The reservation for which the tip is given.
        - amount: The total amount of the tip.
        - secret: A unique secret code for the tip.
        - checkout_url: URL for the tip checkout (for future use).
        - received: Indicates if the tip has been received or not.
        - date: The date and time when the tip was given.
    """
    employee = models.ForeignKey('bookings.Employee', on_delete=models.SET_NULL, related_name='received_tips',
                                 null=True)
    reservation = models.ForeignKey('bookings.Reservation', on_delete=models.SET_NULL, related_name='tips', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    secret = models.CharField(max_length=1000, default="", blank=True)
    checkout_url = models.CharField(max_length=1000, default="", blank=True)  # For future usage
    received = models.BooleanField(default=False)
    date = models.DateTimeField()  # To test!

    def generate_secret(self):
        self.secret = str(random.randint(10000, 99999))

    def save(self, *args, **kwargs):
        if self.reservation:
            self.date = self.reservation.reserved_time
        super().save(*args, **kwargs)
