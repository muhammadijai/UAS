from django.urls import path
from .views import * # Memanggil semua fungsi yang ada di dalam file views.py

urlpatterns = [
    path('', list_users,name='list_users'),
]