from django.urls import path
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDeleteView,
    CustomerListCreateView,
    CustomerRetrieveUpdateDeleteView,
    BorrowBookView,
    ReturnBookView,
    BorrowRecordListView,
    BookRequestListCreateView,
    BookRequestListView
)

urlpatterns = [
    # ===============================
    # 📚 BOOK URLS
    # ===============================
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),

    # ===============================
    # 👤 CUSTOMER URLS
    # ===============================
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDeleteView.as_view(), name='customer-detail'),

    # ===============================
    # 🔄 BORROW & RETURN URLS
    # ===============================
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('borrow-records/', BorrowRecordListView.as_view(), name='borrow-records'),

    # ===============================
    # 📖 BOOK REQUEST URLS
    # ===============================
    path('book-requests/', BookRequestListCreateView.as_view(), name='book-request-create'),
    path('book-requests/list/', BookRequestListView.as_view(), name='book-request-list'),
]
