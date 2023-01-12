"""book_borrow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from book_borrow import views

urlpatterns = {
    path('admin/', admin.site.urls),
    path('all-books/', views.get_all_books, name='all-books'),
    path('borrow-book/<int:book_id>/', views.borrow_book, name='borrow-book'),
    path('return-book/<int:book_id>', views.return_book, name='return-books'),
    path('next-borrow-time/<int:book_id>', views.next_borrow_time, name='next-borrow-time'),
}