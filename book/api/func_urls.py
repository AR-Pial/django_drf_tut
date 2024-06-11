from django.urls import path
from book.api.func_views import *

urlpatterns = [
    path('books/', book_list, name="book_list"),
	path('books/<int:id>/', book_details, name="book_details")
]