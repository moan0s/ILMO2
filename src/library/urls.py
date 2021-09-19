from django.urls import path

from . import views
app_name = "library"
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /books/
    path('books/', views.book_list, name='books'),
    # ex: /library/books/5/
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    # ex: /library/books/5/loans/
    path('books/<int:pk>/loans/', views.loans_of_book),
    # ex: /library/books/5/lend/
    path('books/<int:pk>/lend/', views.lend_book),

    # ex: /library/author/5/
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
]
