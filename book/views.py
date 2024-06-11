from django.shortcuts import render
from .models import Book
from django.http import JsonResponse, HttpResponse

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    print(books)
    print(books.values())
    books_list = list(books.values())
    print(books_list)
    return JsonResponse({"Books : " : books_list})

