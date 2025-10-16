from rest_framework import serializers
from .models import Book, Customer, BorrowRecord, BookRequest


# ===============================
# 1️⃣ Customer Serializer
# ===============================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# ===============================
# 2️⃣ Book Serializer
# ===============================
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# ===============================
# 3️⃣ Borrow Record Serializer
# ===============================
class BorrowRecordSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = '__all__'


# ===============================
# 4️⃣ Book Request Serializer (NEW FEATURE 💡)
# ===============================
class BookRequestSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookRequest
        fields = '__all__'
