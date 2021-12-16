from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Transaction, Winerie, Destination, Product, NominalTransaccion, Transport, ReceivingCustomer,Weight, ProductWeight

# Register your models here.

admin.site.register(Transaction,SimpleHistoryAdmin)
admin.site.register(Winerie)
admin.site.register(Transport)
admin.site.register(Destination)
admin.site.register(Product)
admin.site.register(ReceivingCustomer)
admin.site.register(Weight)
admin.site.register(ProductWeight)
admin.site.register(NominalTransaccion,SimpleHistoryAdmin)
