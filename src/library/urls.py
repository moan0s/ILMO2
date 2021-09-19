from django.urls import path

from . import views
app_name = "library"
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /books/
    path('books/', views.book_list, name='books'),
    # ex: /library/books/5/
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    # ex: /library/books/5/loans/
    path('books/<int:book_id>/loans/', views.loans_of_book),
    # ex: /library/books/5/lend/
    path('books/<int:book_id>/lend/', views.lend_book),
]
