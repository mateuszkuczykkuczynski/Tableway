from django.test import TestCase
from django.contrib.auth import get_user_model

from bookings.models import Restaurant

class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="TestSecret1!",
            name="Jasiek",
            surname="Jacusiowski",
            is_restaurant=True,
            restaurant_name="JaskowaPrzystan",
            # restaurant_country="Aruba",
            restaurant_address="Bundesliga 11A",
            restaurant_type="Asian",
            two_seats_tables=4,
            four_seats_tables=4,
            more_than_four_seats_tables=2,


        )

    def test_user_model(self):
        self.assertEqual(self.user.username, "testuser1")
        self.assertEqual(self.user.email, "testuser1@gmail.com")
        self.assertEqual(self.user.name, "Jasiek")
        self.assertEqual(self.user.surname, "Jacusiowski")
        self.assertEqual(self.user.is_restaurant, True)
        self.assertEqual(self.user.restaurant_name, "JaskowaPrzystan")
        # self.assertEqual(self.user.restaurant_country, "Aruba")
        self.assertEqual(self.user.restaurant_address, "Bundesliga 11A")
        self.assertEqual(self.user.restaurant_type, "Asian")
        self.assertEqual(self.user.two_seats_tables, 4)
        self.assertEqual(self.user.four_seats_tables, 4)
        self.assertEqual(self.user.more_than_four_seats_tables, 2)

    def test_automaticlly_create_restaurant_model(self):
        self.assertEqual(Restaurant.objects.filter(owner=) "testuser1")
        self.assertEqual(self.user.email, "testuser1@gmail.com")
        self.assertEqual(self.user.name, "Jasiek")
        self.assertEqual(self.user.surname, "Jacusiowski")
        self.assertEqual(self.user.is_restaurant, True)
        self.assertEqual(self.user.restaurant_name, "JaskowaPrzystan")
        # self.assertEqual(self.user.restaurant_country, "Aruba")
        self.assertEqual(self.user.restaurant_address, "Bundesliga 11A")
        self.assertEqual(self.user.restaurant_type, "Asian")
        self.assertEqual(self.user.two_seats_tables, 4)
        self.assertEqual(self.user.four_seats_tables, 4)
        self.assertEqual(self.user.more_than_four_seats_tables, 2)

