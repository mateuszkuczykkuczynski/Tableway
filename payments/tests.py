from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Tip, Payment
from bookings.models import Employee, Restaurant, Table, Reservation


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
            service=cls.employee1,
        )

        cls.reservation2 = Reservation.objects.create(
            reserved_time="2023-11-15T18:48:41.193000Z",
            reserved_time_end="2023-11-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
            service=cls.employee1,
        )

        cls.reservation3 = Reservation.objects.create(
            reserved_time="2023-06-15T18:48:41.193000Z",
            reserved_time_end="2023-06-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
            service=cls.employee1,

        )

        cls.reservation4 = Reservation.objects.create(
            reserved_time="2023-02-15T18:48:41.193000Z",
            reserved_time_end="2023-02-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
            service=cls.employee1,
        )

        cls.reservation5 = Reservation.objects.create(
            reserved_time="2023-12-15T18:48:41.193000Z",
            reserved_time_end="2023-12-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
            service=cls.employee1,

        )

        cls.reservation6 = Reservation.objects.create(
            reserved_time="2023-01-15T18:48:41.193000Z",
            reserved_time_end="2023-01-15T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user2,
            service=cls.employee1,
        )

        cls.payment1 = Payment.objects.create(
            reservation=cls.reservation1,
            amount=101
        )

        cls.payment2 = Payment.objects.create(
            reservation=cls.reservation2,
            amount=99
        )

        cls.tip1 = Tip.objects.create(
            reservation=cls.reservation3,
            amount=22
        )

        cls.tip2 = Tip.objects.create(
            reservation=cls.reservation4,
            amount=44
        )

        cls.tip3 = Tip.objects.create(
            reservation=cls.reservation5,
            amount=22,
            employee=cls.employee1,
        )

        cls.tip4 = Tip.objects.create(
            reservation=cls.reservation6,
            amount=44,
            employee=cls.employee1,
        )

    # Part 1 (create_payment)
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

    def test_create_payment_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        data = {
            "reservation_choice": self.reservation1.id,
            "amount": 90
        }
        response = self.client.post(reverse("create_payment", kwargs={"restaurant_id": 20202020}),
                                    data=data, format="json")
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 403 priority over 401

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

    # Part 2 (complete_payment)
    def test_complete_payment_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "completed": True
        }
        response = self.client.put(f"/api/v1/payments/complete/{self.payment1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_payment_view_status_code_if_authenticated_and_authorized_admin_restaurant_owner(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        data = {
            "completed": True
        }
        response = self.client.put(f"/api/v1/payments/complete/{self.payment1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Permissions problem to check
    # def test_complete_payment_view_status_code_if_authenticated_and_authorized_admin_reservation_service(self):
    #     self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
    #     data = {
    #         "completed": True
    #     }
    #     response = self.client.put(f"/api/v1/payments/complete/{self.payment1.id}/", data=data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_payment_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "completed": True
        }
        response = self.client.put(reverse("complete_payment", kwargs={"id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_payment_view_status_code_if_not_authenticated(self):
        data = {
            "completed": True
        }
        response = self.client.put(reverse("complete_payment", kwargs={"id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_payment_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "completed": True
        }
        response = self.client.put(reverse("complete_payment", kwargs={"id": self.payment1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_payment_view_status_code_if_payment_not_exists(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "completed": True
        }
        response = self.client.put(reverse("complete_payment", kwargs={"id": 50055005}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # 403 priority over 404 (for safety purpose)

    # Part 3 (restaurant_all_payments)
    def test_restaurant_all_payments_view_status_code_if_authenticated(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(f"/api/v1/payments/restaurant_all/{self.restaurant_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_payments_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_payments_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_payments_view_status_code_if_authenticated_and_not_authorized_client(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_payments_view_status_code_if_authenticated_and_not_authorized_restaurant_employee(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_payments_view_contains_correct_data(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertContains(response, self.payment1.amount)
        self.assertContains(response, self.payment1.reservation.id)
        # self.assertContains(response, self.payment1.completed)

    def test_restaurant_all_payments_view_contains_correct_instances_length(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_payments", kwargs={"restaurant_id": self.restaurant_1.id}))
        restaurant_payments = Payment.objects.filter(reservation__table_number__location=self.restaurant_1)
        self.assertEqual(len(response.data), restaurant_payments.count())

    # Part 4 (user_all_payments)
    def test_user_all_payments_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(f"/api/v1/payments/user_all/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_payments_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_payments_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_payments_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_payments_view_status_code_if_user_not_exists(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": 44660088}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Because of permission 403 comes before 404

    def test_user_all_payments_view_contains_correct_instances_length(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": self.user2.id}))
        user_payments = Payment.objects.filter(reservation__owner__id=self.user2.id)
        self.assertEqual(len(response.data), user_payments.count())

    def test_user_all_payments_view_contains_correct_data(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_payments", kwargs={"user_id": self.user2.id}))
        self.assertContains(response, self.payment1.amount)
        self.assertContains(response, self.payment2.amount)
        self.assertContains(response, self.payment1.reservation.id)
        self.assertContains(response, self.payment2.reservation.id)
        # self.assertContains(response, self.payment1.completed)

    # Part 5 (tip_employee)
    def test_tip_employee_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 20
        }
        response = self.client.post(f"/api/v1/payments/tips/create/{self.reservation1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tip_employee_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 200
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tip_employee_view_status_code_if_not_authenticated(self):
        data = {
            "amount": 2000
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tip_employee_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        data = {
            "amount": 20000
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tip_employee_view_status_code_if_reservation_not_exists(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 20000
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": 77777}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tip_employee_view_status_code_if_amount_is_string(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": "Cyberpunk"
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tip_employee_view_response_if_amount_is_string(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": "Cyberpunk"
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["A valid integer is required."])

    def test_tip_employee_view_status_code_if_amount_is_negative(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": -8008
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tip_employee_view_response_if_amount_is_negative(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": -8008
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["Amount cannot be negative"])

    def test_tip_employee_view_status_code_if_amount_is_longer_then_eight_digits(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 700790094004
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tip_employee_view_response_if_amount_is_longer_then_eight_digits(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 700790094004
        }
        response = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                    data=data, format="json")
        self.assertEqual(response.data['amount'], ["Amount cannot be bigger than eight digits"])

    def test_tip_employee_view_status_code_if_more_then_one_tip_per_reservation(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 2020
        }
        response_1 = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                      data=data, format="json")
        response_2 = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                      data=data, format="json")
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tip_employee_view_response_if_more_then_one_tip_per_reservation(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "amount": 202020
        }
        response_1 = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                      data=data, format="json")
        response_2 = self.client.post(reverse("tip_employee", kwargs={"reservation_id": self.reservation1.id}),
                                      data=data, format="json")
        error_messages = [error for error in response_2.data]
        self.assertEqual(error_messages, ["A tip for this reservation already exists."])
        # self.assertIn('A tip for this reservation already exists.', str(response_2.data)) # Second solution

    # Part 6 (user_all_tips)
    def test_user_all_tips_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(f"/api/v1/payments/tips/user_all/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_tips_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_all_tips_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_all_tips_view_status_code_if_user_not_exists(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": 2244}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Priority over 404

    # Need to create tips on other reservation for tests purpose because of tips creations limitations (done)
    def test_user_all_tips_view_contains_correct_instances_length(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user2.id}))
        user_tips = Tip.objects.filter(reservation__owner__id=self.user2.id)
        self.assertEqual(len(response.data), user_tips.count())

    def test_user_all_tips_view_contains_correct_data(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user_all_tips", kwargs={"user_id": self.user2.id}))
        self.assertContains(response, self.tip1.amount)
        self.assertContains(response, self.tip1.reservation.id)
        self.assertContains(response, self.tip1.date)
        # self.assertContains(response, self.tip1.employee)
        # self.assertContains(response, self.tip1.received)
        self.assertContains(response, self.tip2.amount)
        self.assertContains(response, self.tip2.reservation.id)
        self.assertContains(response, self.tip2.date)
        # self.assertContains(response, self.tip2.employee)
        # self.assertContains(response, self.tip2.received)

    # In works part 7 path('tips/employee_all/<int:employee_id>', AllEmployeeTipsView.as_view(),
    #          name='employee_all_tips'),
    def test_employee_all_tips_view_status_code_if_authenticated(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(f"/api/v1/payments/tips/employee_all/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_all_tips_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_all_tips_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Add permission (done)
    def test_employee_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testemployee2', password='TestEmployeeSecret2!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_all_tips_view_status_code_if_authenticated_and_restaurant_owner(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_all_tips_view_status_code_if_employee_not_exists(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": 3553}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_all_tips_view_contains_correct_instances_length(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        employee_tips = Tip.objects.filter(employee=self.employee1)
        self.assertEqual(len(response.data), employee_tips.count())

    # Employee do not receive tips based on reservation, -> bugfix for later
    def test_employee_all_tips_view_contains_correct_data(self):
        self.client.login(username='testemployee1', password='TestEmployeeSecret1!')
        response = self.client.get(reverse("employee_all_tips", kwargs={"employee_id": self.employee1.id}))
        self.assertContains(response, self.tip3.amount)
        self.assertContains(response, self.tip3.reservation.id)
        self.assertContains(response, self.tip3.date)
        # self.assertContains(response, self.tip3.received)
        self.assertContains(response, self.tip4.amount)
        self.assertContains(response, self.tip4.reservation.id)
        self.assertContains(response, self.tip4.date)
        # self.assertContains(response, self.tip4.received)

    # # In works part 8
    def test_restaurant_all_tips_view_status_code_if_authenticated(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(f"/api/v1/payments/tips/restaurant_all/{self.restaurant_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_tips_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_all_tips_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_tips_view_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_tips_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": 500005}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_all_tips_view_contains_correct_instances_length(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
        restaurant_tips = Tip.objects.filter(reservation__table_number__location=self.restaurant_1)
        self.assertEqual(len(response.data), restaurant_tips.count())

    def test_restaurant_all_tips_view_contains_correct_data(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("restaurant_all_tips", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertContains(response, self.tip1.amount)
        self.assertContains(response, self.tip1.reservation.id)
        self.assertContains(response, self.tip1.date)
        # self.assertContains(response, self.tip3.received)
        self.assertContains(response, self.tip2.amount)
        self.assertContains(response, self.tip2.reservation.id)
        self.assertContains(response, self.tip2.date)
        # self.assertContains(response, self.tip4.received)
        self.assertContains(response, self.tip3.amount)
        self.assertContains(response, self.tip3.reservation.id)
        self.assertContains(response, self.tip3.date)
        # self.assertContains(response, self.tip3.received)
        self.assertContains(response, self.tip4.amount)
        self.assertContains(response, self.tip4.reservation.id)
        self.assertContains(response, self.tip4.date)
        # self.assertContains(response, self.tip4.received)
