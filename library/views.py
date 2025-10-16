from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Customer, BorrowRecord, BookRequest
from .serializers import (
    BookSerializer,
    CustomerSerializer,
    BorrowRecordSerializer,
    BookRequestSerializer
)

# ===============================
# 📚 BOOK VIEWS
# ===============================
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookSearchView(generics.ListAPIView):
    """
    Search books by title or author.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author']


# ===============================
# 👤 CUSTOMER VIEWS
# ===============================
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ===============================
# 🔄 BORROW & RETURN VIEWS
# ===============================
class BorrowBookView(APIView):
    """
    Allows a customer to borrow a book if copies are available.
    """
    def post(self, request):
        book_id = request.data.get("book_id")
        customer_id = request.data.get("customer_id")

        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except (Book.DoesNotExist, Customer.DoesNotExist):
            return Response({"error": "Book or Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available < 1:
            return Response({"error": "No copies available for this book."}, status=status.HTTP_400_BAD_REQUEST)

        if BorrowRecord.objects.filter(customer=customer, book=book, return_date__isnull=True).exists():
            return Response({"error": "This customer already borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        BorrowRecord.objects.create(book=book, customer=customer)
        book.copies_available -= 1
        book.save()

        return Response({"message": f"{customer.name} borrowed '{book.title}' successfully!"}, status=status.HTTP_201_CREATED)


class ReturnBookView(APIView):
    """
    Allows a customer to return a borrowed book.
    Updates the borrow record with the actual return date and
    increases the book's available copies.
    """
    def post(self, request):
        book_id = request.data.get("book_id")
        customer_id = request.data.get("customer_id")

        try:
            customer = Customer.objects.get(id=customer_id)
            book = Book.objects.get(id=book_id)
        except (Customer.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "Book or Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            record = BorrowRecord.objects.get(book=book, customer=customer, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({"error": "No active borrow record found for this book and customer."}, status=status.HTTP_404_NOT_FOUND)

        record.return_date = timezone.now()
        record.save()

        book.copies_available += 1
        book.save()

        return Response({"message": f"{customer.name} returned '{book.title}' successfully!"}, status=status.HTTP_200_OK)


# ===============================
# 📄 BORROW RECORD VIEWS
# ===============================
class BorrowRecordListView(generics.ListAPIView):
    """
    List all borrow records.
    """
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer


class CustomerBorrowedBooksView(generics.ListAPIView):
    """
    List all books currently borrowed by a specific customer.
    """
    serializer_class = BorrowRecordSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return BorrowRecord.objects.filter(customer_id=customer_id, return_date__isnull=True)


class OverdueBooksView(generics.ListAPIView):
    """
    List all borrow records that are overdue.
    """
    serializer_class = BorrowRecordSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return BorrowRecord.objects.filter(return_date__isnull=True, due_date__lt=today)


# ===============================
# 📖 BOOK REQUEST VIEWS
# ===============================
class BookRequestListCreateView(generics.ListCreateAPIView):
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
            {"message": f"Book request for '{new_request.title}' has been created. We’ll notify you once it’s available."},
            status=status.HTTP_201_CREATED
        )


class BookRequestListView(generics.ListAPIView):
    """
    List all book requests.
    """
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
