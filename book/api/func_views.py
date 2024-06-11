from django.shortcuts import render
from book.models import Book
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from book.api.serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def book_details(request, id):

    if request.method == 'GET':
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({'error':'Book is not found.'}, status=status.HTTP_404_NOT_FOUND)    
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        book = Book.objects.get(id=id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
