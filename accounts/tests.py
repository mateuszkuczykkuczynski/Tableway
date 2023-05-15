from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from bookings.models import Restaurant, Table


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

    def test_api_users_listview(self):
        self.client.login(username='testuser1', password='TestSecret1!')
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Book.objects.count(), 1)
        # self.assertContains(response, self.book)

