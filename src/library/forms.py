import datetime

from django import forms
from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from library.helpers import validate_book_prefix
from library.models import OpeningHours
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class RenewItemForm(forms.Form):
    template_name = 'library/forms/form_snippets.html'
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


class BookAddViaTemplateForm(Form):
    book_prefix = forms.CharField(label='Book prefix',
                                  max_length=10,
                                  validators=[RegexValidator(regex="[A-Z][A-Z][0-9]+",
                                                             message=_("Not a valid book prefix"))])
    title = forms.CharField(label='Title of the book', max_length=200)
    author_name = forms.CharField(label='Author name(s)', max_length=100)
    number_of_instances = forms.IntegerField(label="Number of book instances to create",
                                             validators=[])


class UserFreeSearchForm(forms.Form):
    query = forms.CharField(max_length=100)

    def clean_message(self):
        # Accept any message, unless it contains the word 'chimera'
        message = self.cleaned_data['message']
        if 'chimera' in message.lower():
            raise forms.ValidationError('What did I tell you about chimeras?!')
        return message


class ItemSearchForm(forms.Form):
    template_name = 'library/forms/form_snippets.html'

    query = forms.CharField(max_length=100, label=_('Item Label'))


class UserSearchForm(forms.Form):
    template_name = 'library/forms/form_snippets.html'

    query = forms.CharField(max_length=100, label=_("User"), help_text=_("Search by name, email or username"))
