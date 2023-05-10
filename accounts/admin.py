from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = [
#         "email",
#         "username",
#         "is_staff",
#         "name",
#         "surname",
#         "is_restaurant",
#         "restaurant_name",
#         "restaurant_address",
#     ]
#     fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", "surname", "is_restaurant",
#                                                           "restaurant_name", "restaurant_address",
#                                                           "restaurant_type", "two_seats_tables",
#                                                           "four_seats_tables", "more_than_four_seats_tables")}),
#                                        )
#     add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name", "surname", "is_restaurant",
#                                                                   "restaurant_name", "restaurant_address",
#                                                                   "restaurant_type", "two_seats_tables",
#                                                                   "four_seats_tables",
#                                                                   "more_than_four_seats_tables")}),
#                                                )


# admin.site.register(CustomUser, CustomUserAdmin)

class CustomUserAdmin(admin.ModelAdmin):
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


admin.site.register(CustomUser, CustomUserAdmin)
