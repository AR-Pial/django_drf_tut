from django.urls import path, include
from book.api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', BookVS, basename='book')

urlpatterns = [
    # path('', BookListAV.as_view(), name="book_list"),
    # path('<int:pk>/', BookDetailAV.as_view(), name="book_detail"),
    path('', include(router.urls)),
    path('categories/', CategoryAV.as_view(), name="category_list"),

    path('reviews/', ReviewList.as_view(), name="review_list"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review_detail"),
    path('<int:pk>/review-create/', BookReviewCreate.as_view(), name="review_list"),
    path('<int:pk>/review/', BookReviewList.as_view(), name="review_list"),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name="review_detail"),
]
