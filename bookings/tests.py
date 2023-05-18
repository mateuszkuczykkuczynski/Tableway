from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import Table, Restaurant

User = get_user_model()


class ReservationSystemTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser11",
            email="testuser11@gmail.com",
            password="TestSecret11!",
            name="Maniek",
            surname="Manikowski",
            is_restaurant=True,
            restaurant_name="Maniana",
            restaurant_address="Wielka 15D",
            restaurant_type="Spanish",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,
        )

        cls.user2 = get_user_model().objects.create_user(
            username="testuser22",
            email="testuser22@gmail.com",
            password="TestSecret22!",
            name="Gagus",
            surname="Gagusiowski",
            is_restaurant=True,
            restaurant_name="Guga",
            restaurant_address="Matrymonialna 82E",
            restaurant_type="Greek",
            two_seats_tables=6,
            four_seats_tables=6,
            more_than_four_seats_tables=4,
        )

        cls.user3 = get_user_model().objects.create_user(
            username="testuser33",
            email="testuser33@gmail.com",
            password="TestSecret33!",
            name="Dareczek",
            surname="Dareczkowski",
            is_restaurant=True,
            restaurant_name="Darkownia",
            restaurant_address="Powstania 11L",
            restaurant_type="American",
            two_seats_tables=8,
            four_seats_tables=6,
            more_than_four_seats_tables=4,
        )

        cls.user4 = get_user_model().objects.create_user(
            username="testuser44",
            email="testuser44@gmail.com",
            password="TestSecret44!",
            name="Rysiek",
            surname="Ryskowski",
            is_restaurant=True,
            restaurant_name="Ryszariada",
            restaurant_address="Demencji 11L",
            restaurant_type="Polish",
            two_seats_tables=8,
            four_seats_tables=6,
            more_than_four_seats_tables=4,
        )

        cls.restaurant_1 = Restaurant.objects.get(name="Darkownia")
        cls.restaurant_2 = Restaurant.objects.get(name="Ryszariada")

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

        cls.table3 = Table.objects.create(
            location=cls.restaurant_2,
            capacity=4,
        )
        cls.table3.reservation.set([])

    def test_available_tables_listview_status_code_if_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("available_tables"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_tables_listview_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("available_tables"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_available_tables_listview_contains_all_tables(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("available_tables"))
        self.assertEqual(len(response.data), Table.objects.count())

    def test_available_tables_listview_contains_correct_tables_data(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("available_tables"))

        for table in Table.objects.all():
            self.assertContains(response, table.capacity)
            self.assertContains(response, table.location)
            self.assertContains(response, "Maniana")
            self.assertContains(response, "Guga")

            reservations = table.reservation.all()
            for reservation in reservations:
                self.assertContains(response, reservation.table_number)

    def test_available_tables_detail_view_status_code_if_authenticated(self):
        self.client.login(username='testuser33', password='TestSecret33!')
        response = self.client.get(reverse("table_details", kwargs={"pk": self.table1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_tables_detail_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("table_details", kwargs={"pk": self.table1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_available_tables_detail_view_status_code_if_table_not_exists(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        response = self.client.get(reverse("table_details", kwargs={"pk": 8888}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_available_tables_detail_view_contains_correct_table_data(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("table_details", kwargs={"pk": self.table1.id}))
        self.assertContains(response, self.table1.location)
        self.assertContains(response, self.table1.capacity)

        reservations = self.table1.reservation.all()
        for reservation in reservations:
            self.assertContains(response, reservation.table_number)

    def test_reserv_table_status_code_if_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        data = {
            "reserved_time": "2023-06-20T00:15:00.725Z",
            "duration": 60
        }
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reserv_table_status_code_if_not_authenticated(self):
        data = {
            "reserved_time": "2023-08-20T00:15:00.725Z",
            "duration": 90
        }
        response = self.client.get(reverse("table_reservation", kwargs={"pk": self.table1.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reserv_table_status_code_if_incorrect_data_type_duration_field_and_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        data = {
            "reserved_time": "2023-09-20T00:15:00.725Z",
            "duration": "Bagel"
        }
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserv_table_status_code_if_incorrect_data_type_reserved_time_field_and_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        data = {
            "reserved_time": 9090,
            "duration": 75
        }
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table1.id}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reservation_data_correctly_stored_in_db(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        data = {
            "reserved_time": "2023-10-30T00:15:00.725Z",
            "duration": 60
        }
        self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                         data=data, format="json")

        reservations = self.table2.reservation.all()
        for reservation in reservations:
            self.assertEqual(datetime.fromisoformat(data["reserved_time"]), reservation.reserved_time)

    def test_reservation_data_correctly_stored_in_db_vol_2(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        data = {
            "reserved_time": "2023-12-02T00:15:00.725Z",
            "duration": 90
        }
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table1.id}),
                                    data=data, format="json")

        reservations = self.table1.reservation.all()
        for reservation in reservations:
            response_reserved_time = datetime.fromisoformat(response.data["reserved_time"])
            diff = abs(response_reserved_time - reservation.reserved_time)
            self.assertEqual(diff.total_seconds(), 0)

    def test_reserv_table_if_table_already_reserved_status_code(self):
        self.client.login(username='testuser11', password='TestSecret11!')

        data_1 = {
            "reserved_time": "2023-12-02T00:15:00.725Z",
            "duration": 60
        }

        data_2 = {
            "reserved_time": "2023-12-02T00:30:00.725Z",
            "duration": 60
        }

        self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                         data=data_1, format="json")
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                                    data=data_2, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserv_table_in_last_minute_of_current_reservation_status_code(self):
        self.client.login(username='testuser22', password='TestSecret22!')

        data_1 = {
            "reserved_time": "2023-12-24T00:30:00.725Z",
            "duration": 60
        }

        data_2 = {
            "reserved_time": "2023-12-02T01:30:00.725Z",
            "duration": 60
        }

        self.client.post(reverse("table_reservation", kwargs={"pk": self.table1.id}),
                         data=data_1, format="json")
        response = self.client.post(reverse("table_reservation", kwargs={"pk": self.table1.id}),
                                    data=data_2, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reserv_table_status_code_if_table_not_exists_and_authenticated(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        data = {
            "reserved_time": "2023-11-20T00:15:00.725Z",
            "duration": 90
        }
        response = self.client.post(reverse("table_reservation", kwargs={"pk": 9090}),
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_cancel_table_reserv_status_code_if_authenticated_and_autorized(self):
    #     self.client.login(username='testuser44', password='TestSecret44!')
    #     data = {
    #         "reserved_time": "2023-12-22T00:15:00.725Z",
    #         "duration": 90
    #     }
    #     self.client.post(reverse("table_reservation", kwargs={"pk": self.table3.id}),
    #                      data=data, format="json")
    #
    #     table_66666 = Table.objects.first()
    #     response = self.client.delete(reverse("cancel_table_reservation", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)







