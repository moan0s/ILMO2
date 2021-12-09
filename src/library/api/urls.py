from django.urls import path
from .views import (
    BookApiView,
)

urlpatterns = [
    path('book', BookApiView.as_view()),
]
