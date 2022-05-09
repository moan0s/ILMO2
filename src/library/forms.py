import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from library.models import OpeningHours
from django.urls import reverse
from django.contrib.auth.models import User


class RenewItemForm(forms.Form):
    renewal_date = forms.DateField(help_text=_("Enter a date between now and 4 weeks (default 3)."))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class OpeningHoursModelForm(ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['weekday', 'from_hour', 'to_hour']
        labels = {'from_hour': _('Open from'),
                  'to_hour': _('Open until')}

    def clean(self):
        cleaned_data = super().clean()
        from_hour = cleaned_data.get("from_hour")
        to_hour = cleaned_data.get("to_hour")

        if from_hour and to_hour:
            # Only do something if both fields are valid so far.
            if from_hour > to_hour:
                raise ValidationError(_('Library must be open before closing 😉'))


class UserSearchForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    use_required_attribute = False
