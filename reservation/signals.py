from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from reservation.models import Restaurant, Table


@receiver(post_save, sender=CustomUser)
def create_restaurant(sender, instance, created, **kwargs):
    if created and instance.is_restaurant:
        print("Creating restaurant and tables...")
        restaurant = Restaurant.objects.create(owner=instance,
                                               name=instance.restaurant_name,
                                               address=instance.restaurant_address,
                                               restaurant_type=instance.restaurant_type)
        table_2 = Table.objects.create(restaurant=restaurant, capacity=2)
        table_4 = Table.objects.create(restaurant=restaurant, capacity=4)
        table_more = Table.objects.create(restaurant=restaurant, capacity=6)
        print("Created restaurant and tables.")
