from rest_framework import generics
from .models import Book, LibraryUser
from .serializers import BookSerializer, LibraryUserSerializer


# ==============================
# 📚 BOOK VIEWS
# ==============================
class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET: List all books
    - POST: Add a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET: Retrieve a single book by ID
    - PUT: Update book details
    - DELETE: Remove a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ==============================
# 👤 LIBRARY USER VIEWS
# ==============================
class LibraryUserListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET: List all library users
    - POST: Add a new user
    """
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer


class LibraryUserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET: Retrieve one user
    - PUT: Update user info
    - DELETE: Remove a user
    """
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer
