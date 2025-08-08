from .models import User
from django.urls import path
from .views import UserCSVUploadView,UserListView

urlpatterns = [
    path('process-csv/',UserCSVUploadView.as_view(), name='process-csv'),
    path('users_list/',UserListView.as_view(), name='users_list'),
]

