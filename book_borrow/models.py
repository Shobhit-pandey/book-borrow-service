from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    auther_name = models.CharField(max_length=255, blank=False)


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)


class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    book_return_time = models.DateTimeField(null=True)