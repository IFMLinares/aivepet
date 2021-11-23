from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Transaction, Winerie, Destination, Product, NominalTransaccion

# Register your models here.

admin.site.register(Transaction,SimpleHistoryAdmin)
admin.site.register(Winerie)
admin.site.register(Destination)
admin.site.register(Product)
admin.site.register(NominalTransaccion,SimpleHistoryAdmin)
