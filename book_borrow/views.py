from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from book_borrow.functions import book_availability_for_current_user
from book_borrow.models import Book, BookingHistory
from .data_entry import get_temporary_user
from .dataclasses import Book as BookDataClass, User as UserDataClass

# @login_required()
@api_view(['GET'])
def get_all_books(request):
    author = request.GET.get('author', "")
    filters = {"available": True}
    if author:
        filters["author__name__iexact"] = author
    all_books = Book.objects.filter(**filters).values("id", "name", "type", "author__name")
    for book in all_books:
        book["author"] = book.pop("author__name")
    return Response(all_books, status=status.HTTP_200_OK)


# @login_required()
@api_view(['PUT'])
def borrow_book(request, book_id):
    # user = request.user
    user = get_temporary_user()
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return Response(status.HTTP_404_NOT_FOUND)
    if not book.available:
        return Response({"message": "Book is not available"}, status.HTTP_400_BAD_REQUEST)
    is_blocked_for_current_user = book_availability_for_current_user(
        BookDataClass.get_from_model_object(book),
        UserDataClass.get_from_model_object(user),
    )
    if is_blocked_for_current_user.blocked:
        return Response({"message": "Its seems you booked same book in near past. You can book this book after" +
                                    str(is_blocked_for_current_user.unblock_time)}, status.HTTP_400_BAD_REQUEST)
    book.available = False
    book.save()
    BookingHistory.objects.create(book=book, user=user)
    return Response({"message": "Book issued"}, status=status.HTTP_200_OK)


# @login_required()
@api_view(['PUT'])
def return_book(request, book_id):
    # user = request.user
    user = get_temporary_user()
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return Response(status.HTTP_404_NOT_FOUND)
    if book.available:
        return Response({"message": "This book is not issued to you"}, status.HTTP_400_BAD_REQUEST)
    booking_history = BookingHistory.objects.filter(book_id=book_id, user=user, return_time=None).first()
    if not booking_history:
        return Response({"message": "This book is not issued to you"}, status.HTTP_400_BAD_REQUEST)
    book.available = True
    book.save()
    booking_history.return_time = timezone.now()
    booking_history.save()
    return Response({"message": "Book is returned"}, status.HTTP_200_OK)


# @login_required()
@api_view(['GET'])
def next_borrow_time(request, book_id):
    # user = request.user
    user = get_temporary_user()
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return Response(status.HTTP_404_NOT_FOUND)
    if not book.available:
        return Response({"message": "This book is not available for issue"}, status.HTTP_400_BAD_REQUEST)
    is_blocked_for_current_user = book_availability_for_current_user(
        BookDataClass.get_from_model_object(book),
        UserDataClass.get_from_model_object(user),
    )
    return Response(is_blocked_for_current_user, status=status.HTTP_200_OK)