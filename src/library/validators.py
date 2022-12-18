from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_prefix(prefix):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )