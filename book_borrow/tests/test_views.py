from django.test import TestCase


class AllBookFetchTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_only_available_book(self):
        pass

    def test_get_book_list_without_author_params(self):
        pass

    def test_get_book_list_with_empty_string_author_params(self):
        pass

    def test_get_book_list_with_invalid_author_params(self):
        pass

    def test_get_book_list_with_valid_author_params(self):
        pass


class BorrowBookTestCase(TestCase):
    def setUp(self):
        pass

    def test_borrow_book_with_invalid_book_id(self):
        pass

    def test_borrow_unavailable_book(self):
        pass

    def test_borrow_already_borrowed_before_locking_time(self):
        pass

    def test_borrow_already_borrowed_after_locking_time(self):
        pass

    def test_borrow_new_book(self):
        pass


class ReturnBookTestCase(TestCase):
    def setUp(self):
        pass

    def test_return_book_with_invalid_book_id(self):
        pass

    def test_return_available_book(self):
        pass

    def test_return_book_by_another_user(self):
        pass

    def test_return_book_by_same_user(self):
        pass


class NextBorrowTimeTestCase(TestCase):
    def setUp(self):
        pass

    def test_with_invalid_book_id(self):
        pass

    def test_with_already_borrowed_by_another_user_and_user_never_borrowed(self):
        pass

    def test_with_already_borrowed_by_another_user_and_user_also_borrowed_in_past(self):
        pass

    def test_after_user_already_borrowed_book_and_not_returned(self):
        pass

    def test_book_available_and_user_never_borrowed_book(self):
        pass

    def test_book_available_and_user_borrowed_book_in_past(self):
        pass