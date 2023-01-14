import random
from book_borrow.constant import BOOK_TYPE
from book_borrow.models import Author, Book

available_book_data = [
    {'author': 'Chinua Achebe', 'name': 'Things Fall Apart'},
    {'author': 'Hans Christian Andersen', 'name': 'Fairy tales'},
    {'author': 'Dante Alighieri', 'name': 'The Divine Comedy'},
    {'author': 'Unknown', 'name': 'The Epic Of Gilgamesh'},
    {'author': 'Unknown', 'name': 'The Book Of Job'}
]

unavailable_book_data = [
    {'author': 'Unknown', 'name': 'One Thousand and One Nights'},
    {'author': 'Unknown', 'name': "Njál's Saga"},
    {'author': 'Jane Austen', 'name': 'Pride and Prejudice'},
    {'author': 'Samuel Beckett', 'name': 'Molloy, Malone Dies, The Unnamable, the trilogy'},
]

user_data = ['Aaberg', 'Aara', 'Aalst', 'Aaren', 'Aarika', 'Aaron', 'Aaronson', 'Ab']


def create_users():
    from django.contrib.auth.models import User
    for user_name in user_data:
        user = User.objects.create(username=user_name)
        user.set_password(user_name + "@123")
        user.save()
    return User.objects.all()


def create_available_books():
    for book in available_book_data:
        author = Author.objects.create(name=book['author'])
        random_type = random.randint(0, 2)
        Book.objects.create(author=author, name=book['name'], type=BOOK_TYPE[random_type])
    return Book.objects.filter(available=True)


def create_unavailable_books():
    for book in unavailable_book_data:
        author = Author.objects.create(name=book['author'])
        random_type = random.randint(0, 2)
        Book.objects.create(author=author, name=book['name'], type=BOOK_TYPE[random_type], available=False)
    return Book.objects.filter(available=False)