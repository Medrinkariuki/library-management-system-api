from rest_framework import serializers
from .models import Book, Customer, BorrowRecord, BookRequest


# ===============================
# 📚 BOOK SERIALIZER
# ===============================
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# ===============================
# 👤 CUSTOMER SERIALIZER
# ===============================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# ===============================
# 🔄 BORROW RECORD SERIALIZER
# ===============================
class BorrowRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRecord
        fields = [
            'id',
            'book',
            'book_title',
            'customer',
            'customer_name',
            'checkout_date',
            'due_date',
            'return_date',
            'is_overdue',
        ]

    def get_is_overdue(self, obj):
        return obj.is_overdue()


# ===============================
# 📝 BOOK REQUEST SERIALIZER
# ===============================
class BookRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = BookRequest
        fields = [
            'id',
            'customer',
            'customer_name',
            'title',
            'author',
            'fee',
            'request_date',
        ]
