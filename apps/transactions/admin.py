from django.contrib import admin

from .models import Transaction, Winerie, Destination, Product, NominalTransaccion

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Winerie)
admin.site.register(Destination)
admin.site.register(Product)
admin.site.register(NominalTransaccion)
