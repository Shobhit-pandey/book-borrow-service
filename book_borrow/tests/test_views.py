from datetime import timedelta, datetime

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from book_borrow.constant import BOOK_RETURN_DAYS
from book_borrow.functions import get_blocking_time_in_days
from book_borrow.models import BookingHistory
from book_borrow.tests.dummy_data import create_available_books, create_unavailable_books, create_users
from book_borrow.dataclasses import Book as BookDataClass


class AllBookFetchTestCase(TestCase):
    def setUp(self):
        self.available_books = create_available_books()
        self.unavailable_books = create_unavailable_books()

    def test_get_only_available_book(self):
        response = self.client.get(reverse('all-books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.available_books))

    def test_get_book_list_without_author_params(self):
        response = self.client.get(reverse('all-books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.available_books))

    def test_get_book_list_with_empty_string_author_params(self):
        response = self.client.get(reverse('all-books'), {"author": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.available_books))

    def test_get_book_list_with_invalid_author_params(self):
        response = self.client.get(reverse('all-books'), {"author": "hdjdashdkdhkasdhkhhahskjdh"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_book_list_with_valid_author_params(self):
        response = self.client.get(reverse('all-books'), {"author": self.available_books.first().author.name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class BorrowBookTestCase(TestCase):
    def setUp(self):
        self.available_books = create_available_books()
        self.unavailable_books = create_unavailable_books()
        self.user = create_users()

    def test_borrow_book_with_invalid_book_id(self):
        response = self.client.put(
            reverse('borrow-book', kwargs={"book_id": 999999999}),
            {"username": self.user.first().username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 404)

    def test_borrow_unavailable_book(self):
        book_id = self.available_books.first().id
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": self.user[0].username},
            content_type="application/json", )
        response = self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": self.user[1].username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'Book is not available'})

    def test_borrow_already_borrowed_before_locking_time(self):
        book_id = self.available_books.first().id
        username = self.user.first().username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        response = self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'Book is not available'})

    def test_borrow_already_borrowed_after_locking_time(self):
        book_id = self.available_books.first().id
        username = self.user.first().username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        current_time = timezone.now() - timedelta(days=1000)
        BookingHistory.objects.filter(book_id=book_id, user__username=username).update(return_time=current_time)
        response = self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Book issued'})

    def test_borrow_new_book(self):
        book_id = self.available_books.first().id
        username = self.user.first().username
        response = self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Book issued'})


class ReturnBookTestCase(TestCase):
    def setUp(self):
        self.available_books = create_available_books()
        self.unavailable_books = create_unavailable_books()
        self.user = create_users()

    def test_return_book_with_invalid_book_id(self):
        response = self.client.put(
            reverse('return-book', kwargs={"book_id": 999999999}),
            {"username": self.user.first().username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 404)

    def test_return_available_book(self):
        book_id = self.available_books.first().id
        response = self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": self.user[1].username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'This book is not issued to you'})

    def test_return_book_by_another_user(self):
        book_id = self.available_books.first().id
        issuer_username = self.user[0].username
        return_username = self.user[1].username

        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": issuer_username},
            content_type="application/json", )
        response = self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": return_username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'This book is not issued to you'})

    def test_return_book_by_same_user(self):
        book_id = self.available_books.first().id
        issuer_username = self.user[0].username
        return_username = self.user[0].username

        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": issuer_username},
            content_type="application/json", )
        response = self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": return_username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Book is returned'})


class NextBorrowTimeTestCase(TestCase):
    def setUp(self):
        self.available_books = create_available_books()
        self.unavailable_books = create_unavailable_books()
        self.user = create_users()

    def test_with_invalid_book_id(self):
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": 999999999}),
            {"username": self.user.first().username},
            content_type="application/json", )
        self.assertEqual(response.status_code, 404)

    def test_with_already_borrowed_by_another_user_and_user_never_borrowed(self):
        book_id = self.available_books.first().id
        borrowed_username = self.user[0].username
        another_user = self.user[1].username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": borrowed_username},
            content_type="application/json", )
        issue_time = BookingHistory.objects.filter(book_id=book_id, user__username=borrowed_username,
                                                   return_time=None).first().issue_time
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": book_id}),
            {"username": another_user},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unblock_time"], (issue_time + timedelta(days=BOOK_RETURN_DAYS)).strftime(
            "%d-%B-%Y, %H:%M:%S") + " " + settings.TIME_ZONE)

    def test_with_already_borrowed_by_another_user_and_user_also_borrowed_in_past(self):
        book = self.available_books.first()
        book_id = book.id
        borrowed_username = self.user[0].username
        self_user = self.user[1].username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": borrowed_username},
            content_type="application/json", )
        issue_time = BookingHistory.objects.filter(book_id=book_id, user__username=borrowed_username,
                                                   return_time=None).first().issue_time
        return_time_by_borrowed_user = issue_time + timedelta(days=BOOK_RETURN_DAYS)
        book_return_time_by_self_user = BookingHistory.objects.filter(
            book_id=book_id,
            user__username=self_user
        ).order_by('-return_time').first().return_time
        unblock_time = book_return_time_by_self_user + timedelta(
            days=get_blocking_time_in_days(BookDataClass.get_from_model_object(book))
        )
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unblock_time"], (max(return_time_by_borrowed_user, unblock_time)).strftime(
            "%d-%B-%Y, %H:%M:%S") + " " + settings.TIME_ZONE)

    def test_after_user_already_borrowed_book_and_not_returned(self):
        book = self.available_books.first()
        book_id = book.id
        self_user = self.user[0].username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        issue_time = BookingHistory.objects.filter(book_id=book_id, user__username=self_user,
                                                   return_time=None).first().issue_time
        return_time_by_self_user = issue_time + timedelta(days=BOOK_RETURN_DAYS)

        unblock_time = return_time_by_self_user + timedelta(
            days=get_blocking_time_in_days(BookDataClass.get_from_model_object(book))
        )
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unblock_time"], unblock_time.strftime(
            "%d-%B-%Y, %H:%M:%S") + " " + settings.TIME_ZONE)

    def test_book_available_and_user_never_borrowed_book(self):
        book = self.available_books.first()
        book_id = book.id
        self_user = self.user[0].username
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        actual_unblock_time = datetime.strptime(response.data["unblock_time"][:-4], "%d-%B-%Y, %H:%M:%S")
        expected_unblock_time = datetime.now()
        self.assertTrue(expected_unblock_time > actual_unblock_time)
        self.assertTrue((expected_unblock_time - actual_unblock_time).seconds < 120)

    def test_book_available_and_user_borrowed_book_in_past(self):
        book = self.available_books.first()
        book_id = book.id
        self_user = self.user[0].username
        self.client.put(
            reverse('borrow-book', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.client.put(
            reverse('return-book', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        return_time = BookingHistory.objects.filter(
            book_id=book_id, user__username=self_user).order_by('-return_time').first().return_time

        unblock_time = return_time + timedelta(
            days=get_blocking_time_in_days(BookDataClass.get_from_model_object(book))
        )
        response = self.client.get(
            reverse('next-borrow-time', kwargs={"book_id": book_id}),
            {"username": self_user},
            content_type="application/json", )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unblock_time"], unblock_time.strftime(
            "%d-%B-%Y, %H:%M:%S") + " " + settings.TIME_ZONE)