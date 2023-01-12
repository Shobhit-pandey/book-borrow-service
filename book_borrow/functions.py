from datetime import timedelta

from django.utils import timezone

from book_borrow.dataclasses import BlockStatus, Book, User
from book_borrow.models import BookingHistory


def get_blocking_time_in_days(book: Book) -> int:
    if book.author.lower().startswith("J"):
        return 180
    return 90


def book_availability_for_current_user(book: Book, user: User) -> BlockStatus:
    block_status = BlockStatus(blocked=True, unblock_time="")
    last_booking = BookingHistory.objects.filter(book_id=book.id, user_id=user.id).order_by('-return_time').first()
    if not last_booking:
        block_status.blocked = False
        block_status.unblock_time = None
        return block_status
    last_return_time = last_booking.return_time
    unblock_period_in_days = get_blocking_time_in_days(book)
    unblock_time = last_return_time + timedelta(days=unblock_period_in_days)
    current_time = timezone.now()
    block_status.unblock_time = unblock_time
    block_status.blocked = unblock_time <= current_time
    return block_status