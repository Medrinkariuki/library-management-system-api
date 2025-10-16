from django.db import models
from django.contrib.auth.models import User

# ===============================
# 1️⃣ Customer Model
# ===============================
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===============================
# 2️⃣ Book Model
# ===============================
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"


# ===============================
# 3️⃣ Borrow Record Model
# ===============================
class BorrowRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name} borrowed {self.book.title}"


# ===============================
# 4️⃣ Book Request Model (NEW FEATURE 💡)
# ===============================
class BookRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    requested_title = models.CharField(max_length=200)
    requested_author = models.CharField(max_length=100, blank=True, null=True)
    date_requested = models.DateField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)
    extra_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.customer.name} requested {self.requested_title}"
