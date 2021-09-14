from django.urls import path, include
from .views import *
app_name = 'transactions'

urlpatterns = [
    path('', AddOrder.as_view(), name='add_order'),
]