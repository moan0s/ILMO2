from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /books/
    path('books/', views.index, name='index'),
    # ex: /library/books/5/
    path('books/<int:book_id>/', views.detail, name='detail'),
    # ex: /library/books/5/loans/
    path('books/<int:book_id>/loans/', views.loans_of_book, name='results'),
    # ex: /library/books/5/lend/
    path('books/<int:book_id>/lend/', views.lend_book),
]
