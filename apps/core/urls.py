from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dev', Developing.as_view(), name='dev'),
]