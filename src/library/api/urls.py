from django.urls import path
from .views import (
    BookApiView,
    AccessControlApiView
)

urlpatterns = [
    path('book', BookApiView.as_view()),
    path('uid/<slug:uk>/room/<uuid:rk>', AccessControlApiView.as_view(), name='access-check'),
]
