from django.urls import path, include
from .views import *
app_name = 'transactions'

urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('add', AddOrder.as_view(), name='add_order'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update_order'),
]