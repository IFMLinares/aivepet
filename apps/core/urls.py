from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dev', Developing.as_view(), name='dev'),
    path('list_users', ListUser.as_view(), name='list_user'),
    path('delete_users/<int:pk>', UserDeleteView.as_view(), name='delete_user'),
    path('user_detail/<int:pk>', UserView.as_view(), name='user_detail'),
    path('user_edit/<int:pk>', UserEdit.as_view(), name='user_edit'),
]