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
        for i in range(instance.two_seats_tables):
            table_2 = Table.objects.create(location=restaurant, capacity=2)
        for i in range(instance.four_seats_tables):
            table_4 = Table.objects.create(location=restaurant, capacity=4)
        for i in range(instance.more_than_four_seats_tables):
            table_more = Table.objects.create(location=restaurant, capacity=6)
        print("Created restaurant and tables.")


@receiver(post_save, sender=CustomUser)
def save_restaurant_and_tables(sender, instance, **kwargs):
    # if instance.is_restaurant:
    instance.restaurant.save()
    for table in instance.restaurant.restaurant_tables.all():
        table.save()


