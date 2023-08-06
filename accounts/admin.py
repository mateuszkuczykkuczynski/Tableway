from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin extends the default UserAdmin to handle the administration of the CustomUser model in the Django
    admin interface.

    It uses the CustomUserCreationForm and CustomUserChangeForm for creating and updating CustomUser instances,
    respectively.

    The list_display attribute defines the fields that will be displayed in the user list in the admin interface.

    The fieldsets and add_fieldsets attributes define the layout of the change and add forms in the admin interface.
    They include the default User fields as well as the additional fields defined in the CustomUser model.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "id",
        "email",
        "username",
        "is_staff",
        "name",
        "surname",
        "is_restaurant",
        "restaurant_name",
        "restaurant_address",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", "surname", "is_restaurant",
                                                          "restaurant_name", "restaurant_address",
                                                          "restaurant_type", "two_seats_tables",
                                                          "four_seats_tables", "more_than_four_seats_tables")}),
                                       )
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name", "surname", "is_restaurant",
                                                                  "restaurant_name", "restaurant_address",
                                                                  "restaurant_type", "two_seats_tables",
                                                                  "four_seats_tables",
                                                                  "more_than_four_seats_tables")}),
                                               )


admin.site.register(CustomUser, CustomUserAdmin)
