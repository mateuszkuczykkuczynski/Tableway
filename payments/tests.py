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

        cls.payment1 = Payment.objects.create(
            reservation=cls.reservation1,
            amount=101
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
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # status code need to be checked, should be 401 not 403
    def test_create_payment_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": 20202020}),
                                    data=data, format="json")
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    # In works
    def test_complete_payment_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "completed": True
        }
        response = self.client.get(f"/api/v1/payments/complete/{self.payment1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_complete_payment_view_status_code_if_authenticated_and_authorized_admin(self):
    #     self.client.login(username='testuser2', password='TestSecret2!')
    #     data = {
    #         "completed": True
    #     }
    #     response = self.client.get(f"/api/v1/payments/complete/{self.payment1.id}/", data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_payment_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "completed": True
        }
        response = self.client.get(reverse("complete_payment", kwargs={"payment_id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_payment_view_status_code_if_not_authenticated(self):
        data = {
            "completed": True
        }
        response = self.client.get(reverse("complete_payment", kwargs={"payment_id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_payment_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        data = {
            "completed": True
        }
        response = self.client.get(reverse("complete_payment", kwargs={"payment_id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_complete_payment_view_status_code_if_payment_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "completed": True
        }
        response = self.client.get(reverse("complete_payment", kwargs={"payment_id": 50055005}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Other part
    def test_restaurant_all_payments_view_status_code_if_authenticated(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(f"/api/v1/payments/restaurant_all/{self.restaurant_id.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_payments_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')

        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_payments_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_payments_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_all_payments_view_status_code_if_payment_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": 20202020}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # In works part 2
    def test_user_all_reservation_payments_view_status_code_if_authenticated(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')

        response = self.client.get(f"/api/v1/payments/complete/{self.payment_id.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_reservation_payments_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.post(reverse("user_all_payments", kwargs={"payment_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_reservation_payments_view_status_code_if_not_authenticated(self):
        response = self.client.post(reverse("user_all_payments", kwargs={"payment_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_reservation_payments_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        response = self.client.post(reverse("user_all_payments", kwargs={"payment_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_all_reservation_payments_view_status_code_if_payment_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.post(reverse("user_all_payments", kwargs={"payment_id": 20202020}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_all_reservation_payments_view_status_code_if_authenticated(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(f"/api/v1/payments/restaurant_all/{self.restaurant_id.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_reservation_payments_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("user_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_reservation_payments_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("user_all_payments", kwargs={"restaurant_id": self.restaurant_1.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_reservation_payments_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_all_reservation_payments_view_status_code_if_payment_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("user_all_payments", kwargs={"restaurant_id": 20202020}),
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # In works part 3
    # def test_tip_employee_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!e')
    #     data = {
    #         "amount": 90
    #     }
    #     response = self.client.post(f"/api/v1/payments/create/{self.reservation1.id}/", data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_tip_employee_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": 90
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_tip_employee_view_status_code_if_not_authenticated(self):
    #     data = {
    #         "amount": 90
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_tip_employee_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": 110
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # # status code need to be checked, should be 401 not 403
    # def test_tip_employee_view_status_code_if_restaurant_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": 90
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": 20202020}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_tip_employee_view_status_code_if_amount_is_string(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": "Cyberpunk"
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['amount'], ["A valid integer is required."])
    #
    # def test_tip_employee_view_response_if_amount_is_string(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": "Cyberpunk"
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.data['amount'], ["A valid integer is required."])
    #
    # def test_tip_employee_view_status_code_if_amount_is_negative(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": -8008
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_tip_employee_view_response_if_amount_is_negative(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": -8008
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.data['amount'], ["Amount cannot be negative"])
    #
    # def test_tip_employee_view_status_code_if_amount_is_longer_then_eight_digits(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": 700790094004
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_tip_employee_view_response_if_amount_is_longer_then_eight_digits(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     data = {
    #         "amount": 700790094004
    #     }
    #     response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
    #                                 data=data, format="json")
    #     self.assertEqual(response.data['amount'], ["Amount cannot be bigger than eight digits"])

    # In works part 4
    # def test_user_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/user_all/{self.user1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_user_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_user_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_user_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_user_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_user_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/user_all/{self.user1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_user_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_user_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_user_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_user_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("user_all_tips", kwargs={"user_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # In works part 5
    # def test_employee_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/employee_all/{self.employee1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_employee_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_employee_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_employee_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_employee_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_employee_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/employee_all/{self.employee1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_employee_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_employee_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_employee_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_employee_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    # In works part 6
    # def test_restaurant_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/restaurant_all/{self.restaurant_1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_restaurant_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/employee_all/{self.restaurant_1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_restaurant_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # In works part 7
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/restaurant_all/{self.restaurant_1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(f"/api/v1/payments/tips/employee_all/{self.restaurant_1.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated_by_name(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_not_authenticated(self):
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_restaurant_employees_all_tips_view_status_code_if_payment_not_exists(self):
    #     self.client.login(username='testuser1', password='TestSecret1!')
    #     response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": 20202020}))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # In works part 8 (TODO: additional tests in work)
