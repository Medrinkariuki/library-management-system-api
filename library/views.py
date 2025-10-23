from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Book, Customer, BorrowRecord, BookRequest
from .serializers import BookSerializer, CustomerSerializer, BorrowRecordSerializer, BookRequestSerializer


# ---------------- BOOKS ----------------
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ---------------- CUSTOMERS ----------------
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ---------------- BORROW BOOK ----------------
class BorrowBookView(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        book_id = request.data.get("book_id")

        if not customer_id or not book_id:
            return Response({"error": "Both 'customer_id' and 'book_id' are required."}, status=400)

        try:
            customer = Customer.objects.get(id=customer_id)
            book = Book.objects.get(id=book_id)
        except (Customer.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "Invalid customer or book ID."}, status=404)

        if book.copies_available < 1:
            return Response({"error": "No copies available for this book."}, status=400)

        BorrowRecord.objects.create(customer=customer, book=book, borrow_date=timezone.now())
        book.copies_available -= 1
        book.save()

        return Response({"message": f"{book.title} borrowed successfully by {customer.name}."}, status=201)


# ---------------- RETURN BOOK ----------------
class ReturnBookView(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        book_id = request.data.get("book_id")

        if not customer_id or not book_id:
            return Response({"error": "Both 'customer_id' and 'book_id' are required."}, status=400)

        borrow_record = BorrowRecord.objects.filter(
            book__id=book_id,
            customer__id=customer_id,
            return_date__isnull=True
        ).first()

        if not borrow_record:
            return Response({"error": "No active borrow record found for this book and customer."}, status=404)

        borrow_record.return_date = timezone.now()
        borrow_record.save()

        borrow_record.book.copies_available += 1
        borrow_record.book.save()

        return Response({"message": "Book returned successfully."}, status=200)


# ---------------- BOOK REQUEST ----------------
class BookRequestListCreateView(APIView):
    def get(self, request):
        return Response(
            {"message": "Book request feature is temporarily unavailable."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def post(self, request):
        return Response(
            {"message": "Book request feature is temporarily unavailable."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )



# ---------------- BORROW RECORDS LIST ----------------
class BorrowRecordListView(generics.ListAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
