from datetime import timedelta
from django.db import models
from django.utils import timezone


# ===============================
# 📚 BOOK MODEL
# ===============================
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# ===============================
# 👤 CUSTOMER MODEL
# ===============================
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ===============================
# 🔄 BORROW RECORD MODEL
# ===============================
class BorrowRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now().date() + timedelta(days=14))
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        """
        Returns True if the book is not returned and today is past the due date.
        """
        return self.return_date is None and timezone.now().date() > self.due_date

    def __str__(self):
        return f"{self.customer.name} borrowed {self.book.title}"


# ===============================
# 📝 BOOK REQUEST MODEL
# ===============================
class BookRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} requested by {self.customer.name}"
