from django.contrib import admin
from django.urls import path

from book_borrow import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all-books/', views.get_all_books, name='all-books'),
    path('borrow-book/<int:book_id>/', views.borrow_book, name='borrow-book'),
    path('return-book/<int:book_id>/', views.return_book, name='return-books'),
    path('next-borrow-time/<int:book_id>/', views.next_borrow_time, name='next-borrow-time'),
]