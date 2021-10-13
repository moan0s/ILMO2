import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from library.models import OpeningHours
from django.urls import reverse

class RenewItemForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

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
    to_hour = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}))
    class Meta:
        model = OpeningHours
        fields = ['weekday', 'from_hour', 'to_hour']
        labels = {'from_hour': _('Open from'),
                  'to_hour': _('Open until')}

    def clean_hours(self):
        data = self.cleaned_data

        # Check if opening is before closing
        if data['from_hour'] > data['to_hour']:
            raise ValidationError(_('Library must be open before closing 😉'))

        return data

    def get_success_url(self):
        return reverse('library:openinghours')