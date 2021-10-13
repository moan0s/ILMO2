from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='library/', permanent=True)),
    path('library/', include('library.urls')),
    path('admin/', admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
]


