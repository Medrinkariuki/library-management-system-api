from django.urls import path
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDeleteView,
    LibraryUserListCreateView,
    LibraryUserRetrieveUpdateDeleteView
)

urlpatterns = [
    # ==============================
    # 📚 BOOK ENDPOINTS
    # ==============================
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),

    # ==============================
    # 👤 LIBRARY USER ENDPOINTS
    # ==============================
    path('users/', LibraryUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', LibraryUserRetrieveUpdateDeleteView.as_view(), name='user-detail'),
]
