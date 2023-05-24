from django.contrib import admin
from bookings.models import Restaurant, Reservation, Table, Employee


# class TableInline(admin.TabularInline):
#     model = Table
#
#
# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     inlines = [TableInline]

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Employee)