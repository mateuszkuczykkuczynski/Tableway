from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm extends the default UserCreationForm to handle the creation of new CustomUser instances.

    It includes the default User fields as well as the additional fields defined in the CustomUser model.
    """
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("name", "surname", "email", "is_restaurant", "restaurant_name",
                                                 "restaurant_country", "restaurant_city", "restaurant_address",
                                                 "restaurant_type", "two_seats_tables",
                                                 "four_seats_tables", "more_than_four_seats_tables")


class CustomUserChangeForm(UserChangeForm):
    """
    CustomUserChangeForm extends the default UserChangeForm to handle the updating of existing CustomUser instances.

    It includes all the fields defined in the CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
