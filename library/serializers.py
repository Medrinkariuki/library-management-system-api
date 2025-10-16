from rest_framework import serializers
from .models import Book,LibraryUser

# Converts Book model data into JSON format for API responses
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'