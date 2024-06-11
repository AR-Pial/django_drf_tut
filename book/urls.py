from django.urls import path
from .views import *

urlpatterns = [
    path('', book_list, name="book_list")
]