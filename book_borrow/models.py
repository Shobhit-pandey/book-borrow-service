from django.db import models
from django.contrib.auth.models import User

BOOK_TYPES = (
    ('Paperbacks', 'Paperbacks'),
    ('Hardcover', 'Hardcover'),
    ('Handmade', 'Handmade')
)


class Author(models.Model):
    auther_name = models.CharField(max_length=255, blank=False)


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=BOOK_TYPES, blank=False)


class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True)