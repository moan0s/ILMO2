from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from . import views
from .views import *

urlpatterns = i18n_patterns(
    path('', RedirectView.as_view(url='library/', permanent=True)),
    path('library/', include('library.urls')),
    path('admin/', admin.site.urls, name="admin"),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path(".well-known/security.txt", security_txt),
    path("api-auth/", include('rest_framework.urls')),
    prefix_default_language=False
)
