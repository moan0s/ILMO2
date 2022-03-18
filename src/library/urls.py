from django.urls import path, include

from . import views
from .views import PasswordsChangeView

app_name = "library"

""" BOOK """
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
    path('bookInstance/<slug:pk>', views.BookInstanceDetailView.as_view(), name='bookInstance-detail'),

    # ex: /library/author/5/
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

""" MATERIAL """
urlpatterns += [
    # ex: /material/
    path('materials/', views.MaterialListView.as_view(), name='materials'),
    # ex: /library/material/5/
    path('material/<int:pk>', views.MaterialDetailView.as_view(), name='material-detail'),
    # ex: /library/materialInstance/a6c3b3ae-b254-4480-8573-95868068a9c3/
    path('materialInstance/<slug:pk>', views.MaterialInstanceDetailView.as_view(),
        name='materialInstance-detail'),
]

""" LOANS """
urlpatterns += [
    # ex: /library/my-loans/
    path('my-loans/', views.list_loans_of_user, name='my-loans'),
    # ex: /library/loaned-items/
    path('loaned-items/', views.list_loans_unreturned, name='loaned-items'),
    # ex: /library/loan/1/
    path('loan/<int:pk>/', views.LoanDetailView.as_view(), name='loan-detail'),
]

""" BORROW """
urlpatterns += [
    # ex: /library/item/a6c3b3ae-b254-4480-8573-95868068a9c3/borrow/
    path('item/<uuid:pk>/borrow/', views.borrow_item, name='item-borrow'),
    # ex: /library/item/a6c3b3ae-b254-4480-8573-95868068a9c3/borrow/user/5
    path('item/<uuid:ik>/borrow/user/<slug:uk>', views.borrow_user, name='user-borrow'),
    path('item/<uuid:ik>/return', views.return_item, name='item-return'),
]

""" ITEM """
urlpatterns += [
    path('item/<uuid:pk>/renew/', views.renew_item_librarian, name='renew-item-librarian'),
    path('item/search/', views.item_search, name='item-search'),
]

""" SEARCH """
urlpatterns += [
    path('search/', views.search, name='search'),
]


""" AUTHOR """
urlpatterns += [
    # ex: /library/authors/
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    # ex: /library/author/create/
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

""" OPENING HOUR """
urlpatterns += [
    # ex: /library/openinghour/create
    path('openinghour/create', views.OpeningHoursCreateView.as_view(), name='openinghour-create'),
    # ex: /library/<int:pk>/delete
    path('openinghour/<int:pk>/delete', views.OpeningHourDeleteView.as_view(), name='openinghour-delete'),
    # ex: /library/openinghours/
    path('openinghours/', views.OpeningHoursListView.as_view(), name='openinghours'),
]

""" ACCOUNTS """
urlpatterns += [
    path('user-detail/<slug:pk>/', views.user_detail, name='user-detail'),
    path('password/', views.PasswordsChangeView.as_view(), name='password'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('accounts/', include('django.contrib.auth.urls')),
]

""" Metrics """
urlpatterns += [
    # ex: /library/metrics
    path('metrics/', views.metrics, name="metrics"),
]

""" API """
urlpatterns += [
    path('api/', include('library.api.urls')),
]
