from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from book.models import Book, Category, Review
from book.api.serializers import BookSerializer, CategorySerializer, ReviewSerializer, ReviewSerializerWithoutBook
from book.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]



class BookReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(book=pk)


class BookReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializerWithoutBook
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        book = Book.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(book=book, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this book!")

        if book.number_rating == 0:
            book.avg_rating = serializer.validated_data['rating']
        else:
            prev_total_rating = book.number_rating
            total_rating = (book.avg_rating * book.number_rating) + serializer.validated_data['rating']
            book.avg_rating = total_rating / (prev_total_rating + 1)
        book.number_rating = book.number_rating + 1
        book.save()
        serializer.save(book=book, review_user=review_user)


# class ReviewDetail(mixins.RetrieveModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class CategoryAV(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookVS(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


# class BookVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Book.objects.all()
#         serializer = BookSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Book.objects.all()
#         book = get_object_or_404(queryset, pk=pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book is not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = Book.objects.get(id=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def book_list(request):
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def book_details(request, id):

#     if request.method == 'GET':
#         try:
#             book = Book.objects.get(id=id)
#         except Book.DoesNotExist:
#             return Response({'error':'Book is not found.'}, status=status.HTTP_404_NOT_FOUND)    
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         book = Book.objects.get(id=id)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         book = Book.objects.get(id=id)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
