from django.urls import path
from .views import (
    BookListCreateView,
    CustomerListCreateView,
    BorrowBookView,
    ReturnBookView,
    BookRequestListCreateView,
    BorrowRecordListView,
)

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("customers/", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("borrow/", BorrowBookView.as_view(), name="borrow-book"),
    path("return/", ReturnBookView.as_view(), name="return-book"),
    path("bookrequest/", BookRequestListCreateView.as_view(), name="book-request-list-create"),
    path("borrowrecords/", BorrowRecordListView.as_view(), name="borrow-records"),
]
