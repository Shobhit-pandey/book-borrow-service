from datetime import timedelta
from django.utils import timezone

from book_borrow.constant import BOOK_RETURN_DAYS
from book_borrow.dataclasses import BlockStatus, Book, User, BookNextAvailability
from book_borrow.models import BookingHistory


def get_blocking_time_in_days(book: Book) -> int:
    if book.author.lower().startswith("J"):
        return 180
    return 90


def book_availability_for_current_user(book: Book, user: User) -> BlockStatus:
    current_time = timezone.now()
    block_status = BlockStatus(blocked=False, unblock_time=current_time)
    last_booking = BookingHistory.objects.filter(book_id=book.id, user_id=user.id).order_by('-issue_time').first()
    if not last_booking:
        return block_status
    if last_booking.return_time:
        last_return_time = last_booking.return_time
    else:
        last_return_time = last_booking.issue_time + timedelta(days=BOOK_RETURN_DAYS)
    unblock_period_in_days = get_blocking_time_in_days(book)
    unblock_time = last_return_time + timedelta(days=unblock_period_in_days)
    block_status.unblock_time = unblock_time if unblock_time > current_time else current_time
    block_status.blocked = unblock_time > current_time
    return block_status


def book_next_availability(book: Book) -> BookNextAvailability:
    last_booking = BookingHistory.objects.filter(book_id=book.id).order_by('-issue_time').first()
    current_time = timezone.now()
    if last_booking and not last_booking.return_time:
        return BookNextAvailability(
            name=book.name,
            current_booked_by=last_booking.user.username,
            available_at=last_booking.issue_time + timedelta(days=BOOK_RETURN_DAYS)
        )
    return BookNextAvailability(
        name=book.name,
        current_booked_by=last_booking.user.username if last_booking else None,
        available_at=current_time
    )