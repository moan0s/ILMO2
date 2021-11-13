from django.conf.urls import url
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
    # ex: /library/bookInstance/a6c3b3ae-b254-4480-8573-95868068a9c3/
    url(r'^bookInstance/(?P<pk>[0-9A-Fa-f-]+)/$', views.BookInstanceDetailView.as_view(), name='bookInstance-detail'),

    # ex: /library/author/5/
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    # ex: /material/
    path('materials/', views.MaterialListView.as_view(), name='materials'),
    # ex: /library/material/5/
    path('material/<int:pk>', views.MaterialDetailView.as_view(), name='material-detail'),
    # ex: /library/materialInstance/a6c3b3ae-b254-4480-8573-95868068a9c3/
    url(r'^materialInstance/(?P<pk>[0-9A-Fa-f-]+)/$', views.MaterialInstanceDetailView.as_view(), name='materialInstance-detail'),
]

urlpatterns += [
    # ex: /library/my-loans/
    path('my-loans/', views.list_loans_of_user, name='my-loans'),
     # ex: /library/loaned-books/
    path('loaned-items/', views.list_loans_unreturned, name='loaned-items'),
]
urlpatterns += [
    # ex: /library/item/a6c3b3ae-b254-4480-8573-95868068a9c3/borrow/
    path('item/<uuid:pk>/borrow/', views.borrow_item, name='item-borrow'),
    # ex: /library/item/a6c3b3ae-b254-4480-8573-95868068a9c3/borrow/user/5
    path('item/<uuid:ik>/borrow/user/<int:uk>', views.borrow_user, name='user-borrow'),
    ]

urlpatterns += [
    path('item/<uuid:pk>/renew/', views.renew_item_librarian, name='renew-item-librarian'),
]

urlpatterns += [
    # ex: /library/authors/
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    # ex: /library/author/create/
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

#URL patterns for loan
urlpatterns += [
    path('loan/<int:pk>/', views.LoanDetailView.as_view(), name='loan-detail'),
]

urlpatterns += [
    # ex: /library/openinghour/create
    path('openinghour/create', views.OpeningHoursCreateView.as_view(), name='openinghour-create'),
    # ex: /library/<int:pk>/delete
    path('openinghour/<int:pk>/delete', views.OpeningHourDeleteView.as_view(), name='openinghour-delete'),
    # ex: /library/openinghours/
    path('openinghours/', views.OpeningHoursListView.as_view(), name='openinghours'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]