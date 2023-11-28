from django.contrib import admin
from bookings.models import Restaurant, Reservation, Table, Employee


class TableInline(admin.TabularInline):
    """Inline representation of Table model for the admin interface."""
    model = Table


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Admin representation for the Restaurant model with associated tables."""
    inlines = [TableInline]


# Rest of models will also be displayed better, maybe jazzmin will be used for admin panel creation
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Employee)
