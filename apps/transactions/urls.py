from django.urls import path, include
from .views import *
app_name = 'transactions'

urlpatterns = [

    # URL PARA LAS VISTAS DE TRANSACCIONES
    path('add-transaction', AddOrder.as_view(), name='add_order'),
    path('in-load', OrderListLoad.as_view(), name='order_list_load'),
    path('in-download', OrderListDownload.as_view(), name='order_list_download'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update_order'),
    path('add-wineries', WineriesAdd.as_view(), name='add_wineries'),
    path('add-product', ProductAdd.as_view(), name='add_product'),
    path('add-destinations', DestinationAdd.as_view(), name='add_destinations'),
    path('add-reciving-customers', ReceivingCustomerAdd.as_view(), name='add_reciving_customers'),
    path('product-list', OrderListProducts.as_view(), name='product_list'),
    path('customers-list', OrderListCustomers.as_view(), name='customers_list'),
    path('add-transport', TransportAdd.as_view(), name='add_transport'),

    #URL PARA LAS VISTAS DE BARCOS NOMINADOS (NOMINAL TRANSACCIONS)
    path('add-nominal', AddOrderNominal.as_view(), name='add_order_nominal'),
    path('list_nominal', NominalList.as_view(), name='order_list_nominal'),
    path('delete_nominal/<int:pk>', NominalTransactionDelete.as_view(), name='delete_nominal_trans'),
    path('acepted_nominal/<int:pk>', NominalTransAcepted, name='acepted_nominal_trans'),
    path('detail_nominal/<int:pk>', NominalTransactionDetail.as_view(), name='detail_nominal'),
]