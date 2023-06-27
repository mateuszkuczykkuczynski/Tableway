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

        cls.user3 = get_user_model().objects.create_user(
            username="testuser3",
            email="testuser3@gmail.com",
            password="TestSecret3!",
            name="Trzeci",
            surname="BardziejTrzeci",
            is_restaurant=True,
            restaurant_name="Druga",
            restaurant_address="Druga 1",
            restaurant_type="Spanish",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,
        )

        cls.restaurant_1 = Restaurant.objects.get(name="Pierwsza")
        cls.restaurant_2 = Restaurant.objects.get(name="Druga")

        cls.employee1 = Employee.objects.create_user(
            username="testemployee1",
            email="testemployee1@gmail.com",
            password="TestEmployeeSecret1!",
            name='Biedny',
            surname="Student",
            works_in=cls.restaurant_1,
            account_number=554499001212,
        )

        cls.employee2 = Employee.objects.create_user(
            username="testemployee2",
            email="testemployee2@gmail.com",
            password="TestEmployeeSecret2!",
            name='Jeszczebiedniejszy',
            surname="Studentdrugi",
            works_in=cls.restaurant_2,
            account_number=554499002222,
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

    def test_create_payment_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 110
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # status code need to be checked, should be 401 not 403 
    def test_create_payment_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": 20202020}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_payment_view_status_code_if_amount_is_string(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": "Cyberpunk"
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['amount'], ["A valid integer is required."])

    def test_create_payment_view_response_if_amount_is_string(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": "Cyberpunk"
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["A valid integer is required."])

    def test_create_payment_view_status_code_if_amount_is_negative(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": -8008
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_view_response_if_amount_is_negative(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": -8008
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["Amount cannot be negative"])

    def test_create_payment_view_status_code_if_amount_is_longer_then_eight_digits(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 700790094004
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_view_response_if_amount_is_longer_then_eight_digits(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 700790094004
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["Amount cannot be bigger than eight digits"])
