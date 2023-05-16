from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from bookings.models import Restaurant, Table

User = get_user_model()


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="TestSecret1!",
            name="Jasiek",
            surname="Jacusiowski",
            is_restaurant=True,
            restaurant_name="JaskowaPrzystan",
            restaurant_address="Bundesliga 11A",
            restaurant_type="Asian",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,
        )

        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@gmail.com",
            password="TestSecret2!",
            name="Basiek",
            surname="Basiowski",
            is_restaurant=True,
            restaurant_name="BaskowskaPrzystan",
            restaurant_address="Matematyczna 19B",
            restaurant_type="Mexican",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,

        )

        cls.user3 = get_user_model().objects.create_user(
            username="testuser3",
            email="testuser3@gmail.com",
            password="TestSecret3!",
            name="Rysiek",
            surname="Ryskowski",
            is_restaurant=True,
            restaurant_name="RyskowskaPrzystan",
            restaurant_address="Uzbekistanska 44D",
            restaurant_type="Polish",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,

        )

    def test_user_model(self):
        self.assertEqual(self.user1.username, "testuser1")
        self.assertEqual(self.user1.email, "testuser1@gmail.com")
        self.assertEqual(self.user1.name, "Jasiek")
        self.assertEqual(self.user1.surname, "Jacusiowski")
        self.assertEqual(self.user1.is_restaurant, True)
        self.assertEqual(self.user1.restaurant_name, "JaskowaPrzystan")
        self.assertEqual(self.user1.restaurant_address, "Bundesliga 11A")
        self.assertEqual(self.user1.restaurant_type, "Asian")
        self.assertEqual(self.user1.two_seats_tables, 4)
        self.assertEqual(self.user1.four_seats_tables, 4)
        self.assertEqual(self.user1.more_than_four_seats_tables, 2)

    def test_automaticlly_create_restaurant_model(self):
        restaurant_1 = Restaurant.objects.get(id=1)
        self.assertEqual(restaurant_1.name, "JaskowaPrzystan")
        self.assertEqual(restaurant_1.address, "Bundesliga 11A")
        self.assertEqual(restaurant_1.restaurant_type, "Asian")

    def test_automaticlly_create_table_model(self):
        restaurant_2 = Restaurant.objects.get(id=2)
        self.assertEqual(Table.objects.filter(location=restaurant_2, capacity=2).count(), 4)
        self.assertEqual(Table.objects.filter(location=restaurant_2, capacity=4).count(), 4)
        self.assertEqual(Table.objects.filter(location=restaurant_2, capacity=6).count(), 2)

    def test_api_users_listview_status_code_if_authenticated(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users_listview_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_users_listview_contains_all_users(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        self.assertEqual(User.objects.count(), 3)

    def test_api_users_list_view_contains_correct_users_data(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user-list"))
        self.assertContains(response, self.user1.name)
        self.assertContains(response, self.user1.surname)
        self.assertContains(response, self.user2.name)
        self.assertContains(response, self.user2.surname)

    def test_api_users_detail_view_status_code_if_authenticated(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users_detail_view_status_code_if_not_authenticated(self):
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_users_detail_view_status_code_if_user_not_exists(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        response = self.client.get(reverse("user-detail", kwargs={"pk": 66}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_users_detail_view_contains_correct_user_data(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user2.id}))
        self.assertContains(response, self.user2.name)
        self.assertContains(response, self.user2.surname)

    def test_api_users_put_method_status_code_if_authenticated_and_authorized(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "name": "Zdzisiek",
            "surname": "Zdzisinski"
        }
        response = self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users_put_method_status_code_if_authenticated_and_not_authorized(self):
        self.client.login(username='testuser2', password='TestSecret2!')
        data = {
            "name": "Zdzisiek",
            "surname": "Zdzisinski"
        }
        response = self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_users_put_method_correctly_passes_data(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "name": "Zdzisiu",
            "surname": "Zdzisiunski"
        }
        self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                        data=data, format="json")
        self.assertEqual(User.objects.get(id=3).name, "Zdzisiu")
        self.assertEqual(User.objects.get(id=3).surname, "Zdzisiunski")

    def test_api_users_put_method_status_code_correctly_convert_data_type(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "name": 123456,
            "surname": 654321
        }
        response = self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users_put_method_status_code_correctly_saves_null_value(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "name": None,
            "surname": None
        }
        response = self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                                   data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_users_put_method_correctly_saves_null_value(self):
        self.client.login(username='testuser3', password='TestSecret3!')
        data = {
            "name": None,
            "surname": None
        }
        self.client.put(reverse("user-detail", kwargs={"pk": self.user3.id}),
                        data=data, format="json")
        # TO CHECK WHY!!!!!
        self.assertIsNone(User.objects.get(id=3).name)
        self.assertIsNone(User.objects.get(id=3).surname)
