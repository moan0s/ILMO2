from django.contrib import admin
from .models import Book, Loan, BookInstance, Genre, Author

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Author)

