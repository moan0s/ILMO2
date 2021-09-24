from django.urls import path, include

from . import views
app_name = "library"
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /books/
    path('books/', views.BookListView.as_view(), name='books'),
    # ex: /library/books/5/
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # ex: /library/books/5/loans/
    path('books/<int:pk>/loans/', views.loans_of_book),
    # ex: /library/books/5/lend/
    path('books/<int:pk>/lend/', views.lend_book),

    # ex: /library/author/5/
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    # ex: /library/mybooks/
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-books'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]