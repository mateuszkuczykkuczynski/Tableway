from django.contrib import admin

from payments.models import Payment, Tip

admin.site.register(Payment)
admin.site.register(Tip)
