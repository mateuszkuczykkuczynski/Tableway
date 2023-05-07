from django.contrib import admin
from reservations.models import Restaurant, Table


# class TableInline(admin.TabularInline):
#     model = Table
#
#
# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     inlines = [TableInline]

admin.site.register(Restaurant)
admin.site.register(Table)




