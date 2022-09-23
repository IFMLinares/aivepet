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
    path('dekete-wineries', WineriesDelete.as_view(), name='delte_wineries'),
    path('add-product', ProductAdd.as_view(), name='add_product'),
    path('add-destinations', DestinationAdd.as_view(), name='add_destinations'),
    path('add-reciving-customers', ReceivingCustomerAdd.as_view(), name='add_reciving_customers'),
    path('product-list', OrderListProducts.as_view(), name='product_list'),
    path('customers-list', OrderListCustomers.as_view(), name='customers_list'),
    path('add-transport', TransportAdd.as_view(), name='add_transport'),
    path('get-act', GetAct.as_view(), name='get_act'),
    path('client_transaction/<int:pk>', UserViewTransaction.as_view(), name='client_view'),
    path('finish_transaction/<int:pk>', FinishTransaction, name='finish_trans'),
    path('status_add/', StatusAdd.as_view(), name='status_add'),
    path('multiple_bl/', MultipleBLAdd.as_view(), name='multiple_bl'),
    path('pdf/<int:pk>', PDFView.as_view(), name='pdf_view'),
    path('pdf_tracks/<int:pk>', PDFView1.as_view(), name='pdf_view1'),
    path('transaccion_success', TranssaccionSuccess.as_view(), name='transaction_success'),
    # path('add-weight', RecordWeightAdd.as_view(), name='add_weight'),

    #URL PARA LAS VISTAS DE BARCOS NOMINADOS (NOMINAL TRANSACCIONS)
    path('add-nominal', AddOrderNominal.as_view(), name='add_order_nominal'),
    path('list_nominal', NominalList.as_view(), name='order_list_nominal'),
    path('delete_nominal/<int:pk>', NominalTransactionDelete.as_view(), name='delete_nominal_trans'),
    path('acepted_nominal/<int:pk>', NominalTransAcepted, name='acepted_nominal_trans'),
    path('detail_nominal/<int:pk>', NominalTransactionDetail.as_view(), name='detail_nominal'),
]