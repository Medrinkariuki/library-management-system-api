from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Book, Customer, BorrowRecord, BookRequest
from .serializers import (
    BookSerializer,
    CustomerSerializer,
    BorrowRecordSerializer,
    BookRequestSerializer,
)

# ===============================
# 📚 BOOK VIEWS
# ===============================
class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or add a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'title']


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View, update, or delete a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ===============================
# 👤 CUSTOMER VIEWS
# ===============================
class CustomerListCreateView(generics.ListCreateAPIView):
    """
    List all customers or create a new one.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific customer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ===============================
# 🔄 BORROW & RETURN VIEWS
# ===============================
class BorrowBookView(APIView):
    """
    Allows a customer to borrow a book if it's available.
    """
    def post(self, request):
        book_id = request.data.get("book_id")
        customer_id = request.data.get("customer_id")

        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except (Book.DoesNotExist, Customer.DoesNotExist):
            return Response({"error": "Book or Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if available
        if book.copies_available < 1:
            return Response({"error": "No copies available for this book."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already borrowed
        if BorrowRecord.objects.filter(customer=customer, book=book, return_date__isnull=True).exists():
            return Response({"error": "This customer already borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        # Borrow the book
        BorrowRecord.objects.create(customer=customer, book=book)
        book.copies_available -= 1
        book.save()

        return Response(
            {"message": f"{customer.name} borrowed '{book.title}' successfully!"},
            status=status.HTTP_201_CREATED
        )


class ReturnBookView(APIView):
    """
    Allows a customer to return a borrowed book.
    """
    def post(self, request):
        book_id = request.data.get("book_id")
        customer_id = request.data.get("customer_id")

        try:
            record = BorrowRecord.objects.get(book_id=book_id, customer_id=customer_id, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "No active borrow record found for this book and customer."},
                            status=status.HTTP_404_NOT_FOUND)

        # Return the book
        record.return_date = timezone.now().date()
        record.save()

        book = record.book
        book.copies_available += 1
        book.save()

        return Response(
            {"message": f"{record.customer.name} returned '{record.book.title}' successfully!"},
            status=status.HTTP_200_OK
        )


class BorrowRecordListView(generics.ListAPIView):
    """
    View all borrow records (past and present).
    """
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'book', 'return_date']


# ===============================
# 📝 BOOK REQUEST VIEWS
# ===============================
class BookRequestListCreateView(generics.ListCreateAPIView):
    """
    List all book requests or create a new one.
    """
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            customer = Customer.objects.get(id=data.get("customer_id"))
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        new_request = BookRequest.objects.create(
            customer=customer,
            title=data.get("title"),
            author=data.get("author"),
            fee=data.get("fee", 0.00)
        )
        return Response(
            {"message": f"Book request for '{new_request.title}' has been created. "
                        f"We’ll notify {customer.name} once it’s available."},
            status=status.HTTP_201_CREATED
        )
