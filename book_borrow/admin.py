from django.contrib.admin import site

from book_borrow.models import Book, Author, BookingHistory

site.register(Book)
site.register(Author)
site.register(BookingHistory)