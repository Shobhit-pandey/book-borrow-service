from django.db import models
from django.contrib.auth.models import User

from book_borrow.constant import BOOK_TYPE

BOOK_TYPES = (
    (book_type, book_type) for book_type in BOOK_TYPE
)


class Author(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=BOOK_TYPES, blank=False)

    def __str__(self):
        return self.name


class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.book.name + " (" + self.user.username +")"