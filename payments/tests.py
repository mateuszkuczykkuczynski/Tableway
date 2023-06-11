from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Tip, Payment
from bookings.models import Employee, Restaurant, Table, Reservation
from accounts.models import CustomUser


class PaymentSystemTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="TestSecret1!",
            name="Pierwszy",
            surname="BardziejPierwszy",
            is_restaurant=True,
            restaurant_name="Pierwsza",
            restaurant_address="Pierwsza 1",
            restaurant_type="Spanish",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,
        )

        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@gmail.com",
            password="TestSecret2!",
            name="Drugi",
            surname="BardziejDrugi",
        )

        cls.restaurant_1 = Restaurant.objects.get(name="Pierwsza")

        cls.employee1 = Employee.objects.create_user(
            username="testemployee1",
            email="testemployee1@gmail.com",
            password="TestEmployeeSecret1!",
            name='Biedny',
            surname="Student",
            works_in=cls.restaurant_1,
            account_number=554499001212,
        )

        cls.table1 = Table.objects.create(
            location=cls.restaurant_1,
            capacity=2,
        )
        cls.table1.reservation.set([])

        cls.table2 = Table.objects.create(
            location=cls.restaurant_1,
            capacity=4,
        )
        cls.table2.reservation.set([])

        cls.reservation1 = Reservation.objects.create(
            reserved_time="2023-11-22T18:48:41.193000Z",
            reserved_time_end="2023-11-22T19:48:41.193000Z",
            table_number=cls.table1,
            owner=cls.user2,
        )

        cls.reservation2 = Reservation.objects.create(
            reserved_time="2023-11-15T18:48:41.193000Z",
            reserved_time_end="2023-11-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
        )

    # path('create/<int:restaurant_id>/', CreatePaymentView.as_view(), name='create_payment')
    def test_create_payment_view_status_code_if_authenticated(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(f"/api/v1/payments/create/{self.restaurant_1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_payment_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_payment_view_status_code_if_not_authenticated(self):
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_payment_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": 20202020}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
