from datetime import datetime, date
from urllib.parse import urlencode
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Table, Restaurant, Reservation, Employee

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

        cls.user5 = get_user_model().objects.create_user(
            username="testuser55",
            email="testuser55@gmail.com",
            password="TestSecret55!",
            name="Tysiek",
            surname="Tysiowski",
            is_restaurant=True,
            restaurant_name="Tysiownia",
            restaurant_address="Zimna 77",
            restaurant_type="Polish",
            two_seats_tables=8,
            four_seats_tables=6,
            more_than_four_seats_tables=4,
        )

        cls.user6 = get_user_model().objects.create_user(
            username="testuser66",
            email="testuser66@gmail.com",
            password="TestSecret66!",
            name="TenBez",
            surname="Restauracji",
            is_restaurant=False,
        )

        cls.restaurant_1 = Restaurant.objects.get(name="Darkownia")
        cls.restaurant_2 = Restaurant.objects.get(name="Ryszariada")
        cls.restaurant_3 = Restaurant.objects.get(name="Tysiownia")

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

        cls.table4 = Table.objects.create(
            location=cls.restaurant_3,
            capacity=4,
        )
        cls.table4.reservation.set([])

        cls.reservation1 = Reservation.objects.create(
            reserved_time="2023-11-11T18:48:41.193000Z",
            reserved_time_end="2023-11-11T19:48:41.193000Z",
            table_number=cls.table4,
            owner=cls.user5,

        )

        cls.reservation2 = Reservation.objects.create(
            reserved_time="2023-11-15T18:48:41.193000Z",
            reserved_time_end="2023-11-15T20:48:41.193000Z",
            table_number=cls.table4,
            owner=cls.user4,

        )

        cls.reservation3 = Reservation.objects.create(
            reserved_time="2023-11-02T18:44:41.193000Z",
            reserved_time_end="2023-11-02T20:44:41.193000Z",
            table_number=cls.table4,
            owner=cls.user1,

        )

        cls.reservation4 = Reservation.objects.create(
            reserved_time="2023-12-19T18:48:41.193000Z",
            reserved_time_end="2023-12-19T19:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user6,

        )

        cls.reservation5 = Reservation.objects.create(
            reserved_time="2023-12-02T18:48:41.193000Z",
            reserved_time_end="2023-12-02T20:48:41.193000Z",
            table_number=cls.table2,
            owner=cls.user6,

        )

        cls.reservation6 = Reservation.objects.create(
            reserved_time="2023-02-08T18:44:41.193000Z",
            reserved_time_end="2023-11-08T20:44:41.193000Z",
            table_number=cls.table2,
            owner=cls.user6,

        )

        cls.employee1 = Employee.objects.create(
            username="testemployee11",
            email="testemployee11@gmail.com",
            password="TestEmployeeSecret11!",
            name="Radek",
            surname="Radzi",
            works_in=cls.restaurant_3,
            account_number=554499001212,
        )

    def test_available_tables_listview_status_code_if_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get("/api/v1/bookings/tables/available/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_tables_listview_status_code_if_authenticated_by_name(self):
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
        response = self.client.get(f"/api/v1/bookings/tables/available/{self.table1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_tables_detail_view_status_code_if_authenticated_by_name(self):
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
            "reserved_time": "2023-02-22T00:15:00.725Z",
            "duration": 60
        }
        response = self.client.post(f"/api/v1/bookings/tables/available/reserv/{self.table2.id}",
                                    data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reserv_table_status_code_if_authenticated_by_name(self):
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

    def test_cancel_table_reserv_status_code_if_authenticated_and_autorized(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "reserved_time": "2023-06-20T00:15:00.725Z",
            "duration": 90
        }
        self.client.post(reverse("table_reservation", kwargs={"pk": self.table3.id}),
                         data=data, format="json")

        obj = self.table3.reservation.get(duration=90)

        response = self.client.delete(f"/api/v1/bookings/tables/available/cancel_reserv/{obj.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_table_reserv_status_code_if_authenticated_and_autorized_by_name(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "reserved_time": "2023-12-22T00:15:00.725Z",
            "duration": 90
        }
        self.client.post(reverse("table_reservation", kwargs={"pk": self.table3.id}),
                         data=data, format="json")

        obj = self.table3.reservation.get(duration=90)

        response = self.client.delete(reverse("cancel_table_reservation", kwargs={"pk": obj.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_table_reserv_status_code_if_authenticated_and_not_autorized(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "reserved_time": "2023-12-28T00:15:00.725Z",
            "duration": 60
        }
        self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                         data=data, format="json")

        obj = self.table2.reservation.get(duration=60)

        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.delete(reverse("cancel_table_reservation", kwargs={"pk": obj.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_table_reserv_delete_method_correctly_deletes_data_from_db(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "reserved_time": "2023-08-20T00:45:00.725Z",
            "duration": 120
        }
        self.client.post(reverse("table_reservation", kwargs={"pk": self.table2.id}),
                         data=data, format="json")

        initial_count = Reservation.objects.all().count()

        obj = self.table2.reservation.get(duration=120)
        self.client.delete(reverse("cancel_table_reservation", kwargs={"pk": obj.id}))

        self.assertEqual(Reservation.objects.all().count(), initial_count - 1)

    def test_now_available_tables_listview_status_code_if_authenticated(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get("/api/v1/bookings/tables/now_available_all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_now_available_tables_listview_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("now_available_tables"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_now_available_tables_listview_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("now_available_tables"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_now_available_tables_listview_contains_all_tables(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("now_available_tables"))
        self.assertEqual(len(response.data), Table.objects.count())

    def test_now_available_tables_listview_contains_correct_data(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("available_tables"))

        self.assertContains(response, self.restaurant_1.name)
        self.assertContains(response, self.restaurant_2.name)
        self.assertContains(response, self.restaurant_3.name)
        self.assertContains(response, self.table1.capacity)
        self.assertContains(response, self.table2.capacity)
        self.assertContains(response, self.table3.capacity)
        self.assertContains(response, self.table4.capacity)
        self.assertContains(response, self.table1.id)
        self.assertContains(response, self.table2.id)
        self.assertContains(response, self.table3.id)
        self.assertContains(response, self.table4.id)

        reservations = self.table4.reservation.all()
        for reservation in reservations:
            self.assertContains(response, reservation.reserved_time)
            self.assertContains(response, reservation.reserved_time_end)

    def test_reservation_details_view_status_code_if_authenticated(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        response = self.client.get(f"/api/v1/bookings/tables/reservation_details/{self.reservation1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_details_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        response = self.client.get(reverse("reservation_details", kwargs={"pk": self.reservation1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_details_view_status_code_if_authenticated_and_not_autorized(self):
        self.client.login(username='testuser11', password='TestSecret11!')
        response = self.client.get(reverse("reservation_details", kwargs={"pk": self.reservation1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_details_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("reservation_details", kwargs={"pk": self.reservation1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_details_view_status_code_if_reservation_not_exists(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        response = self.client.get(reverse("reservation_details", kwargs={"pk": 9696}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reservation_details_view_contains_correct_reservation_data(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        response = self.client.get(reverse("reservation_details", kwargs={"pk": self.reservation1.id}))
        self.assertContains(response, self.reservation1.reserved_time)
        self.assertContains(response, self.reservation1.reserved_time_end)
        self.assertContains(response, self.reservation1.table_number.id)
        self.assertContains(response, self.reservation1.owner.id)

    def test_reservation_payment_status_view_status_code_if_authenticated(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "paid": True
        }
        response = self.client.put(f"/api/v1/bookings/tables/reservation_payment_status/{self.reservation2.id}",
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_payment_status_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "paid": True
        }
        response = self.client.put(reverse("reservation_payment_status", kwargs={"pk": self.reservation2.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_payment_status_status_code_if_authenticated_and_not_autorized(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        data = {
            "paid": True
        }
        response = self.client.put(reverse("reservation_payment_status", kwargs={"pk": self.reservation2.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_payment_status_status_code_if_not_authenticated(self):
        data = {
            "paid": True
        }
        response = self.client.put(reverse("reservation_payment_status", kwargs={"pk": self.reservation2.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_payment_status_status_code_if_reservation_not_exists(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "paid": True
        }
        response = self.client.put(reverse("reservation_payment_status", kwargs={"pk": 6666},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Have to be changer from str "service" to field from model in future (example: Reservation.service)
    def test_reservation_payment_status_view_contains_correct_reservation_data(self):
        self.client.login(username='testuser44', password='TestSecret44!')
        data = {
            "paid": True
        }
        response = self.client.put(f"/api/v1/bookings/tables/reservation_payment_status/{self.reservation2.id}",
                                   data=data, format="json")
        self.assertContains(response, "paid")

    def test_reservation_add_service_view_status_code_if_authenticated(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(f"/api/v1/bookings/tables/reservation_add_service/{self.reservation3.id}",
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_add_service_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(reverse("reserv_add_service", kwargs={"pk": self.reservation3.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_add_service_view_status_code_if_authenticated_and_not_autorized(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(reverse("reserv_add_service", kwargs={"pk": self.reservation3.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_add_service_view_status_code_if_not_authenticated(self):
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(reverse("reserv_add_service", kwargs={"pk": self.reservation3.id},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_add_service_view_status_code_if_reservation_not_exists(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(reverse("reserv_add_service", kwargs={"pk": 7007},
                                           ), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Have to be changer from str "service" to field from model in future (example: Reservation.service)
    def test_reservation_add_service_view_contains_correct_reservation_fields(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        data = {
            "service": self.employee1.id
        }
        response = self.client.put(reverse("reserv_add_service", kwargs={"pk": self.reservation3.id},
                                           ), data=data, format="json")
        self.assertContains(response, "service")

    def test_reservation_add_service_view_contains_correctly_saves_data_in_db(self):
        self.client.login(username='testuser55', password='TestSecret55!')
        data = {
            "service": self.employee1.id
        }
        self.client.put(reverse("reserv_add_service", kwargs={"pk": self.reservation3.id},
                                ), data=data, format="json")

        updated_reserv = Reservation.objects.get(id=self.reservation3.id)
        self.assertEqual(self.employee1, updated_reserv.service)

    def test_all_restaurant_reservations_view_status_code_if_authenticated(self):
        self.client.login(username='testuser33', password='TestSecret33!')

        response = self.client.get(f"/api/v1/bookings/tables/all_restaurant_reservations/{self.restaurant_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_restaurant_reservations_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser33', password='TestSecret33!')

        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_restaurant_reservations_view_status_code_if_and_not_autorized(self):
        self.client.login(username='testuser66', password='TestSecret66!')
        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_restaurant_reservations_view_status_code_if_not_authenticated(self):
        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_restaurant_reservations_view_status_code_if_restaurant_not_exists(self):
        self.client.login(username='testuser33', password='TestSecret33!')

        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": 7007}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_restaurant_reservations_view_contains_correct_reservation_fields_names(self):
        self.client.login(username='testuser33', password='TestSecret33!')
        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertContains(response, "reserved_time")
        self.assertContains(response, "reserved_time_end")
        self.assertContains(response, "table_number")

    def test_all_restaurant_reservations_view_contains_correct_reservations_data(self):
        self.client.login(username='testuser33', password='TestSecret33!')
        response = self.client.get(
            reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id}))
        self.assertContains(response, self.reservation4.reserved_time)
        self.assertContains(response, self.reservation4.reserved_time_end)
        self.assertContains(response, self.reservation4.table_number.id)
        self.assertContains(response, self.reservation5.reserved_time)
        self.assertContains(response, self.reservation5.reserved_time_end)
        self.assertContains(response, self.reservation5.table_number.id)
        self.assertContains(response, self.reservation6.reserved_time)
        self.assertContains(response, self.reservation6.reserved_time_end)
        self.assertContains(response, self.reservation6.table_number.id)

    #   Tests passed but functionality is not ready yet. CHeck for later.
    def test_all_restaurant_reservations_view_status_code_if_additional_query_params(self):
        date_param = str(date.today())
        self.client.login(username='testuser33', password='TestSecret33!')
        response = self.client.get(
            f"/api/v1/bookings/tables/all_restaurant_reservations/{self.restaurant_1.id}?date={date_param}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #   Tests passed but functionality is not ready yet. CHeck for later.
    def test_all_restaurant_reservations_view_status_code_if_additional_query_params_by_name(self):
        date_param = str(date.today())
        self.client.login(username='testuser33', password='TestSecret33!')
        url = reverse("all_restaurant_reservations", kwargs={"restaurant_id": self.restaurant_1.id})
        query_params = urlencode({"date": date_param})
        url_with_params = f"{url}?{query_params}"
        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check from here
    def test_all_user_reservations_view_status_code_if_authenticated(self):
        self.client.login(username='testuser66', password='TestSecret66!')

        response = self.client.get(f"/api/v1/bookings/tables/all_user_reservations/{self.user6.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_user_reservations_view_status_code_if_authenticated_by_name(self):
        self.client.login(username='testuser66', password='TestSecret66!')

        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": self.user6.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_user_reservations_view_status_code_if_and_not_autorized(self):
        self.client.login(username='testuser22', password='TestSecret22!')
        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": self.user6.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_user_reservations_view_status_code_if_not_authenticated(self):
        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": self.user6.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Not possible to check reservation for other user that's why 403 status code
    def test_all_user_reservations_view_status_code_if_user_not_exists(self):
        self.client.login(username='testuser66', password='TestSecret66!')

        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": 420024}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_user_reservations_view_contains_correct_reservation_fields_names(self):
        self.client.login(username='testuser66', password='TestSecret66!')
        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": self.user6.id}))
        self.assertContains(response, "reserved_time")
        self.assertContains(response, "reserved_time_end")
        self.assertContains(response, "table_number")

    def test_all_user_reservations_view_contains_correct_reservations_data(self):
        self.client.login(username='testuser66', password='TestSecret66!')
        response = self.client.get(
            reverse("all_user_reservations", kwargs={"pk": self.user6.id}))
        self.assertContains(response, self.reservation4.reserved_time)
        self.assertContains(response, self.reservation4.reserved_time_end)
        self.assertContains(response, self.reservation4.table_number.id)
        self.assertContains(response, self.reservation5.reserved_time)
        self.assertContains(response, self.reservation5.reserved_time_end)
        self.assertContains(response, self.reservation5.table_number.id)
        self.assertContains(response, self.reservation6.reserved_time)
        self.assertContains(response, self.reservation6.reserved_time_end)
        self.assertContains(response, self.reservation6.table_number.id)
