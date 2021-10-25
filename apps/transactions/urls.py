from django.urls import path, include
from .views import *
app_name = 'transactions'

urlpatterns = [
    path('in-load', OrderListLoad.as_view(), name='order_list_load'),
    path('in-download', OrderListDownload.as_view(), name='order_list_download'),
    path('add', AddOrder.as_view(), name='add_order'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update_order'),
    path('add-wineries', WineriesAdd.as_view(), name='add_wineries'),
    path('add-product', ProductAdd.as_view(), name='add_product'),
    path('add-destinations', DestinationAdd.as_view(), name='add_destinations'),
    path('add-reciving-customers', ReceivingCustomerAdd.as_view(), name='add_reciving_customers'),
]