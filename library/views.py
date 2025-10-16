from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
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
    def post(self, request):
        book_id = request.data.get("book_id")
        customer_id = request.data.get("customer_id")

        try:
            record = BorrowRecord.objects.get(
                book_id=book_id, 
                customer_id=customer_id, 
                return_date__isnull=True
            )
        except BorrowRecord.DoesNotExist:
            return Response({"error": "No active borrow record found for this book and customer."}, status=status.HTTP_404_NOT_FOUND)

        record.return_date = record.borrow_date  # or timezone.now()
        record.save()

        book = record.book
        book.copies_available += 1
        book.save()

        return Response({"message": f"{record.customer.name} returned '{book.title}' successfully!"}, status=status.HTTP_200_OK)


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


# ===============================
# 📄 BORROW RECORD VIEWS
# ===============================
class BorrowRecordListView(generics.ListAPIView):
    """
    List all borrow records, including which customer borrowed which book.
    """
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer


# ===============================
# 📄 BOOK REQUEST LIST VIEW
# ===============================
class BookRequestListView(generics.ListAPIView):
    """
    List all book requests.
    """
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
