from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    verbose_name=_('Library')
