from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("name", "surname", "email", "is_restaurant", "restaurant_name",
                                                 "restaurant_address", "restaurant_type", "two_seats_tables",
                                                 "four_seats_tables", "more_than_four_seats_tables")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
