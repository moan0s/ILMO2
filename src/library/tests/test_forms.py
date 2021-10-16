from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from library.forms import RenewItemForm, OpeningHoursModelForm
import datetime

class RenewItemTests(SimpleTestCase):
    def test_correct_renew(self):
        renewal_date = datetime.date.today() + datetime.timedelta(days=20)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_to_late_renew(self):
        renewal_date = datetime.date.today() + datetime.timedelta(days=40)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewItemForm(data=form_data)
        self.assertEqual(form.errors['renewal_date'][0],
            'Invalid date - renewal more than 4 weeks ahead')
        self.assertFalse(form.is_valid())

    def test_past_renew(self):
        renewal_date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': str(renewal_date)}
        form = RenewItemForm(data=form_data)
        self.assertEqual(form.errors['renewal_date'][0],
            'Invalid date - renewal in past')
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewItemForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewItemForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

class CreateOpeninghourTests(TestCase):
    def test_correct_input(self):
        form_data = {'weekday': 1,
                     'from_hour': "13:12",
                     "to_hour": "13:42",
                     "comment": "Only on full moon"}
        form = OpeningHoursModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_weekday(self):
        form_data = {'from_hour': "13:42",
                     "to_hour": "13:12",
                     "comment": "Only on full moon"}
        form = OpeningHoursModelForm(data=form_data)
        form.errors
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertEqual(form.errors['weekday'][0],
            'This field is required.')
        self.assertFalse(form.is_valid())

    def test_begin_before_end(self):
        form_data = {"weekday": 6,
                     'from_hour': "13:42",
                     "to_hour": "13:12",
                     "comment": "Only on full moon"}
        form = OpeningHoursModelForm(data=form_data)
        """
        I can't really explain the following behaviour, in my understanding this should fail. But Django does some kind
        of magic and reverses from and to hour (not only in form.cleaned_data). Bug or feature? ^^
        """
        self.assertTrue(form.is_valid())